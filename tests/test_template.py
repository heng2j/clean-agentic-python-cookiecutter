from __future__ import annotations

import compileall
import importlib.util
import json
import shutil
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest
from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter
from jinja2 import Environment


ROOT = Path(__file__).parents[1]
SAFE_WRAPPER = ROOT / "scripts" / "generate_safe.py"


def _load_safe_wrapper() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cleanai_safe_generator", SAFE_WRAPPER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SAFE = _load_safe_wrapper()


def _render(tmp_path: Path, context: dict[str, str] | None = None) -> Path:
    output = tmp_path / "output"
    output.mkdir(parents=True)
    return Path(
        cookiecutter(
            str(ROOT),
            no_input=True,
            output_dir=str(output),
            extra_context=context or {},
        )
    )


def _assert_render_fails(tmp_path: Path, context: dict[str, str]) -> None:
    output = tmp_path / "output"
    output.mkdir()
    with pytest.raises((CookiecutterException, ValueError)):
        cookiecutter(
            str(ROOT),
            no_input=True,
            output_dir=str(output),
            extra_context=context,
        )


def _valid_context(**overrides: str) -> dict[str, str]:
    context = {
        "author_email": "maintainers@acme.dev",
        "author_name": "Acme Engineering Maintainers",
        "copyright_holder": "Example Project contributors",
        "copyright_year": str(date.today().year),
        "include_github_actions": "yes",
        "license": "MIT",
        "max_crap_score": "30",
        "minimum_coverage": "90",
        "minimum_mutation_score": "80",
        "package_name": "example_project",
        "project_description": "An example project.",
        "project_name": "Example Project",
        "project_slug": "example-project",
        "python_version": "3.12",
    }
    context.update(overrides)
    return context


def test_default_template_renders_compiles_and_records_context(tmp_path: Path) -> None:
    project = _render(tmp_path)

    assert (project / "AGENTS.md").is_file()
    assert (project / "CLAUDE.md").read_text(encoding="utf-8").startswith("@AGENTS.md")
    assert (project / "tools" / "cleanai.py").is_file()
    assert (project / "prompts" / "specifier.md").is_file()
    for relative in (
        "CONTRIBUTING.md",
        "SECURITY.md",
        ".github/pull_request_template.md",
        ".env.example",
        ".envrc",
        "prek.toml",
        "notebooks/README.md",
        "results/README.md",
        "results/.gitignore",
        "results/reference/README.md",
        "scripts/README.md",
        "static/README.md",
        "static/manifest.toml",
        "docs/science/scientific-method.md",
        "docs/science/reproducibility.md",
        "docs/science/data-and-secrets.md",
    ):
        assert (project / relative).is_file(), relative
    assert not (project / ".pre-commit-config.yaml").exists()
    assert compileall.compile_dir(project / "src", quiet=1)
    assert compileall.compile_file(project / "tools" / "cleanai.py", quiet=1)
    with (project / "pyproject.toml").open("rb") as stream:
        tomllib.load(stream)

    replay = json.loads((project / ".cleanai" / "template-context.json").read_text(encoding="utf-8"))
    assert replay["schema_version"] == 1
    assert replay["template"] == "clean-agentic-scientific-python-cookiecutter-v1"
    assert replay["context"]["copyright_year"] == str(date.today().year)
    assert replay["context"]["copyright_holder"] == (
        "Clean Agentic Scientific Python Project contributors"
    )
    assert replay["context"]["author_name"] == (
        "Clean Agentic Scientific Python Project contributors"
    )
    assert replay["context"]["author_email"] == "not-provided"
    assert "_template" not in replay["context"]
    assert not (project / ".cleanai" / "_license_assets").exists()
    with (project / "pyproject.toml").open("rb") as stream:
        metadata = tomllib.load(stream)
    assert metadata["project"]["authors"] == [
        {"name": "Clean Agentic Scientific Python Project contributors"}
    ]


def test_default_copyright_year_is_current_and_replayable() -> None:
    raw = json.loads((ROOT / "cookiecutter.json").read_text(encoding="utf-8"))
    assert raw["copyright_year"] == "current"
    assert raw["author_name"] == "{{ cookiecutter.project_name }} contributors"
    assert raw["author_email"] == "not-provided"
    assert raw["copyright_holder"] == "{{ cookiecutter.project_name }} contributors"


def test_choices_are_fixed() -> None:
    raw = json.loads((ROOT / "cookiecutter.json").read_text(encoding="utf-8"))
    assert raw["python_version"] == ["3.12", "3.13"]
    assert raw["license"] == ["MIT", "Apache-2.0"]
    assert raw["include_github_actions"] == ["yes", "no"]


def test_scientific_profile_has_one_config_authority_per_tool(tmp_path: Path) -> None:
    project = _render(tmp_path)
    pyproject = (project / "pyproject.toml").read_text(encoding="utf-8")
    policy = (project / ".cleanai/policy.toml").read_text(encoding="utf-8")
    gitignore = (project / ".gitignore").read_text(encoding="utf-8")

    assert "[tool.coverage.run]" in pyproject
    assert not (project / ".coveragerc").exists()
    assert (project / "prek.toml").is_file()
    assert not (project / ".pre-commit-config.yaml").exists()
    assert "pyrefly check --min-severity warn --summarize-errors" in policy
    assert "ty check" not in policy.split("[gauntlet.fast]", maxsplit=1)[1].split(
        "[gauntlet.full]", maxsplit=1
    )[0]
    assert "science-audit --strict" in policy
    assert "rumdl check" in policy
    assert ".env\n" in gitignore
    assert "!.env.example" in gitignore


def test_scientific_connected_ci_is_bounded_and_pinned(tmp_path: Path) -> None:
    project = _render(tmp_path)
    workflow = (project / ".github/workflows/quality.yml").read_text(encoding="utf-8")

    assert "connected / Codecov publication" in workflow
    assert "github.event_name == 'push'" in workflow
    assert "continue-on-error: true" in workflow
    assert "id-token: write" in workflow
    assert "codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f" in workflow
    assert 'version: "v11.3.1"' in workflow
    assert "disable_search: true" in workflow
    assert "fail_ci_if_error: true" in workflow
    assert "coverage xml" in workflow


@pytest.mark.parametrize(
    ("license_id", "expected_first_line"),
    [
        ("MIT", "MIT License"),
        ("Apache-2.0", "Apache License"),
    ],
)
def test_license_outputs_are_complete(
    tmp_path: Path,
    license_id: str,
    expected_first_line: str,
) -> None:
    context = _valid_context(
        license=license_id,
        copyright_holder="Élan Research Cooperative",
        copyright_year="2026",
    )
    project = _render(tmp_path, context)
    license_text = (project / "LICENSE").read_text(encoding="utf-8")
    assert license_text.splitlines()[0] == expected_first_line
    assert "@@COPYRIGHT" not in license_text
    assert "Your Name" not in license_text
    assert (project / "TEMPLATE_LICENSE").read_text(encoding="utf-8") == (
        ROOT / "LICENSE"
    ).read_text(encoding="utf-8")

    with (project / "pyproject.toml").open("rb") as stream:
        metadata = tomllib.load(stream)
    expected_license_files = ["LICENSE", "TEMPLATE_LICENSE"]
    if license_id == "Apache-2.0":
        expected_license_files.append("NOTICE")
    assert metadata["project"]["license-files"] == expected_license_files

    if license_id == "Apache-2.0":
        expected = (
            ROOT
            / "{{cookiecutter.project_slug}}"
            / ".cleanai"
            / "_license_assets"
            / "Apache-2.0.txt"
        ).read_text(encoding="utf-8")
        assert license_text == expected
        notice = (project / "NOTICE").read_text(encoding="utf-8")
        assert "Copyright 2026 Élan Research Cooperative" in notice
        assert "[yyyy]" not in notice
    else:
        assert "Copyright (c) 2026 Élan Research Cooperative" in license_text
        assert not (project / "NOTICE").exists()

    replay = json.loads((project / ".cleanai" / "template-context.json").read_text(encoding="utf-8"))
    assert replay["context"]["license"] == license_id
    assert replay["context"]["copyright_holder"] == "Élan Research Cooperative"


def test_unicode_human_fields_and_ordinary_metacharacters_are_preserved(tmp_path: Path) -> None:
    context = _valid_context(
        project_name="Café Delta 研究",
        project_slug="cafe-delta",
        package_name="cafe_delta",
        project_description="O'Reilly & Sons; $5 (R&D) — résumé ✓.",
        author_name="Zoë Li",
        author_email="zoe.li@cafe-delta.dev",
        copyright_holder="李氏 Research Cooperative",
    )
    project = _render(tmp_path, context)
    replay = json.loads((project / ".cleanai" / "template-context.json").read_text(encoding="utf-8"))
    assert replay["context"]["project_name"] == "Café Delta 研究"
    assert replay["context"]["project_description"] == "O'Reilly & Sons; $5 (R&D) — résumé ✓."
    assert replay["context"]["author_name"] == "Zoë Li"
    assert "李氏 Research Cooperative" in (project / "LICENSE").read_text(encoding="utf-8")
    with (project / "pyproject.toml").open("rb") as stream:
        metadata = tomllib.load(stream)
    assert metadata["project"]["authors"][0]["name"] == "Zoë Li"


@pytest.mark.parametrize(
    "context",
    [
        {"project_slug": ""},
        {"project_slug": "../escape", "package_name": "escape"},
        {"project_slug": "/tmp/escape", "package_name": "escape"},
        {"project_slug": "nested/escape", "package_name": "escape"},
        {"project_slug": "Bad-Slug", "package_name": "bad_slug"},
        {"project_slug": "bad-slug-", "package_name": "bad_slug_"},
        {"project_slug": "bad;slug", "package_name": "bad_slug"},
        {"project_slug": "package-keyword", "package_name": "class"},
        {"project_slug": "package-hyphen", "package_name": "bad-name"},
        {"project_slug": "package-digit", "package_name": "123pkg"},
        {"project_slug": "package-capital", "package_name": "CamelCase"},
        {"project_slug": "package-unicode", "package_name": "δοκιμή"},
        {"project_slug": "package-empty", "package_name": ""},
        {"project_slug": "package-json", "package_name": "json"},
        {"project_slug": "package-email", "package_name": "email"},
        {"project_slug": "safe-project", "package_name": "safe_project", "project_name": "bad\nname"},
        {"project_slug": "safe-project", "package_name": "safe_project", "project_description": "bad\u202ename"},
        {"project_slug": "safe-project", "package_name": "safe_project", "author_name": "bad\tname"},
        {"project_slug": "safe-project", "package_name": "safe_project", "author_name": "A \"Quoted\" Name"},
        {"project_slug": "safe-project", "package_name": "safe_project", "author_name": ""},
        {"project_slug": "safe-project", "package_name": "safe_project", "author_name": "Your Name"},
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_name": "Example Maintainer",
        },
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_name": "[author name]",
        },
        {"project_slug": "safe-project", "package_name": "safe_project", "project_description": "C:\\project"},
        {"project_slug": "safe-project", "package_name": "safe_project", "author_email": "a\"b@example.com"},
        {"project_slug": "safe-project", "package_name": "safe_project", "author_email": ""},
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_email": "you@acme.dev",
        },
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_email": "engineer@example.com",
        },
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_email": "engineer@sub.example.org",
        },
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_email": "engineer@acme.test",
        },
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_email": "engineer@acme.invalid",
        },
        {
            "project_slug": "safe-project",
            "package_name": "safe_project",
            "author_email": "engineer@localhost",
        },
        {"project_slug": "safe-project", "package_name": "safe_project", "copyright_holder": ""},
        {"project_slug": "safe-project", "package_name": "safe_project", "copyright_holder": "Your Name"},
        {"project_slug": "safe-project", "package_name": "safe_project", "copyright_holder": "[name of copyright owner]"},
        {"project_slug": "safe-project", "package_name": "safe_project", "copyright_year": "26"},
        {"project_slug": "safe-project", "package_name": "safe_project", "copyright_year": "2026.0"},
        {"project_slug": "safe-project", "package_name": "safe_project", "copyright_year": "9999"},
        {"minimum_coverage": "-1"},
        {"minimum_coverage": "101"},
        {"minimum_coverage": "nan"},
        {"minimum_coverage": "1.5"},
        {"minimum_coverage": "090"},
        {"minimum_coverage": ""},
        {"max_crap_score": "-1"},
        {"max_crap_score": "nan"},
        {"max_crap_score": "inf"},
        {"max_crap_score": "30.5"},
        {"max_crap_score": "abc"},
        {"max_crap_score": ""},
        {"minimum_mutation_score": "-1"},
        {"minimum_mutation_score": "101"},
        {"minimum_mutation_score": "nan"},
        {"minimum_mutation_score": "80.5"},
        {"minimum_mutation_score": "abc"},
        {"minimum_mutation_score": ""},
        {"python_version": "3.11"},
        {"license": "Proprietary"},
        {"include_github_actions": "maybe"},
    ],
)
def test_invalid_context_fails_before_a_usable_project(tmp_path: Path, context: dict[str, str]) -> None:
    _assert_render_fails(tmp_path, context)


@pytest.mark.parametrize(
    "context",
    [
        {"minimum_coverage": "0"},
        {"minimum_coverage": "100"},
        {"max_crap_score": "0"},
        {"max_crap_score": "1000000"},
        {"minimum_mutation_score": "0"},
        {"minimum_mutation_score": "100"},
    ],
)
def test_threshold_boundaries_render(tmp_path: Path, context: dict[str, str]) -> None:
    project = _render(tmp_path, context)
    with (project / "pyproject.toml").open("rb") as stream:
        tomllib.load(stream)
    assert compileall.compile_dir(project / "src", quiet=1)


def test_not_provided_email_is_omitted_but_custom_email_is_preserved(tmp_path: Path) -> None:
    no_email = _render(tmp_path / "no-email", _valid_context(author_email="not-provided"))
    with (no_email / "pyproject.toml").open("rb") as stream:
        no_email_metadata = tomllib.load(stream)
    assert no_email_metadata["project"]["authors"] == [
        {"name": "Acme Engineering Maintainers"}
    ]

    with_email = _render(
        tmp_path / "with-email",
        _valid_context(author_email="release@acme.dev"),
    )
    with (with_email / "pyproject.toml").open("rb") as stream:
        with_email_metadata = tomllib.load(stream)
    assert with_email_metadata["project"]["authors"] == [
        {"email": "release@acme.dev", "name": "Acme Engineering Maintainers"}
    ]


def test_prior_pre_hook_injection_payload_is_rejected_without_execution(tmp_path: Path) -> None:
    marker = tmp_path / "output" / "PRE_HOOK_ESCAPE_MARKER"
    payload = (
        '"; __import__("pathlib").Path.cwd().parent.joinpath("PRE_HOOK_ESCAPE_MARKER")'
        '.write_text("escaped", encoding="utf-8"); project_slug="safe'
    )
    _assert_render_fails(tmp_path, {"project_slug": payload, "package_name": "safe"})
    assert not marker.exists()


def test_prior_post_hook_injection_payload_is_rejected_without_execution(tmp_path: Path) -> None:
    marker = tmp_path / "output" / "POST_HOOK_ESCAPE_MARKER"
    payload = (
        '"; __import__("pathlib").Path("../POST_HOOK_ESCAPE_MARKER")'
        '.write_text("escaped", encoding="utf-8"); author="'
    )
    _assert_render_fails(
        tmp_path,
        {"project_slug": "post-hook-project", "package_name": "post_hook_project", "author_name": payload},
    )
    assert not marker.exists()


def test_code_looking_holder_is_data_not_hook_source(tmp_path: Path) -> None:
    marker = tmp_path / "output" / "HOLDER_ESCAPE_MARKER"
    payload = (
        '"; __import__("pathlib").Path("../HOLDER_ESCAPE_MARKER")'
        '.write_text("escaped", encoding="utf-8"); holder="'
    )
    project = _render(
        tmp_path,
        _valid_context(copyright_holder=payload, project_slug="holder-data", package_name="holder_data"),
    )
    assert not marker.exists()
    assert payload in (project / "LICENSE").read_text(encoding="utf-8")


def test_github_actions_no_removes_only_the_optional_workflow(tmp_path: Path) -> None:
    project = _render(tmp_path, {"include_github_actions": "no"})
    assert not (project / ".github" / "workflows" / "quality.yml").exists()
    assert (project / ".cleanai" / "template-context.json").is_file()


def test_post_hook_refuses_a_license_symlink_without_touching_target(tmp_path: Path) -> None:
    fake_root = tmp_path / "fake-project"
    assets = fake_root / ".cleanai" / "_license_assets"
    shutil.copytree(
        ROOT / "{{cookiecutter.project_slug}}" / ".cleanai" / "_license_assets",
        assets,
    )
    outside = tmp_path / "outside-license.txt"
    outside.write_text("outside remains unchanged\n", encoding="utf-8")
    try:
        (fake_root / "LICENSE").symlink_to(outside)
    except OSError as error:
        pytest.skip(f"symlinks unavailable: {error}")

    hook_source = (ROOT / "hooks" / "post_gen_project.py").read_text(encoding="utf-8")
    rendered_hook = Environment(autoescape=False).from_string(hook_source).render(
        cookiecutter=_valid_context()
    )
    hook = tmp_path / "rendered-post-hook.py"
    hook.write_text(rendered_hook, encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(hook)],
        cwd=fake_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert completed.returncode != 0
    assert "refusing symlink path" in completed.stdout
    assert outside.read_text(encoding="utf-8") == "outside remains unchanged\n"


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def test_safe_wrapper_generates_and_replays_reviewed_context(tmp_path: Path) -> None:
    preset = tmp_path / "preset.json"
    _write_json(
        preset,
        {
            "project_name": "Café Delta",
            "project_slug": "cafe-delta",
            "package_name": "cafe_delta",
            "author_name": "Zoë Li",
            "author_email": "zoe.li@cafe-delta.dev",
            "copyright_holder": "Café Delta Cooperative",
            "copyright_year": "2026",
        },
    )
    first = SAFE.generate(preset, tmp_path / "first-output")
    replay = first / ".cleanai" / "template-context.json"
    second = SAFE.generate(replay, tmp_path / "second-output")
    assert (first / "LICENSE").read_bytes() == (second / "LICENSE").read_bytes()
    assert replay.read_bytes() == (second / ".cleanai" / "template-context.json").read_bytes()


@pytest.mark.parametrize(
    "identity",
    [
        {"author_name": "Your Name"},
        {"author_name": ""},
        {"author_email": "you@acme.dev"},
        {"author_email": "maintainer@example.net"},
        {"author_email": "maintainer@project.invalid"},
        {"author_email": ""},
    ],
)
def test_safe_wrapper_rejects_placeholder_identity(
    tmp_path: Path, identity: dict[str, str]
) -> None:
    preset = tmp_path / "preset.json"
    _write_json(
        preset,
        {
            "author_email": "maintainers@acme.dev",
            "author_name": "Acme Engineering Maintainers",
            "package_name": "safe_project",
            "project_slug": "safe-project",
            **identity,
        },
    )
    with pytest.raises(SAFE.PresetError, match="author_(?:name|email)"):
        SAFE.generate(preset, tmp_path / "output")


def test_safe_wrapper_resolves_current_year_and_derives_honest_identity(tmp_path: Path) -> None:
    preset = tmp_path / "preset.json"
    _write_json(
        preset,
        {
            "project_name": "Safe Project",
            "project_slug": "safe-project",
            "package_name": "safe_project",
        },
    )
    project = SAFE.generate(preset, tmp_path / "output")
    replay = json.loads((project / ".cleanai" / "template-context.json").read_text(encoding="utf-8"))
    assert replay["context"]["author_name"] == "Safe Project contributors"
    assert replay["context"]["author_email"] == "not-provided"
    assert replay["context"]["copyright_year"] == str(date.today().year)


def test_safe_wrapper_rejects_jinja_before_cookiecutter_executes(tmp_path: Path) -> None:
    marker = tmp_path / "JINJA_INPUT_MARKER"
    preset = tmp_path / "malicious.json"
    _write_json(
        preset,
        {
            "project_description": (
                '{{ cycler.__init__.__globals__.os.popen("touch JINJA_INPUT_MARKER").read() }}'
            )
        },
    )
    with pytest.raises(SAFE.PresetError, match="forbidden Jinja delimiter"):
        SAFE.generate(preset, tmp_path / "output")
    assert not marker.exists()
    assert not (tmp_path / "output").exists()


@pytest.mark.parametrize(
    "raw",
    [
        '{"project_name": "First", "project_name": "Second"}',
        '{"unknown": "value"}',
        '{"minimum_coverage": 90}',
        '["not", "an", "object"]',
        '{"context": {}, "schema_version": 2, "template": "clean-agentic-scientific-python-cookiecutter-v1"}',
    ],
)
def test_safe_wrapper_rejects_malformed_preset_shapes(tmp_path: Path, raw: str) -> None:
    preset = tmp_path / "preset.json"
    preset.write_text(raw, encoding="utf-8")
    with pytest.raises(SAFE.PresetError):
        SAFE.load_preset(preset)


def test_safe_wrapper_refuses_existing_symlink_target(tmp_path: Path) -> None:
    preset = tmp_path / "preset.json"
    _write_json(
        preset,
        {
            "project_name": "Safe Project",
            "project_slug": "safe-project",
            "package_name": "safe_project",
        },
    )
    output = tmp_path / "output"
    output.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "sentinel.txt"
    sentinel.write_text("unchanged\n", encoding="utf-8")
    try:
        (output / "safe-project").symlink_to(outside, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlinks unavailable: {error}")

    with pytest.raises(SAFE.PresetError, match="refusing to overwrite existing target"):
        SAFE.generate(preset, output)
    assert sentinel.read_text(encoding="utf-8") == "unchanged\n"


def test_safe_wrapper_cli_reports_refusal_without_traceback(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    preset = tmp_path / "preset.json"
    _write_json(preset, {"package_name": "json", "project_slug": "json-project"})
    result = SAFE.main(["--preset", str(preset), "--output-dir", str(tmp_path / "output")])
    captured = capsys.readouterr()
    assert result == 2
    assert "safe generation refused:" in captured.err
    assert "standard-library module" in captured.err
    assert "Traceback" not in captured.err
