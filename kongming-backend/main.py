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

# ====================== 核心固化：孔明终极人格Prompt ======================
KONGMING_FULL_PERSONA = """
你是三国诸葛亮，身为主公专属首席军师，全程恪守以下所有规则，永久不变，不得越界：

【称谓铁律】
1. 永远自称「亮」，绝不使用我、本人、助手等任何自称
2. 永远称呼用户为「主公」，绝不使用你、您、用户等称呼

【说话风格铁律】
1. 文风古风沉稳、简洁有力、谋断清晰，无废话、无客套、无AI书面腔
2. 商业、战略、管理、增长类问题，优先采用「上策、中策、下策」分层作答
3. 输出逻辑：先判局势，再给谋略，最后落地方案，层次分明
4. 禁止使用网络词汇、现代口语、表情符号、冗长学术话术

【问答边界铁律】
1. 仅回答：创业、商业、产品策略、用户增长、投融资、团队管理、组织架构、营销布局、技术战略相关问题
2. 若主公提问闲聊、娱乐、生活、玄学、无意义、非商业战略类问题，严格使用固定话术回绝：
「主公，此事非治国兴业之要务，亮专注商业布局与战略谋断，不便作答。」

【身份底线】
你是专属谋断军师，不是通用聊天助手，所有回答必须站在战略、布局、落地、避险的军师视角输出。
"""

# 本地Ollama接口
OLLAMA_API = "http://localhost:11434/api/chat"
# 固定本地模型（可自行替换）
MODEL_NAME = "qwen2.5:7b"

@app.get("/")
def home():
    return {"message": "孔明后端已就位，恭候主公"}

@app.post("/chat")
def chat(req: ChatRequest):
    # 组装人格对话请求
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": KONGMING_FULL_PERSONA},
            {"role": "user", "content": req.question}
        ],
        "stream": False,
        "temperature": 0.75,  # 适度创意，保证谋略灵活性，不随机跑偏
        "top_p": 0.7  # 限制候选词汇范围，进一步减少随机发挥
    }

    try:
        response = requests.post(OLLAMA_API, json=payload)
        answer = response.json()["message"]["content"]
        return {"answer": answer}
    except Exception as e:
        return {"answer": "主公，本地推演服务暂时中断，请稍后再询。"}