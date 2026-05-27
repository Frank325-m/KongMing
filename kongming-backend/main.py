from pyexpat import model

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

# app = FastAPI(title="孔明AI军师(本地Ollama版)")
app = FastAPI(title="孔明AI军师(线上版)")

# 全局跨域配置 - 针对SSE优化
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 明确指定前端地址
    allow_credentials=True,
    allow_methods=["*"],  # SSE需要GET和OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],  # 暴露所有头给前端
    max_age=86400  # 预检请求缓存时间
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

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

MODEL_NAME = os.getenv("LLM_MODEL_NAME")
# 最优沉稳参数 - 转换为浮点数
TEMP = float(os.getenv("TEMPERATURE", "0.45"))
TOP_P = float(os.getenv("TOP_P", "0.7"))

@app.get("/")
def home():
    return {"message": "孔明后端已就位，恭候主公"}

# 处理OPTIONS预检请求
@app.options("/chat-stream")
async def options_chat_stream():
    from fastapi.responses import JSONResponse
    response = JSONResponse(content={})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "86400"  # 24小时
    return response

# 流式对话接口（新版核心）- 支持GET和POST方法
@app.get("/chat-stream")
@app.post("/chat-stream")
async def chat_stream(request: Request, question: str = None):
    # 处理GET或POST请求（从查询参数获取question）
    if not question:
        # 如果是POST请求，尝试从请求体获取
        try:
            body = await request.body()
            if body:
                data = await request.json()
                question = data.get("question")
        except:
            pass
    
    if not question:
        return {"error": "问题不能为空"}
    
    messages = [
        {"role": "system", "content": KONGMING_FULL_PERSONA},
        {"role": "user", "content": question}
    ]

    def stream_generator():
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            temperature=TEMP,
            top_p=TOP_P,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield f"{chunk.choices[0].delta.content}\n\n"
        yield "[DONE]\n\n"
    
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }

    return StreamingResponse(stream_generator(), headers=headers)

@app.post("/chat")
def chat(req: ChatRequest):
    # 组装人格对话请求
    messages =  [
        {"role": "system", "content": KONGMING_FULL_PERSONA},
        {"role": "user", "content": req.question}
    ]

    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMP,
            top_p=TOP_P,
        )
        return {"answer": res.choices[0].message.content}
    except Exception as e:
        return {"answer": "主公，本地推演服务暂时中断，请稍后再询。"}