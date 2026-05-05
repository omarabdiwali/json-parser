# JSON Parser from Scratch

A lightweight, dependency-free JSON parser implemented in pure Python. This project demonstrates how to parse JSON files without using the built-in `json` module.

## Features

- Parses **any JSON value**: objects (`{}`), arrays (`[]`), strings, numbers, booleans (`true`, `false`), and `null`
- Handles strings with escape sequence handling support (like `\"`, `\\`, etc.)
- Parses numbers (integers and floating-point)
- Supports boolean values and `null`
- **Stringification**: Converts Python objects back to JSON strings
- Whitespace handling
- Command-line interface for file input
- Uses recursive descent parsing algorithm
- Detailed error messages with position and context information

## Requirements

- Python 3.6+

## Usage

### Command Line
```bash
python main.py <json-file-path>
```

### Example
```bash
python main.py data.json
```

### Using as a Module
You can also use the parser and stringifier in your Python code:

```python
from main import parse, stringify

# Parse a JSON string
json_data = '{"name": "John", "age": 30}'
parsed = parse(json_data)
print(parsed)  # {'name': 'John', 'age': 30}

# Convert back to JSON string
json_string = stringify(parsed)
print(json_string)  # {"name":"John","age":30}
```

## Implementation Details

The parser uses **recursive descent parsing** with the following core functions:

### Parsing Functions
- **`parseString(content, index)`**: Parses JSON strings with proper handling of escape sequences
- **`parseNumber(content, index)`**: Parses integers and floating-point numbers using regex pattern matching
- **`parseBoolAndNull(content, index)`**: Parses boolean (`true`/`false`) and `null` values
- **`parseArray(content, index)`**: Recursively parses JSON arrays
- **`parseObject(content, index)`**: Recursively parses JSON objects with key-value pairs
- **`parse(content)`**: Main entry point that determines the JSON value type and routes to appropriate parser

### Stringification Functions
- **`stringifyDict(obj)`**: Converts Python dictionaries to JSON object strings
- **`stringifyList(array, depth)`**: Converts Python lists to JSON array strings (with optional depth tracking)
- **`stringify(json)`**: Main entry point for converting Python objects to JSON strings

### Parsing Process
1. Reads the entire file content using UTF-8 encoding
2. Strips whitespace and removes line breaks
3. Processes the content character by character
4. Builds the corresponding Python data structure (dict, list, str, int, float, bool, or None)

## Error Handling

The parser includes detailed error handling:
- Validates that JSON files start with a valid starting character
- Raises exceptions for unknown characters during parsing
- Provides error messages including:
  - The position (index) where the error occurred
  - Surrounding context (substring around the error)
  - Specific error type (while parsing object, list, etc.)

## Performance

The parser displays parsing duration in seconds after processing, giving users insight into parsing performance.

## Example Output

When running `python main.py example.json`, you might see:
```
{'name': 'John', 'age': 30, 'isStudent': False}

Parsing took 0.000123 seconds.
```

## Limitations

- Memory-intensive for very large JSON files as it loads entire file into memory
- The stringify function produces compact JSON (no pretty-printing with indentation)

## License

MIT License