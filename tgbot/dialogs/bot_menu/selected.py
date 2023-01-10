import logging
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

# async def on_chosen_some_item(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
#     ctx = manager.current_context()
#     ctx.dialog_data.update(some_item=item_id)
#     await manager.switch_to(SomeGroupState.SomeAction)
from tgbot.dialogs.bot_menu.getters import get_product_info, fake_db_get_product, fake_db_buy_product
from tgbot.dialogs.bot_menu.states import BotMenu, BuyProduct


async def on_chosen_category(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(category_id=item_id)
    await manager.switch_to(BotMenu.select_products)


async def on_chosen_product(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(product_id=item_id)
    await manager.switch_to(BotMenu.product_info)


async def on_buy_product(c: CallbackQuery, widget: Any, manager: DialogManager):
    ctx = manager.current_context()
    product_id = ctx.dialog_data.get('product_id')
    await manager.start(BuyProduct.enter_amount, data={'product_id': product_id})


async def on_entered_amount(m: Message, widget: Any, manager: DialogManager, amount: str):
    ctx = manager.current_context()
    if not amount.isdigit():
        await m.answer('Enter a number')
        return
    product_id = int(ctx.start_data.get('product_id'))
    session = None
    product_info = await fake_db_get_product(session, product_id)
    stock = product_info['stock']
    if int(amount) > stock:
        await m.reply('Not enough in stock')
        return

    ctx.dialog_data.update(amount=amount)
    await manager.switch_to(BuyProduct.confirm)


async def on_confirm_buy(c: CallbackQuery, widget: Any, manager: DialogManager):
    ctx = manager.current_context()
    product_id = int(ctx.start_data.get('product_id'))
    amount = int(ctx.dialog_data.get('amount'))
    session = None
    await fake_db_buy_product(session, product_id, amount)
    product = await fake_db_get_product(session, product_id)

    name = product['name']
    await c.message.answer(f'You bought {amount} {name}!')
    await manager.done()
