
import uuid
from datetime import datetime
from core.config import KONGMING_FULL_PERSONA


class SessionManager:
    """会话管理器：内存存储，管理所有对话会话"""
    def __init__(self):
        self.sessions = {}      # 会话消息内容
        self.session_info = {}  # 会话元信息
    
    def create_session(self):
        """创建新会话，初始化孔明人格"""
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        self.sessions[session_id] = [
            {"role": "system", "content": KONGMING_FULL_PERSONA}
        ]
        
        self.session_info[session_id] = {
            "id": session_id,
            "title": "新对话",
            "created_at": now,
            "updated_at": now,
            "message_count": 0
        }
        
        return session_id
    
    def get_all_sessions(self):
        """获取所有会话列表，按更新时间倒序排列"""
        session_list = list(self.session_info.values())
        session_list.sort(key=lambda x: x["updated_at"], reverse=True)
        return session_list
    
    def get_session(self, session_id):
        """获取单个会话，转换角色名给前端（assistant -> ai）"""
        if session_id not in self.sessions:
            return None
        
        frontend_messages = []
        for msg in self.sessions[session_id]:
            role = msg["role"]
            if role == "assistant":
                role = "ai"
            frontend_messages.append({
                "role": role,
                "content": msg["content"]
            })
        
        return {
            "session_id": session_id,
            "messages": frontend_messages,
            "info": self.session_info.get(session_id, {})
        }
    
    def delete_session(self, session_id):
        """删除指定会话"""
        deleted = False
        if session_id in self.sessions:
            del self.sessions[session_id]
            deleted = True
        if session_id in self.session_info:
            del self.session_info[session_id]
            deleted = True
        return deleted
    
    def update_session_title(self, session_id, title):
        """更新会话标题"""
        if session_id in self.session_info:
            self.session_info[session_id]["title"] = title
            self.session_info[session_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False
    
    def restore_session(self, session_id, history):
        """从前端历史恢复会话，用于页面刷新后重建"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        now = datetime.now().isoformat()
        
        # 验证历史格式，支持前后端角色名转换
        validated_history = []
        for msg in history:
            if msg.get("role") and msg.get("content"):
                role = msg["role"]
                if role == "ai":
                    role = "assistant"
                if role in ["system", "assistant", "user"]:
                    validated_history.append({
                        "role": role,
                        "content": msg["content"]
                    })
        
        # 确保孔明人格在最前面
        if not validated_history or validated_history[0].get("role") != "system":
            validated_history.insert(0, {"role": "system", "content": KONGMING_FULL_PERSONA})
        
        self.sessions[session_id] = validated_history
        
        # 更新会话元信息
        if session_id not in self.session_info:
            self.session_info[session_id] = {
                "id": session_id,
                "title": "新对话",
                "created_at": now,
                "updated_at": now,
                "message_count": len(validated_history) - 1
            }
        else:
            self.session_info[session_id]["updated_at"] = now
            self.session_info[session_id]["message_count"] = len(validated_history) - 1
        
        return session_id
    
    def clear_session(self, session_id):
        """清空会话，仅保留孔明人格"""
        if session_id in self.sessions:
            self.sessions[session_id] = [
                {"role": "system", "content": KONGMING_FULL_PERSONA}
            ]
            if session_id in self.session_info:
                self.session_info[session_id]["updated_at"] = datetime.now().isoformat()
                self.session_info[session_id]["message_count"] = 0
            return True
        return False
    
    def add_user_message(self, session_id, question):
        """添加用户消息到会话"""
        if session_id not in self.sessions:
            session_id = self.create_session()
        
        self.sessions[session_id].append({"role": "user", "content": question})
        return session_id
    
    def add_assistant_message(self, session_id, content, first_question=None):
        """添加助手消息，第一条自动生成会话标题"""
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id].append({"role": "assistant", "content": content})
        
        if session_id in self.session_info:
            self.session_info[session_id]["updated_at"] = datetime.now().isoformat()
            self.session_info[session_id]["message_count"] = len(self.sessions[session_id]) - 1
            
            # 第一条消息生成会话标题
            if (self.session_info[session_id]["message_count"] == 2 and 
                self.session_info[session_id]["title"] == "新对话" and 
                first_question):
                title = first_question
                if len(title) > 20:
                    title = title[:20] + "..."
                self.session_info[session_id]["title"] = title
        
        return True
    
    def get_session_history(self, session_id, max_length=22):
        """获取会话历史，自动截断过长历史保留最前面的系统提示和最近对话"""
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]
        
        if len(messages) > max_length:
            messages = [messages[0]] + messages[-(max_length - 1):]
            self.sessions[session_id] = messages
        
        return messages


# 全局会话管理器实例
session_manager = SessionManager()
