
import uuid
from datetime import datetime
from core.config import KONGMING_FULL_PERSONA


class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.session_info = {}
    
    def create_session(self):
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
        session_list = list(self.session_info.values())
        # 按更新时间倒序排列
        session_list.sort(key=lambda x: x["updated_at"], reverse=True)
        return session_list
    
    def get_session(self, session_id):
        if session_id not in self.sessions:
            return None
        
        # 转换assistant -> ai 给前端
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
        deleted = False
        if session_id in self.sessions:
            del self.sessions[session_id]
            deleted = True
        if session_id in self.session_info:
            del self.session_info[session_id]
            deleted = True
        return deleted
    
    def update_session_title(self, session_id, title):
        if session_id in self.session_info:
            self.session_info[session_id]["title"] = title
            self.session_info[session_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False
    
    def restore_session(self, session_id, history):
        if not session_id:
            session_id = str(uuid.uuid4())
        
        now = datetime.now().isoformat()
        
        # 确保历史格式正确，支持角色转换
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
        
        # 添加系统提示到开头
        if not validated_history or validated_history[0].get("role") != "system":
            validated_history.insert(0, {"role": "system", "content": KONGMING_FULL_PERSONA})
        
        self.sessions[session_id] = validated_history
        
        # 更新或创建会话信息
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
        if session_id not in self.sessions:
            session_id = self.create_session()
        
        self.sessions[session_id].append({"role": "user", "content": question})
        return session_id
    
    def add_assistant_message(self, session_id, content, first_question=None):
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id].append({"role": "assistant", "content": content})
        
        # 更新会话信息
        if session_id in self.session_info:
            self.session_info[session_id]["updated_at"] = datetime.now().isoformat()
            self.session_info[session_id]["message_count"] = len(self.sessions[session_id]) - 1
            
            # 如果是第一条消息，自动生成标题
            if (self.session_info[session_id]["message_count"] == 2 and 
                self.session_info[session_id]["title"] == "新对话" and 
                first_question):
                title = first_question
                if len(title) > 20:
                    title = title[:20] + "..."
                self.session_info[session_id]["title"] = title
        
        return True
    
    def get_session_history(self, session_id, max_length=22):
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]
        
        # 限制历史长度，防止token过多
        if len(messages) > max_length:
            messages = [messages[0]] + messages[-(max_length - 1):]
            self.sessions[session_id] = messages
        
        return messages


# 全局实例
session_manager = SessionManager()
