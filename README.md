# JSON Parser from Scratch

A lightweight, dependency-free JSON parser implemented in pure Python. This project demonstrates how to parse JSON files without using the built-in `json` module.

## Features

- Parses JSON objects (`{}`) and arrays (`[]`)
- Handles strings (with escape character support)
- Parses numbers (integers and floats)
- Supports boolean values (`true`, `false`) and `null`
- Whitespace handling
- Command-line interface for file input

## Requirements

- Python 3.6+

## Usage

```bash
python main.py <json-file-path>
```

### Example

```bash
python main.py data.json
```

## Implementation Details

The parser uses recursive descent parsing with the following key functions:

- **`parseString(content, index)`**: Parses JSON strings with escape sequence handling
- **`parseNumber(content, index)`**: Parses integers and floating-point numbers
- **`parseBoolOrNull(content, index)`**: Parses boolean and null values
- **`parseList(content, index)`**: Parses JSON arrays recursively
- **`parseObject(content, index)`**: Parses JSON objects with key-value pairs

The parser reads the entire file content, removes line breaks, and processes it character by character to build the corresponding Python data structure (dict, list, str, int, float, bool, or None).

## Limitations

- Limited escape sequence handling in strings
- No validation for malformed JSON beyond basic structure

## License

MIT License