# CHANGELOG

## v0.3.0

[PR-8](https://github.com/stankudrow/pymbus/pull/8)

Added:

- more ruff rules;
- make blocks, frames and records non-greedy for exhaustible input data;
- add DataRecord class.

Changed:

- update project metadata;
- lint the code and test base(s).

## v0.2.0

[PR-4](https://github.com/stankudrow/pymbus/pull/4)

Added:

- mypy support;
- more ruff rules;
- randomised tests with coverage.

Changed:

- API: reconsidered and flatten;
- the former `DataRecord` class is now `DataRecordHeader`.

## v0.1.0

[PR-1](https://github.com/stankudrow/pymbus/pull/1).

Added:

- pymbus MVP:
  - Python>=3.10;
  - core objects: fields, blocks, frames, records + codes and structures;
  - pyproject.toml with uv project manager;
  - unit tests via pytest framework;
- README file;
- minimal Python .gitignore file;
- GitHub Actions workflow file;
- pre-commit configuration file;
- and some minor stuff.
