import openai
from openai import OpenAI, RateLimitError, Timeout, APIError, APIConnectionError, OpenAIError

openai.api_key = "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"
try:
    # Use the updated ChatCompletion.create method
    client = OpenAI(
        api_key=openai.api_key,  # This is the default and can be omitted
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "HELLO WORLD"},
                    
                ],
            }
        ],
    )
    print(response)  # Output the generated message
except APIConnectionError:
    print("Invalid API key. Please check your key.")
except OpenAIError as e:
    print(f"An OpenAI API error occurred: {e}")