
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# === API KEYS ===
GEMINI_API_KEY = "AIzaSyDiKXYPygewEHOXqvEaPVq0siwy4_umwO8"
COHERE_API_KEY = "kIhXqy0XihtfL4TWmYNK4K8m22pKSbmYdhFMUHsK"
MISTRAL_API_KEY = "SkQDtwJiN1s9WYZacipPvMaxW6NTmJlW"

# === ENDPOINTS ===
@app.post("/aggregate")
async def aggregate(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    responses = {}

    # === Gemini (Google) ===
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    gemini_payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    gemini_res = requests.post(gemini_url, json=gemini_payload)
    try:
        gemini_text = gemini_res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        gemini_text = "Error from Gemini"
    responses["gemini"] = gemini_text

    # === Cohere ===
    cohere_url = "https://api.cohere.ai/v1/chat"
    cohere_headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    cohere_payload = {
        "message": prompt,
        "model": "command-r",
    }
    cohere_res = requests.post(cohere_url, headers=cohere_headers, json=cohere_payload)
    try:
        cohere_text = cohere_res.json()['text']
    except:
        cohere_text = "Error from Cohere"
    responses["cohere"] = cohere_text

    # === Mistral (via OpenRouter) ===
    mistral_url = "https://openrouter.ai/api/v1/chat/completions"
    mistral_headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    mistral_payload = {
        "model": "mistral/mistral-medium",
        "messages": [{"role": "user", "content": prompt}]
    }
    mistral_res = requests.post(mistral_url, headers=mistral_headers, json=mistral_payload)
    try:
        mistral_text = mistral_res.json()['choices'][0]['message']['content']
    except:
        mistral_text = "Error from Mistral"
    responses["mistral"] = mistral_text

    return {"prompt": prompt, "responses": responses}
