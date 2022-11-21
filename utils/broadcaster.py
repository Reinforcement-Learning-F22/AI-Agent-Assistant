import asyncio

from aiogram.utils import exceptions

from loader import bot
from utils.notify_admins import report_log


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender

    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        await report_log(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        await report_log(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        await report_log(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        await report_log(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        await report_log(f"Target [ID:{user_id}]: failed")
    else:
        await report_log(f"Target [ID:{user_id}]: success")
        return True
    return False
