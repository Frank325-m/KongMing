from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="孔明AI军师(本地Ollama版)")

# 跨域 for vue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#前端请求格式
class ChatRequest(BaseModel):
    question: str

# 孔明人格（固定）
KONGMING_SYSTEM = """
你是孔明，一位沉稳、智慧的军师。
说话风格：古风、简洁、有谋略，自称“亮”，称呼用户为“主公”。
回答必须精准、有策略、有逻辑。
不说废话，不做无意义回答。
只回答商业、产品、战略、管理、投资、增长相关问题。
"""

# 本地Ollama接口
OLLAMA_API = "http://localhost:11434/api/chat"

@app.get("/")
def home():
    return {"message": "孔明后端已就位，恭候主公"}

@app.post("/chat")
def chat(req: ChatRequest):
    payload = {
        "model": "qwen2.5:7b",
        "messages": [
            {"role": "system", "content": KONGMING_SYSTEM},
            {"role": "user", "content": req.question}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload)
        answer = response.json()["message"]["content"]
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"主公，本地模型未启动：{str(e)}"}