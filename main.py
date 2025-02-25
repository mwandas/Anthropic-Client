import anthropic
import argparse
import copy
import time


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
    },
    'sonnet3.7': {
        'id': 'claude-3-7-sonnet-20250219',
        'name': 'Sonnet 3.7',
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

    cost_summary = {
        "total": cost,
        "input": cost_input_tokens,
        "output": cost_output_tokens,
        "write": cost_prompt_caching_write_tokens,
        "read": cost_prompt_caching_read_tokens,
        "formatted_total": formatted_cost,
        "formatted_input": formatted_input_tokens_cost,
        "formatted_output": formatted_output_tokens_cost,
        "formatted_write": formatted_prompt_caching_write_tokens_cost,
        "formatted_read": formatted_prompt_caching_read_tokens_cost,
        "input_tokens": usage.input_tokens,
        "cache_creation_input_tokens": usage.cache_creation_input_tokens,
        "cache_read_input_tokens": usage.cache_read_input_tokens,
        "output_tokens": usage.output_tokens
        }
    return cost_summary


def sent_to_claude(model, input_messages, cache_file):
    try:
        client = anthropic.Anthropic(
            api_key = get_anthropic_api_key(),
        )

        system_messages = []
        if cache_file:
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_content = f.read()
                    system_messages.append({
                        'type': 'text',
                        'text': cache_content,
                        'cache_control': {'type': 'ephemeral'}
                    })
            except FileNotFoundError:
                print(f"Warning: Cache file '{cache_file}' not found.")

        input_messages[-1]['content'][0]['cache_control'] = {'type': 'ephemeral'}
        message = client.messages.create(
            model = model['id'],
            max_tokens = 1024,
            system = system_messages,
            messages = input_messages
        )
    except anthropic.RateLimitError as e: # 429 Error
        print('Your account has hit a rate limit.')
        print(e)
        time.sleep(5)
        return sent_to_claude(model, input_messages, cache_file)
    except anthropic.InternalServerError as e:
        print('Internal server error. Please try again later.')
        print(e)
        return sent_to_claude(model, input_messages, cache_file)
    except anthropic.APIStatusError as e:  # Catch-all for other error when an API response has a status code of 4xx or 5xx.
        print('Another non-200-range status code was received')
        print(f'Status Code: {e.status_code}')
        print(f'Response: {e.response}')
        print(e)
        time.sleep(5)
        return sent_to_claude(model, input_messages, cache_file)

    return message


def create_message_as_assistant(conversation, current_message, role):
    conversation.append({'role': role,
                         'content': [{ 'type': 'text',
                                       'text': current_message,
                                     }]
                        })
    return conversation


def chat_loop(model, cache_file):
    conversation = []
    total_cost = {
        "total": 0,
        "input": 0,
        "output": 0,
        "write": 0,
        "read": 0
    }
    while True:
        user_message = input("Enter your message (or 'exit' to quit): ")

        if user_message.lower() == 'exit':
            print('Exiting chat...')
            break

        print('\nYou: ', user_message)

        conversation = create_message_as_assistant(conversation, user_message, role = 'user')
        claude_message = sent_to_claude(model, copy.deepcopy(conversation), cache_file)
        claude_response = claude_message.content[0].text
        conversation = create_message_as_assistant(conversation, claude_response, role = 'assistant')
        print(f'{model["name"]}:', claude_response)
        border = '-' * 80
        print(border)
        cost_summary = calculate_cost(model, claude_message.usage)
        if cost_summary:
            total_cost["total"] += cost_summary["total"]
            total_cost["input"] += cost_summary["input"]
            total_cost["output"] += cost_summary["output"]
            total_cost["write"] += cost_summary["write"]
            total_cost["read"] += cost_summary["read"]

            print(f"* Input tokens: {cost_summary['input_tokens']} ({cost_summary['input_tokens']}, {cost_summary['cache_creation_input_tokens']}, {cost_summary['cache_read_input_tokens']})")
            print(f"* Output tokens: {cost_summary['output_tokens']}")
            print(f"\nCost: {cost_summary['formatted_total']} ¢")
            print(f"  - Input tokens: {cost_summary['formatted_input']} ¢")
            print(f"  - Output tokens: {cost_summary['formatted_output']} ¢")
            print(f"  - Prompt caching write tokens: {cost_summary['formatted_write']} ¢")
            print(f"  - Prompt caching read tokens: {cost_summary['formatted_read']} ¢")


            print(f"\nTotal cost so far: {total_cost['total'] * 100:.4f} ¢")
            print(f"  - Input tokens: {total_cost['input'] * 100:.4f} ¢")
            print(f"  - Output tokens: {total_cost['output'] * 100:.4f} ¢")
            print(f"  - Prompt caching write tokens: {total_cost['write'] * 100:.4f} ¢")
            print(f"  - Prompt caching read tokens: {total_cost['read'] * 100:.4f} ¢")

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

    parser.add_argument(
        '--cache',
        dest = 'cache_file',
        help = 'Path to the cache text file.',
    )

    args = parser.parse_args()

    chat_loop(MODEL_CONFIG[args.model], args.cache_file)
