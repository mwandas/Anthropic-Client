# How to use the Anthropic-Client

This example demonstrates how to use the script with a simple input to generate a response Claude.

## Prerequisites

- Python 3.x installed on your machine
- anthropic Python package installed

## Usage

To run the script with a text input:

```bash
python3 main.py "Hello Claude!"
```

### Example Output

```
*** MODEL: claude-3-5-haiku-20241022 ***
--------------------------------------------------------------------------------
Hello! How are you doing today?
--------------------------------------------------------------------------------
* Input tokens: 10 (10, 0, 0)
* Output tokens: 11
Input tokens: 10 (10, 0, 0)
Output tokens: 11
Cost: 0.0005 ¢
 - Input tokens: 0.0001 ¢
 - Output tokens: 0.0004 ¢
 - Prompt caching write tokens: 0.0000 ¢
 - Prompt caching read tokens: 0.0000 ¢
```
