from pydantic import BaseModel


class PushRequestDTO(BaseModel):
    """
    DTO для отправки push-уведомлений через gRPC.
    """
    message: dict[str, str]
    user_ids: list[int] | None = None
    is_base: bool | None = None
