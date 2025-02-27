import httpx
import re

from .constants import API_TOKEN_CHECK_URL, GET_SERVICES_URL, IMEI_CHECK_URL
from .constants import CheckHeadersConst


def check_sub_channel(chat_member):
    """Проверяет подписку пользователя на канал."""

    if chat_member.status != 'left':
        return True
    return False


def validate_imei(imei: str) -> bool:
    """Валидирует IMEI по длине и числовому формату."""

    return bool(re.fullmatch(r"\d{15}", imei))


async def check_token(text: str):
    """Выполняет запрос к imeicheck.net и
    проверяет валидность переданного API-токена."""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                API_TOKEN_CHECK_URL,
                headers=CheckHeadersConst.headers(text),
            )
            if response.status_code == 401:
                return {"status": "unauthorized",
                        "message": "Токен недействителен."}
            response.raise_for_status()
            return {"status": "authorized", "data": response.json()}

        except httpx.HTTPStatusError as exc:
            return f"Ошибка: {exc.response.status_code} - {exc.response.text}"
        except Exception as exc:
            return f"Ошибка подключения: {exc}"


async def get_service_list(text: str):
    """Выполняет запрос к imeicheck.net и
    получает список бесплатных сервисов для API-токена."""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                GET_SERVICES_URL,
                headers=CheckHeadersConst.headers(text),
            )
            response.raise_for_status()
            services = response.json()

            free_services = [
                service for service in services
                if (
                    service.get("price") == "0.00" and
                    service.get("title") == "Mock service with only successful results")
            ]
            return [service["id"] for service in free_services]

        except httpx.HTTPStatusError as exc:
            return f"Ошибка: {exc.response.status_code} - {exc.response.text}"
        except Exception as exc:
            return f"Ошибка подключения: {exc}"


async def check_imei(imei: str, token: str):
    """Выполняет запрос к imeicheck.net для проверки IMEI
    и предоставляет информацию о IMEI."""

    service_ids = await get_service_list(token)
    if not service_ids:
        return (
            "Для данного API-токена нет доступных бесплатных сервисов. "
            "Попробуйте ввести другой API-токен.")

    service_id = service_ids[-1]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                IMEI_CHECK_URL,
                headers=CheckHeadersConst.headers(token),
                json={
                    "deviceId": imei,
                    "serviceId": service_id
                }
            )
            response.raise_for_status()
            imei_info = response.json()
            return imei_info

        except httpx.HTTPStatusError as exc:
            return f"Ошибка: {exc.response.status_code} - {exc.response.text}"
        except Exception as exc:
            return f"Ошибка подключения: {exc}"
