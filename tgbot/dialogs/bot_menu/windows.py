from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Button
from aiogram_dialog.widgets.text import Format, Const

from . import keyboards, getters, selected
from .states import BotMenu, BuyProduct


def categories_window():
    return Window(
        Const('Choose select_products that you`re interested in'),
        keyboards.paginated_categories(selected.on_chosen_category),
        Cancel(Const('Exit')),
        state=BotMenu.select_categories,
        getter=getters.get_categories
    )


def products_window():
    return Window(
        Const('Choose product that you`re interested in'),
        keyboards.paginated_products(selected.on_chosen_product),
        Back(Const('<< Choose another select_products')),
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
        Cancel(Const('<< Choose another product')),
        state=BuyProduct.enter_amount,
        getter=getters.get_product
    )


def confirm_buy_window():
    return Window(
        Format('''You want to buy {product.name} for {product.price}$
Is it correct?'''),
        Button(Const('Yes'),
               'confirm_buy',
               on_click=selected.on_confirm_buy),
        Back(Const('<< Choose another product')),
        Cancel(Const('<< Change amount')),
        state=BuyProduct.confirm,
        getter=getters.get_product
    )
