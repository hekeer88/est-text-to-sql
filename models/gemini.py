import json.decoder

from google import genai
from google.genai import types
from utils.enums import LLM
import time

client = None

def init_gemini(GEMINI_API_KEY):
    global client
    client = genai.Client(api_key=GEMINI_API_KEY)


def ask_completion(model, batch, temperature):
    response = client.models.generate_content(
        model=model,
        contents=batch,
        # temperature=temperature,
        # max_tokens=200,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0,
        # stop=[";"]
    )
    response_clean = [choice.text for choice in response.choices]
    return dict(
        response=response_clean,
        **response["usage"]
    )


def ask_chat(model, messages: list, temperature, n):
    chat = client.chats.create(model=model)

    config = types.GenerateContentConfig(
        candidate_count=n,
        max_output_tokens=300,
        temperature=temperature,
        # top_p=0.1,
        # top_k=1
    )

    user_message = messages[-1]["content"]
    attempts = 0
    max_attempts = 11

    # response = chat.send_message(user_message, config)

    while attempts < max_attempts:
        response = chat.send_message(user_message, config)
        print("Raw Gemini response:", response)

        if not response or not response.candidates:
            attempts += 1
            continue

        try:
            response_clean = [
                c.content.parts[0].text
                for c in response.candidates[:n]
                if c.content and c.content.parts and c.finish_reason != "RECITATION"
            ]
            if response_clean:
                break
        except Exception:
            pass

        attempts += 1
        time.sleep(0.5)


    if not response_clean:
        raise ValueError("No valid response after retries.")

    if n == 1:
        response_clean = response_clean[0]

    return dict(
        response=response_clean,
        total_tokens=0
    )


def ask_llm(model: str, batch: list, temperature: float, n:int):
    n_repeat = 0
    sleep_time = 1
    max_sleep = 64
    # response = {"response": [""], "usage": {"total_tokens": 0}}

    while True:
        try:
            if model in LLM.TASK_CHAT:
                # batch size must be 1
                assert len(batch) == 1, "batch must be 1 in this mode"
                messages = [{"role": "user", "content": batch[0]}]
                response = ask_chat(model, messages, temperature, n)
                response['response'] = [response['response']]
                time.sleep(0.5)
            break
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


