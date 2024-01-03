# ChatGPT API Fan Control Project

## Description

This project utilizes the ChatGPT API to control a fan based on temperature readings which from simulation platform.
It's a Python-based solution integrating AI and IoT for smart temperature regulation.

## Installation and Configuration

### Prerequisites

Python 3.11

### Steps

Install required packages:
* `conda install requests`


* `pip install paho-mqtt`

## Usage

* `python OpenAI_API_beta.py`

or 

* `python OpenAI_API_alpha.hpy`

## Comparison between OpenAI_API_beta and OpenAI_API_alpha

OpenAI_API_beta.py using the Assistant API, while OpenAI_API_alpha using the Chat Completions API.

In our OpenAI_API_alpha.py, we realize that using the Chat Completions API to control a fan based on temperature readings which from simulation platform.

In our OpenAI_API_beta.py, we introduce a feature called "function calling" which allows the user to call a function in the assistant's code.
This feature is useful for IoT applications. In this project, we use function calling to control a fan based on temperature readings.
We believe that in the future, this feature will be widely used in IoT applications, not just for controlling a fan we use in this project, 
maybe also for controlling a light, a door, or even a car.

The most important thing is that the Assistant API introduces a new feature called "thread", which allows users to communicate with the assistant 
in a more natural way. For example, in the Chat Completions API, the user can only send one message at a time, and the assistant will only reply once.
But in the Assistant API, the user can send messages at multiple times, and the assistant will reply multiple times.

However, the Assistant API is still in beta, and it is not as stable as the Chat Completions API. Besides, we use the authentic API key in this project,
which means that the Assistant API is more expensive than the Chat Completions API, and the Assistant API has rate limits on the number of requests per minute and per day,
because OpenAI need rate limits to help protect against abuse/overuse of the API. So we can't use the Assistant API in a large scale application,
and we can't test too much data.

Despite this, we still think that the Assistant API has a more promising future in IoT applications. Threads is its strong advantage.
And in the future, OpenAI plan to release more OpenAI-built tools, and allow developer to provide their own tools on OpenAI's platform.

## Troubleshooting and Error Reports

### version1_1

#### error:

{
    'error': {
        `'message': "Expected tool outputs for call_ids ['call_SLVC6oRoltVMv3qbxqN8mvOy', 'call_xcDL9fuPVAJRDwkoTjv5r75A'], got ['call_SLVC6oRoltVMv3qbxqN8mvOy']"`,
        'type': 'invalid_request_error',
        'param': None,
        'code': None
    }
}

#### solution:

https://community.openai.com/t/expected-tool-output-for-wrong-call-id/560554

### version1_2

#### error:

{
    connected & return result_code: 0
    MQTT connected
    run.status:  in_progress
    run.status:  requires_action
    run.status:  in_progress
    run.status:  in_progress
    run.status:  completed
    Messages
    user: The temperature is 77.1 (in Celsius).
    assistant: I've turned on the fan to ensure a comfortable temperature. If there's anything else you need, feel free to ask!
    run.status:  in_progress
    run.status:  requires_action
    run.status:  in_progress
    run.status:  in_progress
    run.status:  in_progress
    run.status:  in_progress
    run.status:  in_progress
    run.status:  in_progress
    run.status:  in_progress
    `run.status:  failed`
    Messages
    user: The temperature is 77.1 (in Celsius).
    assistant: I've turned on the fan to ensure a comfortable temperature. If there's anything else you need, feel free to ask!
    user: The temperature is 68.7 (in Celsius).
    run.status:  in_progress
    run.status:  in_progress
    run.status:  in_progress
}

#### solution:

Sometimes the assistant will fail to run because of the rate limit. We need to wait for a while and try again.
So, we need to add a retry mechanism to the OpenAI_API_beta.py.
The former client_id '1111' has been occupied by the other's run, so we need to change the client_id to '111'.

## Useful Links
https://platform.openai.com/docs/assistants/tools/function-calling
https://cookbook.openai.com/examples/assistants_api_overview_python
https://community.openai.com/t/assistant-api-message-no-answer-only-question/534101/3