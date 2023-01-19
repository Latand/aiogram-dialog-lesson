import logging
from typing import Any

from aiogram_dialog import Window, Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Button
from aiogram_dialog.widgets.text import Format, Const

from . import keyboards, getters, selected
from .states import BotMenu, BuyProduct
from ...misc.constants import SwitchToWindow


def categories_window():
    return Window(
        Const('Choose Category that you`re interested in'),
        keyboards.paginated_categories(selected.on_chosen_category),
        Cancel(Const('Exit')),
        state=BotMenu.select_categories,
        getter=getters.get_categories
    )


def products_window():
    return Window(
        Const('Choose Product that you`re interested in'),
        keyboards.paginated_products(selected.on_chosen_product),
        Back(Const('<< Choose another Product')),
        state=BotMenu.select_products,
        getter=getters.get_products
    )


def product_info_window():
    return Window(
        Format('''Product: {product.name}
Price: {product.price}
In Stock: {product.stock} pcs'''),
        Button(
            Const('Buy'),
            'buy_product',
            on_click=selected.on_buy_product),
        Back(Const('<< Choose another product')),
        state=BotMenu.product_info,
        getter=getters.get_product_info,
    )


def buy_product_window():
    return Window(
        Format('''How many {product.name} do you want to buy?
In Stock: {product.stock} pcs'''),
        TextInput(id='amount', on_success=selected.on_entered_amount),
        Cancel(Const('Cancel')),
        Cancel(Const('<< Choose another product'),
               'cancel_switch_to_select_products',
               result={'switch_to_window': SwitchToWindow.SelectProducts}),
        state=BuyProduct.enter_amount,
        getter=getters.get_product
    )


def confirm_buy_window():
    return Window(
        Format('''You want to buy {quantity} {product.name} for {total_amount}$
Is it correct?'''),
        Button(Const('Yes'),
               'confirm_buy',
               on_click=selected.on_confirm_buy),
        Back(Const('<< Change amount')),
        Cancel(Const('<< Choose another product'),
               'cancel_switch_to_select_products',
               result={'switch_to_window': SwitchToWindow.SelectProducts}),
        state=BuyProduct.confirm,
        getter=getters.get_product
    )


async def on_process_result(data: Data, result: Any, manager: DialogManager):
    if result:
        switch_to_window = result.get('switch_to_window')
        if switch_to_window == SwitchToWindow.SelectProducts:
            manager.show_mode = ShowMode.SEND
            await manager.switch_to(BotMenu.select_products)
