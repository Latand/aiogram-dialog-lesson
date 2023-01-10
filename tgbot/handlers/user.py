from aiogram import Dispatcher
from aiogram.types import Message
from aiogram_dialog import DialogManager

from tgbot.dialogs.bot_menu.states import BotMenu


async def command_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(BotMenu.select_categories)


def register_user(dp: Dispatcher):
    dp.register_message_handler(command_menu, commands=["menu"], state="*")
