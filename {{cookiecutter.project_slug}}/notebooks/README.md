# Notebooks

Use notebooks for exploration, narrative demonstrations, and figures—not as the
only home of reusable behavior. Import the installed public package, move stable
logic into `src/{{ cookiecutter.package_name }}`, and cover that logic with tests.

Before committing a notebook, remove accidental secrets and unnecessary outputs,
identify inputs and random seeds, and record the command/tool version needed to
execute it. This starter does not install Jupyter or marimo by default; select
and lock a notebook runtime only when the project needs one.
