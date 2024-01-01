This is a python project which using ChatGPT API to determine to open the fan base on temperature.

useful tutorial link:
https://platform.openai.com/docs/assistants/tools/function-calling
https://cookbook.openai.com/examples/assistants_api_overview_python
https://community.openai.com/t/assistant-api-message-no-answer-only-question/534101/3

environment configuration:
Python 3.11
conda install requests
pip install paho-mqtt

version1_1 error:
{
    'error': {
        'message': "Expected tool outputs for call_ids ['call_SLVC6oRoltVMv3qbxqN8mvOy', 'call_xcDL9fuPVAJRDwkoTjv5r75A'], got ['call_SLVC6oRoltVMv3qbxqN8mvOy']",
        'type': 'invalid_request_error',
        'param': None,
        'code': None
    }
}

solution:
https://community.openai.com/t/expected-tool-output-for-wrong-call-id/560554

version1_2 error:
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
    run.status:  failed
    Messages
    user: The temperature is 77.1 (in Celsius).
    assistant: I've turned on the fan to ensure a comfortable temperature. If there's anything else you need, feel free to ask!
    user: The temperature is 68.7 (in Celsius).
    run.status:  in_progress
    run.status:  in_progress
    run.status:  in_progress
}