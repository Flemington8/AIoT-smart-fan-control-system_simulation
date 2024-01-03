# Notice how all of these API calls are asynchronous operations;
# this means we actually get async behavior in our code without the use of async libraries!

# Threads can be used to create multiple conversations with the same assistant.

from openai import OpenAI

from simulation_beta import *


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
        print('run.status: ', run.status)
    return run


def pretty_print(messages):
    print("# Messages")
    count = 0
    for message in messages:
        if message.role == "user":
            count += 1
            print('* conversation {}'.format(count))
        print(f"{message.role}: {message.content[0].text.value}")


function_json = {
    "name": "control_fan",
    "description": "When temperature is high, key_status will be 'ON', so set the fan on,"
                   "when temperature is low, key_status will be 'OFF', so set the fan off.",
    "parameters": {
        "type": "object",
        "properties": {
            "key_status": {"type": "string",
                           "description": "The status of fan, only ON or OFF is allowed."}
        },
        "required": ["control_factor"]
    }
}

client = OpenAI(
    api_key = "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"
    # "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"#"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"
)

assistant = client.beta.assistants.create(
    name = "Fan Control Assistant",
    instructions = "You are a smart home assistant,"
                   "and you can control the fan based on the current temperature to make the homeowner feel comfortable.",
    tools = [{"type": "code_interpreter"},
             {"type": "retrieval"},
             {"type": "function", "function": function_json}],
    model = "gpt-3.5-turbo-1106"
)

FAN_CONTROL_ASSISTANT_ID = assistant.id

thread, run = create_thread_and_run("The temperature is {} (in Celsius).".format(capture_temperature()))
run = wait_on_run(run, thread)

while True:
    # time.sleep(20)  # make sure run.status won't be 'failed'
    try:
        tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
        name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # The Assistants API will pause execution during a Run when it invokes functions,
        # and you can supply the results of the function call back to continue the Run execution.
        if name == "control_fan":  # In the future, we will support more functions.
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id = thread.id,
                run_id = run.id,
                tool_outputs = [
                    {
                        "tool_call_id": tool_call.id,
                        "output": control_fan(arguments["key_status"]),
                    }
                ],
            )

            run = wait_on_run(run, thread)

            messages = client.beta.threads.messages.list(
                thread_id = thread.id,
                order = "asc"
            )
            pretty_print(messages)
    except Exception as e:
        print('Exception: ', e)
    finally:
        print('\nwait for 20 seconds')
        time.sleep(20)  # make sure run.status won't be 'failed', because the rate limit is 3 requests per minute.
        # Add a new message to the thread
        run = submit_message(FAN_CONTROL_ASSISTANT_ID, thread, "The temperature is {} (in Celsius).".format(capture_temperature()))
        run = wait_on_run(run, thread)
