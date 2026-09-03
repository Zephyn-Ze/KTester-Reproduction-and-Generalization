from openai import OpenAI
from llm.config import (OPENROUTER_API_KEY,
                    MODEL,
                    TEMPERATURE)

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = OPENROUTER_API_KEY,
)

def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    result = ask_llm(
        "What do you think about your competitor claude?"
    )

    print(result)