import anthropic
import sys


ANTHROPIC_KEY_FILE = 'main-key'
HAIKU3="claude-3-haiku-20240307"
HAIKU35="claude-3-5-haiku-20241022"
SONNET35NEW="claude-3-5-sonnet-20241022"

CLAUDE_MODEL=HAIKU35


def get_anthropic_api_key():
  try:
    with open(ANTHROPIC_KEY_FILE, 'r') as f:
      api_key = f.read().strip()
      return api_key
  except FileNotFoundError:
    print("Warning: 'api-key' file not found.")
    return ""


def get_claude_model():
  return CLAUDE_MODEL


def calculate_cost(usage):
    input_tokens = usage.cache_creation_input_tokens + usage.cache_read_input_tokens + usage.input_tokens
    output_tokens = usage.output_tokens
    model_prices = {
      SONNET35NEW: {
          "input_tokens": 3,
          "output_tokens": 15,
          "prompt_caching_write_tokens": 3.75,
          "prompt_caching_read_tokens": 0.3,
      },
      HAIKU3: {
          "input_tokens": 0.25,
          "output_tokens": 1.25,
          "prompt_caching_write_tokens": 0.3,
          "prompt_caching_read_tokens": 0.03,
      },
      HAIKU35: {
          "input_tokens": 0.8,
          "output_tokens": 4,
          "prompt_caching_write_tokens": 1,
          "prompt_caching_read_tokens": 0.08,
      },
    }

    current_model = get_claude_model()
    if current_model in model_prices:
        cost_input_tokens = usage.input_tokens * model_prices[current_model]['input_tokens'] / 10e6
        cost_output_tokens = usage.output_tokens * model_prices[current_model]['output_tokens'] / 10e6
        cost_prompt_caching_write_tokens = usage.cache_creation_input_tokens * model_prices[current_model]['prompt_caching_write_tokens'] / 10e6
        cost_prompt_caching_read_tokens = usage.cache_read_input_tokens * model_prices[current_model]['prompt_caching_read_tokens'] / 10e6

        cost = cost_input_tokens + cost_output_tokens + cost_prompt_caching_write_tokens + cost_prompt_caching_read_tokens

        formatted_cost = f"{cost * 100:.4f}"
        formatted_input_tokens_cost = f"{cost_input_tokens * 100:.4f}"
        formatted_output_tokens_cost = f"{cost_output_tokens * 100:.4f}"
        formatted_prompt_caching_write_tokens_cost = f"{cost_prompt_caching_write_tokens * 100:.4f}"
        formatted_prompt_caching_read_tokens_cost = f"{cost_prompt_caching_read_tokens * 100:.4f}"

        cost_summary = [
            (f"* Input tokens: {usage.input_tokens} ({usage.input_tokens}, {usage.cache_creation_input_tokens}, {usage.cache_read_input_tokens})"),
            (f"* Output tokens: {usage.output_tokens}"),
            (f"\nCost: {formatted_cost} ¢"),
            (f"  - Input tokens: {formatted_input_tokens_cost} ¢"),
            (f"  - Output tokens: {formatted_output_tokens_cost} ¢"),
            (f"  - Prompt caching write tokens: {formatted_prompt_caching_write_tokens_cost} ¢"),
            (f"  - Prompt caching read tokens: {formatted_prompt_caching_read_tokens_cost} ¢"),
        ]
        for line in cost_summary:
            print(line)
    else:
        print(f'No data how to calculate cost for model: {get_claude_model()}')
        return


def sent_to_claude(input_messages):
    try:
        client = anthropic.Anthropic(
            api_key = get_anthropic_api_key(),
        )
        message = client.messages.create(
            model = get_claude_model(),
            max_tokens = 1024,
            messages = input_messages
        )
    except anthropic.APIConnectionError as e:
        print('The server could not be reached')
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except anthropic.RateLimitError as e:
        print('A 429 status code was received; we should back off a bit.')
    except anthropic.APIStatusError as e:
        print('Another non-200-range status code was received')
        print(e.status_code)
        print(e.response)

    return message


def create_message_as_assistant(conversation, current_message, role):
    conversation.append({'role': role, 'content': current_message})
    return conversation


def chat_function():
    conversation = []
    while True:
        user_message = input("Enter your message (or 'exit' to quit): ")

        if user_message.lower() == 'exit':
            print('Exiting chat...')
            break

        print('\nYou: ', user_message)

        conversation = create_message_as_assistant(conversation, user_message, role = 'user')
        claude_message = sent_to_claude(conversation)
        claude_response = claude_message.content[0].text
        conversation = create_message_as_assistant(conversation, claude_response, role = 'assistant')
        print(f'{CLAUDE_MODEL}: ', claude_response)
        border = '-' * 80
        print(border)
        calculate_cost(claude_message.usage)
        print(border)
        print()

if __name__ == '__main__':
    chat_function()
