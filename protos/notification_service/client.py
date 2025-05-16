import grpc
import logging
from typing import Optional

from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import ParseDict  # ✅ Это нужно для корректного преобразования

from protos.notification_service import notification_service_pb2 as notification_pb2
from protos.notification_service import notification_service_pb2_grpc as notification_pb2_grpc
from .dto import PushRequestDTO

logger = logging.getLogger(__name__)


class NotificationServiceClient:
    """
    Асинхронный gRPC-клиент для Notification Service.
    """

    def __init__(self, host: str = "localhost", port: int = 50054):
        self.target = f"{host}:{port}"
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[notification_pb2_grpc.NotificationServiceStub] = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """
        Устанавливает соединение с gRPC-сервером.
        """
        if not self.channel:
            self.channel = grpc.aio.insecure_channel(self.target)
            self.stub = notification_pb2_grpc.NotificationServiceStub(self.channel)

    async def send_push_from_users(self, request_data: PushRequestDTO) -> bool:
        """
        Отправка push-уведомлений пользователям через gRPC.

        Args:
            request_data: DTO с параметрами запроса

        Returns:
            True при успехе, False при ошибке
        """
        if not self.stub:
            await self.connect()

        try:
            logger.warning("📤 NotificationServiceClient.send_push_from_users CALLED")  # ⬅️ Debug log

            message_struct = ParseDict(request_data.message, Struct())  # ✅ безопасное преобразование

            request = notification_pb2.SendPushFromUsersRequest(
                message=message_struct,
                user_ids=request_data.user_ids or []
            )

            if request_data.is_base is not None:
                request.is_base = request_data.is_base

            await self.stub.SendPushFromUsers(request)
            return True

        except grpc.RpcError as e:
            logger.error(f"GRPC ошибка: {e}")
            return False

        except Exception as e:
            logger.error(f"Ошибка при обращении к GRPC серверу: {str(e)}")
            return False

    async def close(self):
        """
        Закрывает соединение с gRPC-сервером.
        """
        if self.channel:
            await self.channel.close()
            self.channel = None
            self.stub = None