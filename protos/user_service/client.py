import grpc
import logging

from protos.user_service import user_service_pb2 as user_pb2
from protos.user_service import user_service_pb2_grpc as user_pb2_grpc
from protos.user_service.dto import GetUserInfoDTO, TariffDTO

logger = logging.getLogger(__name__)


class UserServiceClient:
    """
    Клиент для работы с GRPC сервисом пользователей (асинхронная версия)
    """

    def __init__(self, host: str = "localhost", port: int = 50051):
        """
        Инициализация клиента

        Args:
            host: хост GRPC сервера
            port: порт GRPC сервера
        """
        self.target = f"{host}:{port}"
        self.channel = None
        self.stub = None

    async def connect(self):
        """
        Установка соединения с GRPC сервером
        """
        self.channel = grpc.aio.insecure_channel(self.target)
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)

    async def get_user_info(self, user_id: int) -> GetUserInfoDTO | None:
        """
        Получение информации о пользователе и его подписке

        Args:
            user_id: идентификатор пользователя

        Returns:
            Информация о пользователе или None в случае ошибки
        """
        if not self.stub:
            await self.connect()

        try:
            request = user_pb2.GetUserInfoRequest(user_id=user_id)
            response = await self.stub.GetUserInfo(request)

            return GetUserInfoDTO(
                user_id=response.user_id,
                tariff=TariffDTO(
                    id=response.tariff.id,
                    name=response.tariff.name,
                    description=response.tariff.description,
                    price=response.tariff.price,
                    features=response.tariff.features,
                ),
                start_date=response.start_date,
                end_date=response.end_date,
                count_lawyers=response.count_lawyers,
                consultations_total=response.consultations_total,
                consultations_used=response.consultations_used,
                can_user_ai=response.can_user_ai,
                can_create_custom_templates=response.can_create_custom_templates,
                unlimited_documents=response.unlimited_documents
            )
        except grpc.RpcError as e:
            logger.error(f"GRPC ошибка: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при обращении к GRPC серверу: {str(e)}")
            return None

    async def write_off_consultation(self, user_id: int) -> bool:
        """
        Списание консультации

        Args:
            user_id: идентификатор пользователя

        Returns:
            True при успехе, False при ошибке
        """
        if not self.stub:
            await self.connect()

        try:
            request = user_pb2.WriteOffConsultationRequest(user_id=user_id)
            await self.stub.WriteOffConsultation(request)
            return True
        except grpc.RpcError as e:
            logger.error(f"GRPC ошибка: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при обращении к GRPC серверу: {str(e)}")
            return False

    async def close(self):
        """
        Закрытие соединения с GRPC сервером
        """
        if self.channel:
            await self.channel.close()