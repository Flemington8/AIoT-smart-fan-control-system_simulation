# Notice how all of these API calls are asynchronous operations;
# this means we actually get async behavior in our code without the use of async libraries!

# Threads can be used to create multiple conversations with the same assistant.

import time
import json
import simulation
from openai import OpenAI

function_json = {
    "name": "capture_temperature",
    "description": "Returns the temperature data (in Celsius) captured by temperature sensor."
    # "parameters": {
    #     "type": "object",
    #     "properties": {
    #         "temperature": {"type": "string"},
    #     },
    #     "required": ["temperature"],
    # },
}

client = OpenAI(
    api_key = "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"
)

assistant = client.beta.assistants.create(
    name = "Fan Control Assistant",
    instructions = "You are a helpful assistant to control the fan to regulate the indoor temperature."
                   "You only need to reply 'ON' or 'OFF'.",
    tools = [{"type": "code_interpreter"},
             {"type": "retrieval"},
             {"type": "function", "function": function_json}],
    model = "gpt-3.5-turbo-1106"
)

FAN_CONTROL_ASSISTANT_ID = assistant.id


def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(FAN_CONTROL_ASSISTANT_ID, thread, user_input)
    return thread, run


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id = thread.id, role = "user", content = user_message
    )
    return client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant_id,
    )


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id = thread.id,
            run_id = run.id,
        )  # retrieve the run status
        time.sleep(0.5)
    return run


def pretty_print(messages):
    print("# Messages")
    for message in messages:
        print(f"{message.role}: {message.content[0].text.value}")
    print()


thread, run = create_thread_and_run("Get the temperature from sensor, and decide whether to turn on fan or turn off?"
                                    "You only need to reply 'ON' or 'OFF'.")
run = wait_on_run(run, thread)

tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread.id,
    run_id=run.id,
    tool_outputs=[
        {
            "tool_call_id": tool_call.id,
            "output": "20",
        }
    ],
)

run = wait_on_run(run, thread)

messages = client.beta.threads.messages.list(
    thread_id = thread.id,
    order = "asc"
)

pretty_print(messages)
