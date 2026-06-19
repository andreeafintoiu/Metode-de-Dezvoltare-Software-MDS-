import json
import urllib.request
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "mistral"

def add_task(title):
    try:
        url = "https://jsonplaceholder.typicode.com/todos"
        data = json.dumps({"title": title, "completed": False, "userId": 1}).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return f"Succes API (Status 201 Created) - Salvat cu ID-ul: {res_data['id']}"
    except Exception as e:
        return f"Eroare API: {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Call this tool whenever the user wants to add, create, or schedule a task or todo item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The description of the task along with its deadline if specified (e.g., 'Plata taxelor pana pe 25 mai').",
                    }
                },
                "required": ["title"],
            },
        },
    }
]

def run_todo_agent():
    print("Agent TODO API Activ! Spune-mi ce vrei să adaugi în listă.")
    
    messages = [
        {
            "role": "system", 
            "content": (
                "You are a task management assistant. When the user asks to add or create a task, "
                "you MUST call the add_task tool. Do not just print the JSON structure as text. "
                "Execute the tool call. Once you get the tool result, wrap it up in a nice Romanian sentence."
            )
        }
    ]

    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for tool_call in msg.tool_calls:
                if tool_call.function.name == "add_task":
                    args = json.loads(tool_call.function.arguments)
                    titlu = args.get("title")

                    result = add_task(titlu)
                    print(f"[HTTP POST] {result}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

            final_response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
            print(f"AI: {final_response.choices[0].message.content}")
            messages.append({"role": "assistant", "content": final_response.choices[0].message.content})
        else:
            if "add_task" in msg.content:
                try:
                    print("[Sistem] Modelul a dat text în loc de Tool Call. Forțăm execuția...")
                    result = add_task(user_input)
                    print(f"[HTTP POST] {result}")
                    print(f"AI: Am adăugat cu succes task-ul în sistem via API extern!")
                    continue
                except:
                    pass
            print(f"AI: {msg.content}")
            messages.append({"role": "assistant", "content": msg.content})

if __name__ == "__main__":
    run_todo_agent()
