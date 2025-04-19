
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WPP_API_URL = os.getenv("WPP_API_URL")  # ex: http://localhost:21465

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("body")
    phone = data.get("message", {}).get("from")

    if not message or not phone:
        return {"status": "ignored"}

    # Envia mensagem para o ChatGPT
    chat_response = await ask_chatgpt(message)

    # Envia resposta para o WhatsApp
    await send_whatsapp_message(phone, chat_response)

    return {"status": "ok", "response": chat_response}

async def ask_chatgpt(message: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    json_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}],
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
    data = response.json()
    return data["choices"][0]["message"]["content"]

async def send_whatsapp_message(phone: str, message: str):
    url = f"{WPP_API_URL}/api/sendText"
    payload = {"phone": phone, "message": message}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)
    