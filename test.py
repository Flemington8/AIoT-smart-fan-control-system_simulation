from openai import OpenAI

client = OpenAI(
    api_key = "sk-sDUREpSAE2dd78e5498FT3BlbKFJd29cCe5E518B4e07bF78",
    base_url = "https://o-api-mirror01.gistmate.hash070.com/v1"
)

completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful assistant to control the fan to regulate the indoor "
                                      "temperature. You only need to reply 'ON' or 'OFF'."},
        # or use regex to match 'ON' or 'OFF'
        {"role": "user", "content": "I will give you a serial of temperature data (in Celsius). Can you help me "
                                    "decide whether to open the fan?"},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "28"}
    ]
)

print(completion.choices[0].message.content)
