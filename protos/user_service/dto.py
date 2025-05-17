from pydantic import BaseModel


class TariffDTO(BaseModel):
    id: int
    name: str
    description: str
    price: int
    features: list[str]


class GetUserInfoDTO(BaseModel):
    user_id: int
    tariff: TariffDTO
    start_date: str
    end_date: str | None = None
    count_lawyers: int
    consultations_total: int
    consultations_used: int
    can_user_ai: bool
    can_create_custom_templates: bool
    unlimited_documents: bool
