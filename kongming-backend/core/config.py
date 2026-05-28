
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

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

# 初始化OpenAI兼容客户端
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

# 模型参数配置
MODEL_NAME = os.getenv("LLM_MODEL_NAME")
TEMP = float(os.getenv("TEMPERATURE", "0.45"))  # 温度参数控制随机性
TOP_P = float(os.getenv("TOP_P", "0.7"))        # top_p控制采样范围

# 会话历史长度限制，防止token过多
MAX_HISTORY_LENGTH = 22  # system + 10*2轮对话

# 每日对话配额配置
QUOTA_GUEST_DAILY_LIMIT = int(os.getenv("QUOTA_GUEST_DAILY_LIMIT", "5"))
QUOTA_USER_DAILY_LIMIT = int(os.getenv("QUOTA_USER_DAILY_LIMIT", "30"))

# 邀请码准入配置
INVITE_CODE = os.getenv("INVITE_CODE", "kongming2026")
INVITE_REQUIRED = os.getenv("INVITE_REQUIRED", "false").lower() == "true"
