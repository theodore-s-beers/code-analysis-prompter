import os
import pathlib
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI


def chat_with_gpt(client: OpenAI, api_key: str, prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    response = ""

    if completion.usage:
        response += f"Prompt tokens: {completion.usage.prompt_tokens}\n"
        response += f"Completion tokens: {completion.usage.completion_tokens}\n"

    if completion.choices:
        response += f"Answer: {completion.choices[0].message.content}"

    if not response:
        raise RuntimeError("No response from GPT-4o mini")

    return response


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OSError("API key not found")

    client = OpenAI(api_key=api_key)

    paths = list(pathlib.Path("files/").rglob("*.py"))

    if not paths:
        raise RuntimeError("No Python files found")
    if len(paths) > 50:
        raise RuntimeError(f"Suspiciously large number of Python files: {len(paths)}")

    intro = "Hello. I'm checking a bunch of Python modules for code that runs globally, which I generally do not want. Could you please tell me, as concisely as possible, if you notice any top-level code that will execute on import in the following Python module?\n\n"

    for path in paths:
        try:
            with open(path, "r") as file:
                print("----------------")
                print(f"Checking {path}...")

                full_content = file.read()

                line_count = full_content.count("\n")
                if line_count < 10 or line_count > 500:
                    print(f"Skipping {path} due to line count: {line_count}")
                    continue

                print("Beginning chat with GPT-4o mini...")
                response = chat_with_gpt(client, api_key, intro + full_content)
                print(response)

                time.sleep(3)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
