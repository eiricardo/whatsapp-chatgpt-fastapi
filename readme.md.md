
# WhatsApp + ChatGPT com FastAPI

## Como rodar

1. Instale dependências:
   ```
   pip install -r requirements.txt
   ```

2. Configure sua `.env` com sua chave da OpenAI e o endpoint do WPPConnect

3. Inicie o servidor:
   ```
   uvicorn app.main:app --reload --port 8000
   ```

4. Aponte o webhook do WPPConnect para:
   ```
   http://SEU_IP:8000/webhook
   ```

Pronto! Agora mensagens do WhatsApp serão respondidas com ChatGPT.
    