from dotenv import load_dotenv
from llama_index.embeddings.openai_like import OpenAILikeEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
import os

load_dotenv()

_initialized = False


def init_llama_index():
    global _initialized
    if _initialized:
        return

    Settings.embed_model = OpenAILikeEmbedding(
        model_name=os.getenv("EMBEDDING_MODEL_NAME", "qwen3-embedding-4b"),
        api_base=os.getenv("BASE_URL", "http://host.docker.internal:8080/v1"),
        api_key="not-needed",
        check_embedding_ctx_length=False,
        timeout=120,
    )

    Settings.llm = OpenAILike(
        model=os.getenv("LLM_MODEL_NAME", "gpt-oss-120b"),
        api_base=os.getenv("BASE_URL", "http://host.docker.internal:8080/v1"),
        api_key="not-needed",
        timeout=120,
        is_chat_model=True,  # this is important
    )

    _initialized = True
