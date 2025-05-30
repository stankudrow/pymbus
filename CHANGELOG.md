# CHANGELOG

## v0.5.0

- update VIF codes: tables and utils ([PR-22](https://github.com/stankudrow/pymbus/pull/22)):
  - remove the "code" attribute from the VIFCode dataclass;
  - rename the `VIFCodeDescription` enum to `VIFCodeKind`;
  - introduce the `VIFTablet` class responsible for VIF code selection;
  - remove `get_vif_code` function in favour of the the `VIFTablet` class;
  - fix VIF code selection regardless the extension (MSB) bit is set or not;
  - add VIF codes for **0xFB** code extension byte;
  - rename the "unit" attribute of the `ValueInformationField` class to "data";
  - add a minor optimisation: one VIFCode dataclass instance is used for all reserved codes.

## v0.4.0

- remake VIF codes ([PR-17](https://github.com/stankudrow/pymbus/pull/17) + [PR-18](https://github.com/stankudrow/pymbus/pull/18)):
  - only one VIFCode (data)class for coding
  - the `get_vif_code` factory method is improved

- subclass TelegramContainer from the `Sequence` ABC ([PR-16](https://github.com/stankudrow/pymbus/pull/16))

- subclass the TelegramField class from Python `int` type ([PR-15](https://github.com/stankudrow/pymbus/pull/15)):
  - make TelegramField support the operations that `int` does;
  - ensure the byte range validation for TelegramField -> the `validate` flag removed;
  - unburden and simplify TelegramField successors and classes derived from TelegramContainer;
  - revises the [PR-11](https://github.com/stankudrow/pymbus/pull/11).

- submodule specific Telegram fields (A, C, CI, Data, Value) ([PR-12](https://github.com/stankudrow/pymbus/pull/12))

- improve Telegram classes ([PR-11](https://github.com/stankudrow/pymbus/pull/11)):
  - the API of TelegramField is enriched:
    - `total_ordering` is enabled - the full set of arithmetic comparison operators are on
    - bitwise operator support:
      - and (&)
      - or (|)
      - xor (^)
      - inversion (~)
    - the `validate` flag is added
    - the `byte` attribute is removed
  - the API of TelegramContainer is enriched:
    - `total_ordering` is enabled
    - the `validate` flag is added
  - all entities related to the the TelegramField and TelegramContainer classes are updated
  - introduce the `utils` module with the `validate_byte` function
  - some obsolete entities are removed

## v0.3.0

[PR-8](https://github.com/stankudrow/pymbus/pull/8)

Added:

- more ruff rules;
- make blocks, frames and records non-greedy for exhaustible input data;
- add DataRecord class.

Changed:

- update the project metadata;
- lint the code and test base(s).

## v0.2.0

[PR-4](https://github.com/stankudrow/pymbus/pull/4)

Added:

- mypy support;
- more ruff rules;
- randomised tests with coverage.

Changed:

- API: reconsidered and flattened;
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
