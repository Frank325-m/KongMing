
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from core.models import (
    ChatRequest,
    RestoreSessionRequest,
    UpdateSessionTitleRequest
)
from core.session_manager import session_manager
from core.llm_service import llm_service
from core.config import MAX_HISTORY_LENGTH

app = FastAPI(title="孔明AI军师")

# 全局跨域配置 - 针对SSE优化
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # 暴露所有头给前端
    max_age=86400  # 预检请求缓存时间
)


@app.get("/")
def home():
    return {"message": "孔明后端已就位，恭候主公"}


@app.post("/new-session")
def create_session():
    session_id = session_manager.create_session()
    return {"session_id": session_id}


@app.get("/sessions")
def get_sessions():
    return {"sessions": session_manager.get_all_sessions()}


@app.get("/session/{session_id}")
def get_session(session_id: str):
    result = session_manager.get_session(session_id)
    if result is None:
        return {"error": "会话不存在"}
    return result


@app.post("/update-session-title")
def update_session_title(request: UpdateSessionTitleRequest):
    success = session_manager.update_session_title(request.session_id, request.title)
    return {"success": success}


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    success = session_manager.delete_session(session_id)
    return {"success": True}


@app.post("/restore-session")
def restore_session(request: RestoreSessionRequest):
    session_id = session_manager.restore_session(request.session_id, request.history)
    return {"session_id": session_id}


@app.post("/clear-session")
def clear_session(session_id: str):
    success = session_manager.clear_session(session_id)
    return {"success": True}


# 流式对话接口（核心）- 支持上下文记忆
@app.get("/chat-stream")
@app.post("/chat-stream")
async def chat_stream(request: Request, question: str = None, session_id: str = None):
    extracted_question = question
    extracted_session_id = session_id

    # 处理GET或POST请求（从请求体获取）
    if not extracted_question:
        try:
            body = await request.body()
            if body:
                data = await request.json()
                extracted_question = data.get("question")
                extracted_session_id = data.get("session_id")
        except:
            pass

    if not extracted_question:
        return {"error": "问题不能为空"}

    # 获取或创建会话，添加用户消息
    current_session_id = session_manager.add_user_message(extracted_session_id, extracted_question)
    
    # 获取会话历史
    messages = session_manager.get_session_history(current_session_id, MAX_HISTORY_LENGTH)

    async def async_generator():
        try:
            stream = llm_service.generate_stream_response(messages)
            ai_response = ""

            for chunk in stream:
                if chunk.startswith("error:"):
                    yield chunk
                    return

                if chunk == "[DONE]\n\n":
                    if ai_response:
                        session_manager.add_assistant_message(
                            current_session_id, 
                            ai_response, 
                            extracted_question
                        )
                    yield f"session_id:{current_session_id}\n\n"
                else:
                    yield chunk
                    if chunk.strip() and chunk != "[DONE]\n\n":
                        ai_response += chunk.replace("\n\n", "")

        except Exception as e:
            yield f"error:{str(e)}\n\n"

    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }

    return StreamingResponse(async_generator(), headers=headers)
