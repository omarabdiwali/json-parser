# JSON Parser from Scratch

A lightweight, dependency-free JSON parser implemented in pure Python. This project demonstrates how to parse JSON files without using the built-in `json` module.

## Features

- Parses JSON objects (`{}`) and arrays (`[]`)
- Handles strings (with escape sequence handling support)
- Parses numbers (integers and floating-point)
- Supports boolean values (`true`, `false`) and `null`
- Whitespace handling
- Command-line interface for file input
- Uses recursive descent parsing algorithm

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

The parser uses **recursive descent parsing** with the following core functions:

- **`parseString(content, index)`**: Parses JSON strings with proper handling of escape sequences (like `\"`, `\\`)
- **`parseNumber(content, index)`**: Parses integers and floating-point numbers using regex pattern matching
- **`parseBoolAndNull(content, index)`**: Parses boolean (`true`/`false`) and `null` values using regex pattern matching
- **`parseList(content, index)`**: Recursively parses JSON arrays
- **`parseObject(content, index)`**: Recursively parses JSON objects with key-value pairs

The parser follows these steps:
1. Reads the entire file content using UTF-8 encoding
2. Strips whitespace and removes line breaks
3. Processes the content character by character
4. Builds the corresponding Python data structure (dict, list, str, int, float, bool, or None)

## Error Handling

The parser includes basic error handling:
- Validates that JSON files start with a valid starting character
- Raises exceptions for unknown characters during parsing
- Provides detailed error messages including the position and surrounding context

## Performance

The parser displays parsing duration in seconds after processing, giving users insight into parsing performance.

## Limitations

- Memory-intensive for very large JSON files as it loads entire file into memory

## License

MIT License