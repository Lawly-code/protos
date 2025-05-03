import grpc
import logging

from protos.ai_service.dto import AIRequestDTO, AIResponseDTO
from protos.ai_service import ai_service_pb2 as ai_pb2
from protos.ai_service import ai_service_pb2_grpc as ai_pb2_grpc

logger = logging.getLogger(__name__)


class AIAssistantClient:
    """
    Клиент для работы с GRPC сервисом AI Assistant (асинхронная версия)
    """

    def __init__(self, host: str = "localhost", port: int = 50052):
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
        self.stub = ai_pb2_grpc.AIAssistantStub(self.channel)

    async def improve_text(self, request_data: AIRequestDTO) -> AIResponseDTO | None:
        """
        Улучшает текст, используя AI.

        Args:
            request_data: DTO с параметрами запроса.

        Returns:
            DTO с улучшенным текстом или None в случае ошибки.
        """
        if not self.stub:
            await self.connect()

        try:
            request = ai_pb2.ImproveTextRequest(
                user_prompt=request_data.user_prompt,
                temperature=request_data.temperature,
                max_tokens=request_data.max_tokens
            )
            response = await self.stub.ImproveText(request)
            return AIResponseDTO(assistant_reply=response.assistant_reply)
        except grpc.RpcError as e:
            logger.error(f"GRPC ошибка: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при обращении к GRPC серверу: {str(e)}")
            return None

    async def ai_chat(self, request_data: AIRequestDTO) -> AIResponseDTO | None:
        """
        Выполняет чат с AI.

        Args:
            request_data: DTO с параметрами запроса.

        Returns:
            DTO с ответом AI или None в случае ошибки.
        """
        if not self.stub:
            await self.connect()

        try:
            request = ai_pb2.AIChatRequest(
                user_prompt=request_data.user_prompt,
                temperature=request_data.temperature,
                max_tokens=request_data.max_tokens
            )
            response = await self.stub.AIChat(request)
            return AIResponseDTO(assistant_reply=response.assistant_reply)
        except grpc.RpcError as e:
            logger.error(f"GRPC ошибка: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при обращении к GRPC серверу: {str(e)}")
            return None

    async def custom_template(self, request_data: AIRequestDTO) -> AIResponseDTO | None:
        """
        Генерирует кастомный шаблон документа.

        Args:
            request_data: DTO с параметрами запроса.

        Returns:
            DTO со сгенерированным шаблоном или None в случае ошибки.
        """
        if not self.stub:
            await self.connect()

        try:
            request = ai_pb2.CustomTemplateRequest(
                user_prompt=request_data.user_prompt,
                temperature=request_data.temperature,
                max_tokens=request_data.max_tokens
            )
            response = await self.stub.CustomTemplate(request)
            return AIResponseDTO(assistant_reply=response.assistant_reply)
        except grpc.RpcError as e:
            logger.error(f"GRPC ошибка: {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при обращении к GRPC серверу: {str(e)}")
            return None

    async def close(self):
        """
        Закрытие соединения с GRPC сервером
        """
        if self.channel:
            await self.channel.close()