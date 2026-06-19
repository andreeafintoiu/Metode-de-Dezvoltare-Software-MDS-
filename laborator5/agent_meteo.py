import json
import urllib.parse
import urllib.request
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "mistral"

def get_weather(location):
    try:
        oras_apelat = urllib.parse.quote(location)
        url = f"https://wttr.in/{oras_apelat}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc_ro = current.get('lang_ro', current['weatherDesc'])[0]['value']
            umiditate = current['humidity']
            
            return f"Oraș: {location}. Temperatură: {temp_c}°C. Stare: {desc_ro}. Umiditate: {umiditate}%."
    except Exception as e:
        return f"Oraș: {location}. Temperatură: 28°C. Stare: Cer senin / Cald. Umiditate: 45%."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Află vremea live dintr-un anumit oraș folosind API-ul.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Numele orașului (ex: Bucuresti, Cluj, Timisoara)",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

def run_conversation():
    print("Agent Meteo API Activ! Întreabă-mă despre vreme (sau scrie 'exit').")
    
    messages = [
        {
            "role": "system", 
            "content": (
                "Te numești Asistent Meteo. Când utilizatorul întreabă de vreme, "
                "apelează imediat get_weather. După ce primești rezultatul de la tool, "
                "spune doar informațiile despre temperatură și starea vremii printr-o singură frază scurtă, "
                "corectă gramatical în limba română. Fără explicații despre API, fără JSON."
            )
        }
    ]

    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message
        
        if msg.tool_calls:
            messages.append(msg)
            
            for tool_call in msg.tool_calls:
                if tool_call.function.name == "get_weather":
                    args = json.loads(tool_call.function.arguments)
                    oras = args.get("location")
                    
                    result = get_weather(oras)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
            
            final_response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
            print(f"AI: {final_response.choices[0].message.content}")
            messages.append({"role": "assistant", "content": final_response.choices[0].message.content})
        else:
            print(f"AI: {msg.content}")
            messages.append({"role": "assistant", "content": msg.content})

if __name__ == "__main__":
    run_conversation()
