# Changelog
All notable changes to this project will be documented in this file.

## [0.0.11] - 2020-06-10

### Changed

- Small speed improvement by removing left padding calculation from loop

### Fixed

- No false positive on closing parenthesis-wrapped expression inside a call
- No false positive on closing index check inside blocks

## [0.0.10] - 2020-03-11

### Fixed

- Pound sign in a string shouldn't be detected as start of comment block

## [0.0.9] - 2020-03-09

### Fixed
- Only check for function calls when checking lunula brackets

## [0.0.8] - 2020-03-06

### Fixed
- Handle nested function calls
- Ignore conditional blocks
- Ignore function calls with strange whitespace

## [0.0.7] - 2019-09-21

### Added
- Tuples are now also validated as part of 101 and 102 checks

### Fixed
- False positive on type annotation and regex

## [0.0.6] - 2019-07-29

### Fixed
- Handle situation where end character is at EOF
- Display correct error if line has multiple opening characters without any closing characters

## [0.0.5] - 2019-07-15

### Fixed
- Handle situations where a line has multiple closing characters

## [0.0.4] - 2019-06-07

### Fixed
- Escaped characters are ignored

## [0.0.3] - 2019-06-05

### Fixed
- Strings with only closing characters are ignored

## [0.0.2] - 2019-05-31

### Fixed
- Handle situations where there are uneven numbers of opening and closing characters on the same line
- Ensure opening and closing characters inside strings are ignored
