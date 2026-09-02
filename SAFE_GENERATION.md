# Safe generation and replay

## Trust boundary

A Cookiecutter template is executable code. Cookiecutter renders context values
with Jinja and runs the template's Python hooks. Therefore:

- inspect or verify the template source before running it;
- treat Cookiecutter replay files, presets, and direct `--no-input` extra
  context as trusted/code-equivalent input;
- never pass a downloaded, agent-produced, form-produced, or otherwise
  untrusted JSON object directly to Cookiecutter; and
- do not interpret successful generation as evidence that the generated
  application is correct or secure.

The hooks serialize every context value as data and confine their writes to the
physical generated-project root. That prevents a quote or shell-looking value
from becoming hook source. It does not turn an untrusted Cookiecutter template
or raw Jinja context into a sandbox.

## Generate from an untrusted JSON preset

Use the repository-owned wrapper, which parses and validates JSON before
Cookiecutter sees it:

```bash
uv run python scripts/generate_safe.py \
  --preset ./project-preset.json \
  --output-dir ./generated
```

A preset may contain any subset of these string fields:

```json
{
  "project_name": "Café Delta",
  "project_slug": "cafe-delta",
  "package_name": "cafe_delta",
  "project_description": "A small, evidence-oriented Python service.",
  "author_name": "Zoë Li",
  "author_email": "zoe.li@cafe-delta.dev",
  "copyright_holder": "Café Delta contributors",
  "copyright_year": "current",
  "python_version": "3.12",
  "license": "MIT",
  "include_github_actions": "yes",
  "minimum_coverage": "90",
  "max_crap_score": "30",
  "minimum_mutation_score": "80"
}
```

Omitted `project_slug`, `package_name`, `author_name`, and `copyright_holder`
values are derived from the project name. The derived author is the project's
contributor group, not an invented person. Omitted `author_email` is recorded
as `not-provided` and is left out of package metadata; supply a real contact
address only when the project has one. If name derivation produces an
unsupported identifier—for example, from a non-ASCII project name—supply
explicit ASCII identifiers as in the example.

The raw template uses `current` as its copyright-year default. The safe wrapper
resolves that sentinel before rendering, while the direct hook resolves it
during rendering. In both cases the replay file stores the concrete four-digit
year. An explicitly supplied four-digit year remains unchanged on replay.

The wrapper rejects, before Cookiecutter execution:

- Jinja delimiters anywhere in the JSON;
- duplicate or unknown keys and non-string context values;
- control and Unicode format characters;
- unsafe distribution/import names, keywords, and standard-library collisions;
- malformed, nonfinite, decimal, negative, or out-of-range thresholds;
- unsupported enum choices;
- placeholder author names, placeholder email local parts, and email addresses
  under the reserved example, test, invalid, or localhost domains;
- placeholder or empty copyright holders and invalid years (with `current`
  accepted only as the documented dynamic-year sentinel);
- fields that cannot be represented safely in the generated TOML; and
- an existing or symlink output target.

Ordinary Unicode human text and punctuation such as apostrophes, ampersands,
semicolons, dollar signs, and parentheses are preserved. Double quotes and
backslashes in fields embedded by the current TOML template are rejected with
a field-specific message rather than generating broken TOML.

## Replay an exact context

Each successful render records the validated public context at:

```text
.cleanai/template-context.json
```

The file includes the explicitly selected copyright year. It contains no local
template path or generation timestamp, so it can be reviewed, versioned, and
replayed deterministically:

```bash
uv run python scripts/generate_safe.py \
  --preset ./previous-project/.cleanai/template-context.json \
  --output-dir ./replayed
```

Use `current` for a new project when generation-time resolution is wanted. Keep
the recorded concrete year when replaying the same legal/project context;
change it deliberately when creating a distinct project or when counsel
requires a different notice.

## License outputs

- `MIT` writes the standard MIT text with the selected year and holder.
- `Apache-2.0` writes the standard Apache License 2.0 text and a `NOTICE` with
  the selected project, year, and holder. Bracketed text in the Apache appendix
  is part of the canonical license's instructions; it is not project metadata.

This open-source scientific variant intentionally offers only OSI-approved MIT
and Apache-2.0 code licenses. Data, documentation, figures, model weights,
dependencies, and other third-party artifacts may have separate terms.

Every generated project also retains the template's MIT terms in
`TEMPLATE_LICENSE`. The selected project license applies only to rights the
named holder is authorized to license; it does not override the template
license, dependency licenses, or other third-party terms.

License choice and legal identity are recorded in the replay context. License
generation is configuration output, not a legal finding of ownership. Review
the result with appropriate legal counsel for consequential distribution.
