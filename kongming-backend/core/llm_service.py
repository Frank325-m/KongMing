
from core.config import client, MODEL_NAME, TEMP, TOP_P


class LLMService:
    """LLM服务封装：流式生成孔明回复"""
    @staticmethod
    def generate_stream_response(messages):
        """流式生成回复，逐字返回"""
        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                stream=True,
                temperature=TEMP,
                top_p=TOP_P,
            )
            
            ai_response = ""
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    ai_response += content
                    yield f"{content}\n\n"
            
            yield "[DONE]\n\n"
            return ai_response
        
        except Exception as e:
            yield f"error:{str(e)}\n\n"
            return None


# 全局LLM服务实例
llm_service = LLMService()
