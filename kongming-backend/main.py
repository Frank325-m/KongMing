
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
from core.config import MAX_HISTORY_LENGTH, QUOTA_GUEST_DAILY_LIMIT, QUOTA_USER_DAILY_LIMIT, INVITE_CODE, INVITE_REQUIRED
from pydantic import BaseModel

# FastAPI应用初始化
app = FastAPI(title="孔明AI军师")

# 全局跨域配置 - 针对SSE流式响应优化
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
    """健康检查接口"""
    return {"message": "孔明后端已就位，恭候主公"}


# 获取每日配额配置，支持动态配置
@app.get("/quota-config")
def get_quota_config():
    return {
        "guest_daily_limit": QUOTA_GUEST_DAILY_LIMIT,
        "user_daily_limit": QUOTA_USER_DAILY_LIMIT
    }

class InviteCodeRequest(BaseModel):
    code: str

# 验证邀请码是否正确
@app.post("/verify-invite")
def verify_invite_code(request: InviteCodeRequest):
    if not INVITE_REQUIRED:
        return {"success": True, "message": "邀请码验证未启用"}
    if request.code == INVITE_CODE:
        return {"success": True, "message": "验证通过，请进"}
    return {"success": False, "message": "邀请码有误，请核实"}

# 获取是否需要邀请码配置
@app.get("/invite-required")
def get_invite_required():
    return {
        "required": INVITE_REQUIRED
    }


@app.post("/new-session")
def create_session():
    """创建新会话"""
    session_id = session_manager.create_session()
    return {"session_id": session_id}


@app.get("/sessions")
def get_sessions():
    """获取所有会话列表"""
    return {"sessions": session_manager.get_all_sessions()}


@app.get("/session/{session_id}")
def get_session(session_id: str):
    """获取单个会话详情"""
    result = session_manager.get_session(session_id)
    if result is None:
        return {"error": "会话不存在"}
    return result


@app.post("/update-session-title")
def update_session_title(request: UpdateSessionTitleRequest):
    """更新会话标题"""
    success = session_manager.update_session_title(request.session_id, request.title)
    return {"success": success}


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """删除指定会话"""
    success = session_manager.delete_session(session_id)
    return {"success": True}


@app.post("/restore-session")
def restore_session(request: RestoreSessionRequest):
    """从前端历史恢复会话"""
    session_id = session_manager.restore_session(request.session_id, request.history)
    return {"session_id": session_id}


@app.post("/clear-session")
def clear_session(session_id: str):
    """清空会话内容，保留孔明人格"""
    success = session_manager.clear_session(session_id)
    return {"success": True}


# 流式对话接口（核心）- 支持上下文记忆
@app.get("/chat-stream")
@app.post("/chat-stream")
async def chat_stream(request: Request, question: str = None, session_id: str = None):
    """核心流式对话接口，支持GET/POST，返回SSE流"""
    extracted_question = question
    extracted_session_id = session_id

    # 支持两种请求方式：URL参数或请求体
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
    
    # 获取会话历史，自动截断过长历史
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
                    # 流式响应完成，保存助手消息
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
