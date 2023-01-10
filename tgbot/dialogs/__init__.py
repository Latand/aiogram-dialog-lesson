from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

from . import bot_menu


def setup_dialogs(dp: Dispatcher):
    registry = DialogRegistry(dp)
    for dialog in [
        *bot_menu.bot_menu_dialogs(),
    ]:
        registry.register(dialog)  # register a dialog
