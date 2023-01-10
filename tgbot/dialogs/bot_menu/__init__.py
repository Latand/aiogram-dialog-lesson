from aiogram_dialog import Dialog

from . import windows


def bot_menu_dialogs():
    return [
        Dialog(
            windows.categories_window(),
            windows.products_window(),
            windows.product_info_window(),
        ),
        Dialog(
            windows.buy_product_window(),
            windows.confirm_buy_window(),
        ),
    ]
