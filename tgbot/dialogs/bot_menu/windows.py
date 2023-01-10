from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Button
from aiogram_dialog.widgets.text import Format

from . import keyboards, getters, selected
from .states import BotMenu, BuyProduct


def categories_window():
    return Window(
        Format('{window_text}'),
        keyboards.paginated_categories(selected.on_chosen_category),
        Cancel(Format('{cancel_text}')),
        state=BotMenu.select_categories,
        getter=getters.get_categories
    )


def products_window():
    return Window(
        Format('{window_text}'),
        keyboards.paginated_products(selected.on_chosen_product),
        Back(Format('{back_text}')),
        state=BotMenu.select_products,
        getter=getters.get_products
    )


def product_info_window():
    return Window(
        Format('{window_text}'),
        Button(
            Format('{buy_text}'),
            'buy_product',
            on_click=selected.on_buy_product),
        Back(Format('{back_text}')),
        state=BotMenu.product_info,
        getter=getters.get_product_info
    )


def buy_product_window():
    return Window(
        Format('{window_text}'),
        TextInput(id='amount', on_success=selected.on_entered_amount),
        Cancel(Format('{cancel_text}')),
        state=BuyProduct.enter_amount,
        getter=getters.get_amount
    )


def confirm_buy_window():
    return Window(
        Format('{window_text}'),
        Button(Format('{yes_text}'),
               'confirm_buy',
               on_click=selected.on_confirm_buy),
        Back(Format('{back_text}')),
        Cancel(Format('{cancel_text}')),
        state=BuyProduct.confirm,
        getter=getters.get_confirm
    )
