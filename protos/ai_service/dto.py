from pydantic import BaseModel


class AIRequestDTO(BaseModel):
    """Базовый класс для запросов к AI сервису"""
    user_prompt: str
    temperature: float | None = None
    max_tokens: int | None = None


class AIResponseDTO(BaseModel):
    """Класс для ответов от AI сервиса"""
    assistant_reply: str
