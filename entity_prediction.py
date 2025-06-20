import requests
import json

def build_prompt(user_input):
    return f"""
You are an entity recognition assistant. Extract the following entities from the input text:
- Product (the item being searched for)
- Brand (if mentioned)
- Price (if a number like $10 or under 100 is mentioned)
- Color (if mentioned)

Respond in JSON format with keys "product", "brand", "price", and "color". Do not add any extra text. If an entity is not present in the user query, just give empty string "". Refer to sample example: {{"product":"sofa","brand":"Kraft","price":"200","color":""}}

Input: "{user_input}"
"""

def extract_entities_llama(user_input):
    prompt = build_prompt(user_input)
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    response_json = response.json()
    try:
        output = response_json['response']
        parsed = json.loads(output.strip().split("```json")[-1].split("```")[0])
        print(parsed)
        return parsed
    except Exception as e:
        print("⚠️ Failed to parse LLaMA response:", e)
        print("Raw response:", response_json)
        return {"product": "", "brand": "", "price": "", "color":""}
    
extract_entities_llama("bosch hammer")