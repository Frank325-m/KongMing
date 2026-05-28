
from core.config import client, MODEL_NAME, TEMP, TOP_P


class LLMService:
    @staticmethod
    def generate_stream_response(messages):
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


llm_service = LLMService()
