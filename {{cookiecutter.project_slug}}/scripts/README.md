# Scripts

Scripts are thin, reviewable entry points for contributor or experiment tasks.
Reusable behavior belongs in `src/{{ cookiecutter.package_name }}` and is tested
there. A script must document its inputs, outputs, side effects, network use,
failure behavior, and exact invocation. Do not create a second untested source
tree here.
