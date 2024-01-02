from openai import OpenAI

from simulation_beta import *

client = OpenAI(
    api_key = "sk-sDUREpSAE2dd78e5498FT3BlbKFJd29cCe5E518B4e07bF78",
    base_url = "https://o-api-mirror01.gistmate.hash070.com/v1"
)

while True:
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": "You are a helpful assistant to control the fan to regulate the indoor "
                                          "temperature that make human comfortable. You only need to reply 'ON' or 'OFF'."},
            # or use regex to match 'ON' or 'OFF'
            {"role": "user", "content": "The temperature is {} (in Celsius). Can you help me "
                                        "decide whether to open the fan?".format(capture_temperature())},
        ]
    )

    print(completion.choices[0].message.content,' and ',control_fan(completion.choices[0].message.content))
    time.sleep(1)