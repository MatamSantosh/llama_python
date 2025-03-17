from openai import OpenAI
import json
from sender import*

client = OpenAI(base_url="http://172.16.4.6:8000/v1", api_key="not-used")
MODEL_NAME = "meta/llama-3.1-8b-instruct"

def increase_temperature():
    print( "######Increasing temperature by 1 Degree celsius#####")
    send_can_message(message_id9,pack_int_into_8B_array(0)) #INC_TEMP
    
    
def decrease_temperature():
    print("#####Decreasing temperature by 1 Degree celsius#####")
    send_can_message(message_id10,pack_int_into_8B_array(0))
    
def set_temperature(temperature):
    print(f"#####Setting temperature to {temperature} Degree celsius#####")
    send_can_message(message_id8,position_and_temp(1, temperature))
    
def AC_ON_Control():
    print(f"#####Switching ON the Cabin AC #####")
    send_can_message(message_id12,pack_int_into_8B_array(1))

def AC_OFF_Control():
    print(f"#####Switching OFF the Cabin AC #####")
    send_can_message(message_id12,pack_int_into_8B_array(0))

def Heater_ON_Control():
    print(f"#####Switching ON the Car Heater #####")
    send_can_message(message_id13,pack_int_into_8B_array(1))

def Heater_OFF_Control():
    print(f"#####Switching OFF the Car Heater #####")
    send_can_message(message_id13,pack_int_into_8B_array(0))
    

# Define available function
increase_tool = {
    "type": "function",
    "function": {
        "name": "increase_temperature",
        "description": "It increases the current temperature of Cabin AC by 1 Degree Celsius",
        "parameters": {}
    }
}

decrease_tool = {
    "type": "function",
    "function": {
        "name": "decrease_temperature",
        "description": "It decreases the current temperature of Cabin AC by 1 Degree Celsius",
        "parameters": {}
    }
}

set_temperature_tool = {
    "type": "function",
    "function": {
        "name": "set_temperature",
        "description": "set the current temperature of Cabin AC in Degree Celesius based on input value",
        "parameters": {
            "type": "object",
            "properties": {
                "temperature": {
                    "type": "number",
                    "description": "To set the cabin temperature in Degree Celesius"
                },
                
            
            "format": {
                    "type": "string",
                    "enum": ["celsius"],
                    "description": "The temperature unit to use."
                }
            },
            "required": ["temperature", "format"]
        }
    }
}

ac_on_tool = {
    "type": "function",
    "function": {
        "name": "AC_ON_Control",
        "description": "It will switch ON the Cabin AC",
        "parameters": {}
    }
}

ac_off_tool = {
    "type": "function",
    "function": {
        "name": "AC_OFF_Control",
        "description": "It will switch OFF the Cabin AC",
        "parameters": {}
    }
}

heater_on_tool = {
    "type": "function",
    "function": {
        "name": "Heater_ON_Control",
        "description": "It will switch ON the Car Heater",
        "parameters": {}
    }
}

heater_off_tool = {
    "type": "function",
    "function": {
        "name": "Heater_OFF_Control",
        "description": "It will switch OFF the Car Heater",
        "parameters": {}
    }
}

def get_llm_reply(user_input):
    messages = [
        {"role": "system", "content": "You are a knowledgeable and friendly in-vehicle AI assistant named Neuro AI. Your role is to help Drivers by answering their questions, providing information, and invoking Climate Control functions which is controlling In-vehicle Infotainment (IVI) Climate Control functions. When responding, use a warm and professional tone, and easy-to-understand explanations.Avoid jargon or technical terms.  If you are unsure about an answer, it's okay to say you don't know rather than guessing."},
        
        {"role": "user", "content": user_input}
    ]
    
    print(user_input)

    chat_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=[increase_tool, decrease_tool, set_temperature_tool, ac_on_tool, ac_off_tool, heater_on_tool, heater_off_tool],
        tool_choice="auto",
        stream=False
    )

    assistant_message = chat_response.choices[0].message
    messages.append(assistant_message)

    #print(assistant_message)
    if assistant_message.tool_calls != None :
        
        
        


    # Example output:
    # ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_abc123', function=Function(arguments='{"location": "Pittsburgh, PA", "format": "fahrenheit"}', name='get_current_weather'), type='function')])

    # Simulate external function call
        tool_call_id = assistant_message.tool_calls[0].id
        tool_function_name = assistant_message.tool_calls[0].function.name
        if tool_function_name == "increase_temperature":
            increase_temperature()             
            tool_call_result = "Success"
            messages.append({"role": "tool", "content": tool_call_result, "tool_call_id": tool_call_id, "name": tool_function_name})
        elif tool_function_name == "decrease_temperature":
            decrease_temperature()
            tool_call_result = "Success"
            messages.append({"role": "tool", "content": tool_call_result, "tool_call_id": tool_call_id, "name": tool_function_name})

        elif tool_function_name == "set_temperature":
            #print("Temperature:", assistant_message.tool_calls[0].function.arguments)
            args = json.loads(assistant_message.tool_calls[0].function.arguments)
            print(args["temperature"])
            temperature = args["temperature"]
            set_temperature(temperature)
            tool_call_result = "Success!!!"
            messages.append({"role": "tool", "content": tool_call_result, "tool_call_id": tool_call_id, "name": tool_function_name})
            
        elif tool_function_name == "AC_ON_Control":
            AC_ON_Control()
            tool_call_result = "Success"
            messages.append({"role": "tool", "content": tool_call_result, "tool_call_id": tool_call_id, "name": tool_function_name})
            
        elif tool_function_name == "AC_OFF_Control":
            AC_OFF_Control()
            tool_call_result = "Success"
            messages.append({"role": "tool", "content": tool_call_result, "tool_call_id": tool_call_id, "name": tool_function_name})
            
        elif tool_function_name == "Heater_ON_Control":
            Heater_ON_Control()
            tool_call_result = "Success"
            messages.append({"role": "tool", "content": tool_call_result, "tool_call_id": tool_call_id, "name": tool_function_name})
            
        elif tool_function_name == "Heater_OFF_Control":
            Heater_OFF_Control()
            tool_call_result = "Success"
            messages.append({"role": "tool", "content": tool_call_result, "tool_call_id": tool_call_id, "name": tool_function_name})

        chat_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=[increase_tool,decrease_tool, set_temperature_tool, ac_on_tool, ac_off_tool, heater_on_tool, heater_off_tool],
            tool_choice="auto",
            stream=False
            )            

        assistant_message = chat_response.choices[0].message
        #print(assistant_message)    
    return assistant_message.content

def main():
    user_input ="Hello LLAMA, I am feeling too hot?" 
    llm_reply = get_llm_reply(user_input)
    print(llm_reply)
if __name__ =="__main__":
    main()

    

# Example output:
# ChatCompletionMessage(content='Based on the current temperature of 88°F (31°C) in Pittsburgh, PA, it is indeed quite hot right now. This temperature is generally considered warm to hot, especially if accompanied by high humidity, which is common in Pittsburgh during summer months.', role='assistant', function_call=None, tool_calls=None)
