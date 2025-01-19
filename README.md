# How to use the Anthropic-Client

This example demonstrates how to use the script with a simple input to generate a response Claude.

## Prerequisites

- Python 3.x installed on your machine
- anthropic Python package installed

## Usage

To run the script with a text input:

```bash
python3 main.py
```

This script operates in chat mode. It prompts the user for input, displays the response from Claude, and then waits for the next user input. The complete conversation history is passed to the Claude API to enable more context-aware responses.

To exit the application, type 'exit' as user input.

### Example Output

```
Enter your message (or 'exit' to quit): How many 'r' are in strawberry?

You:  How many 'r' are in strawberry?
claude-3-5-haiku-20241022:  There is 1 "r" in the word "strawberry".
--------------------------------------------------------------------------------
* Input tokens: 18 (18, 0, 0)
* Output tokens: 18

Cost: 0.0009 ¢
  - Input tokens: 0.0001 ¢
  - Output tokens: 0.0007 ¢
  - Prompt caching write tokens: 0.0000 ¢
  - Prompt caching read tokens: 0.0000 ¢
--------------------------------------------------------------------------------

Enter your message (or 'exit' to quit): It is incorrecct.

You:  It is incorrecct.
claude-3-5-haiku-20241022:  Let me count the "r" letters in "strawberry" for you:

s t r a w b e r r y

There are actually 2 "r" letters in the word "strawberry".
--------------------------------------------------------------------------------
* Input tokens: 45 (45, 0, 0)
* Output tokens: 48

Cost: 0.0023 ¢
  - Input tokens: 0.0004 ¢
  - Output tokens: 0.0019 ¢
  - Prompt caching write tokens: 0.0000 ¢
  - Prompt caching read tokens: 0.0000 ¢
--------------------------------------------------------------------------------

Enter your message (or 'exit' to quit): Still incorrect

You:  Still incorrect
claude-3-5-haiku-20241022:  Let me count carefully:
s t r a w b e r r y

You're right, and my previous answers were wrong. There are 3 "r" letters in "strawberry".

Thank you for your patience in helping me get to the correct answer.
--------------------------------------------------------------------------------
* Input tokens: 98 (98, 0, 0)
* Output tokens: 60

Cost: 0.0032 ¢
  - Input tokens: 0.0008 ¢
  - Output tokens: 0.0024 ¢
  - Prompt caching write tokens: 0.0000 ¢
  - Prompt caching read tokens: 0.0000 ¢
--------------------------------------------------------------------------------

Enter your message (or 'exit' to quit): exit
Exiting chat...
```
