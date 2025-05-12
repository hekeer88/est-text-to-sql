import json.decoder
import random

from openai import OpenAI
from utils.enums import LLM
import time
from openai._exceptions import RateLimitError

client = None


def init_chatgpt(OPENAI_API_KEY):
    global client
    client = OpenAI(api_key=OPENAI_API_KEY)


def ask_chat(model, messages: list, temperature, n):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=300,
        n=n
    )

    print(response)
    response_clean = [choice.message.content for choice in response.choices]
    if n == 1:
        response_clean = response_clean[0]
    return dict(
        response=response_clean,
        total_tokens=response.usage.total_tokens
    )


def ask_llm(model: str, batch: list, temperature: float, n:int):
    n_repeat = 0
    sleep_time = 1
    max_sleep = 64

    while True:
        try:
            if model in LLM.TASK_CHAT:
                assert len(batch) == 1, "batch must be 1 in this mode"
                messages = [{"role": "user", "content": batch[0]}]
                response = ask_chat(model, messages, temperature, n)
                response['response'] = [response['response']]
                time.sleep(0.5)
            break
        except RateLimitError:
            time.sleep(sleep_time + random.uniform(0, 1))
            sleep_time = min(sleep_time * 2, max_sleep)
            n_repeat += 1
            print(f"Repeat for the {n_repeat} times for RateLimitError", end="\n")
            time.sleep(3)
            continue
        except json.decoder.JSONDecodeError:
            n_repeat += 1
            print(f"Repeat for the {n_repeat} times for JSONDecodeError", end="\n")
            time.sleep(1)
            continue
        except Exception as e:
            response = {"response": [""], "usage": {"total_tokens": 0}}
            n_repeat += 1
            print(f"Repeat for the {n_repeat} times for exception: {e}", end="\n")
            time.sleep(min(sleep_time * 2, max_sleep))
            continue

    return response
