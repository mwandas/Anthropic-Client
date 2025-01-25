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

### The 'help' parameter output
```
> python3 main.py -h
usage: main.py [-h] [--model {haiku3,haiku3.5,sonnet3.5}] [--cache CACHE_FILE]

Chat with Claude.

options:
  -h, --help            show this help message and exit
  --model {haiku3,haiku3.5,sonnet3.5}
                        The model to use.
                          Options:
                           - haiku3: Haiku 3
                           - haiku3.5: Haiku 3.5
                           - sonnet3.5: Sonnet 3.5 (New)
                        Defaults to haiku3.5.
  --cache CACHE_FILE    Path to the cache text file.
```

### Example Output

```
Enter your message (or 'exit' to quit): How many 'r' are in strawberry?

You:  How many 'r' are in strawberry?
Haiku 3.5: There are 2 'r' letters in the word "strawberry".
--------------------------------------------------------------------------------
* Input tokens: 18 (18, 0, 0)
* Output tokens: 19

Cost: 0.0090 ¢
  - Input tokens: 0.0014 ¢
  - Output tokens: 0.0076 ¢
  - Prompt caching write tokens: 0.0000 ¢
  - Prompt caching read tokens: 0.0000 ¢
--------------------------------------------------------------------------------

Enter your message (or 'exit' to quit): It is incorrecct.

You:  It is incorrecct.
Haiku 3.5: I apologize, but my previous answer was correct. Let me explain:

The word "strawberry" has 2 'r' letters:
- One 'r' in "straw"
- One 'r' in "berry"

So, "strawberry" contains 2 'r' letters.

If you believe the count is different, could you please clarify why?
--------------------------------------------------------------------------------
* Input tokens: 46 (46, 0, 0)
* Output tokens: 89

Cost: 0.0393 ¢
  - Input tokens: 0.0037 ¢
  - Output tokens: 0.0356 ¢
  - Prompt caching write tokens: 0.0000 ¢
  - Prompt caching read tokens: 0.0000 ¢
--------------------------------------------------------------------------------

Enter your message (or 'exit' to quit): Still incorrect

You:  Still incorrect
Haiku 3.5: Let me count the 'r' letters carefully:

st(r)awbe(r)(r)y

There are 3 'r' letters in the word "strawberry":
1. In "straw"
2. In "berry"
3. Also in "berry"

So the correct answer is 3 'r' letters.
--------------------------------------------------------------------------------
* Input tokens: 140 (140, 0, 0)
* Output tokens: 81

Cost: 0.0436 ¢
  - Input tokens: 0.0112 ¢
  - Output tokens: 0.0324 ¢
  - Prompt caching write tokens: 0.0000 ¢
  - Prompt caching read tokens: 0.0000 ¢
--------------------------------------------------------------------------------

Enter your message (or 'exit' to quit): exit
Exiting chat...
```
