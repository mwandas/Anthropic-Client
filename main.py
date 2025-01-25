import anthropic
import argparse


ANTHROPIC_KEY_FILE = 'main-key'

MODEL_CONFIG = {
    'haiku3': {
        'id': 'claude-3-haiku-20240307',
        'name': 'Haiku 3',
        'pricing': {
            'input tokens': 0.25,
            'output tokens': 1.25,
            'prompt caching write tokens': 0.3,
            'prompt caching read tokens': 0.03,
        }
    },
    'haiku3.5': {
        'id': 'claude-3-5-haiku-20241022',
        'name': 'Haiku 3.5',
        'pricing': {
            'input tokens': 0.8,
            'output tokens': 4,
            'prompt caching write tokens': 1,
            'prompt caching read tokens': 0.08,
        }
    },
    'sonnet3.5': {
        'id': 'claude-3-5-sonnet-20241022',
        'name': 'Sonnet 3.5 (New)',
        'pricing': {
            'input tokens': 3,
            'output tokens': 15,
            'prompt caching write tokens': 3.75,
            'prompt caching read tokens': 0.3,
        }
    }
}


def get_anthropic_api_key():
  try:
    with open(ANTHROPIC_KEY_FILE, 'r') as f:
      api_key = f.read().strip()
      return api_key
  except FileNotFoundError:
    print("Warning: 'api-key' file not found.")
    return ""


def calculate_cost(model, usage):
    if not model.get('pricing'):
        print(f'No pricing data available for model: {model["id"]}')
        return

    pricing = model['pricing']

    cost_input_tokens = usage.input_tokens * pricing['input tokens'] / 1e6
    cost_output_tokens = usage.output_tokens * pricing['output tokens'] / 1e6
    cost_prompt_caching_write_tokens = usage.cache_creation_input_tokens * pricing['prompt caching write tokens'] / 1e6
    cost_prompt_caching_read_tokens = usage.cache_read_input_tokens * pricing['prompt caching read tokens'] / 1e6

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


def sent_to_claude(model, input_messages):
    try:
        client = anthropic.Anthropic(
            api_key = get_anthropic_api_key(),
        )
        message = client.messages.create(
            model = model['id'],
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


def chat_loop(model):
    conversation = []
    while True:
        user_message = input("Enter your message (or 'exit' to quit): ")

        if user_message.lower() == 'exit':
            print('Exiting chat...')
            break

        print('\nYou: ', user_message)

        conversation = create_message_as_assistant(conversation, user_message, role = 'user')
        claude_message = sent_to_claude(model, conversation)
        claude_response = claude_message.content[0].text
        conversation = create_message_as_assistant(conversation, claude_response, role = 'assistant')
        print(f'{model["name"]}:', claude_response)
        border = '-' * 80
        print(border)
        calculate_cost(model, claude_message.usage)
        print(border)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Chat with Claude.',
                                     formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument(
        '--model',
        choices=MODEL_CONFIG.keys(),
        default="haiku3.5",
        help=f'The model to use.\n  Options:\n' + '\n'.join(
            [f'   - {key}: {value["name"]}'
            for key, value in MODEL_CONFIG.items()]
        ) + '\nDefaults to haiku3.5.',
    )

    args = parser.parse_args()

    chat_loop(MODEL_CONFIG[args.model])
