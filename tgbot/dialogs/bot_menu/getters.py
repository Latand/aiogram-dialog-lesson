from aiogram_dialog import DialogManager

from tgbot.dialogs.bot_menu.states import BotMenu
from tgbot.services.repo import Repo


async def get_categories(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    repo: Repo = middleware_data.get('repo')
    db_categories = await repo.get_categories(session)

    data = {
        # 'categories': db_categories
        'categories': [
            (f'{category.name} ({len(category.items)})', category.category_id)
            for category in db_categories
        ],
    }
    return data


async def get_products(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    category_id = dialog_manager.current_context().dialog_data.get('category_id')
    if not category_id:
        await dialog_manager.event.answer('Choose a category first')
        await dialog_manager.switch_to(BotMenu.select_categories)
        return

    category_id = int(category_id)
    repo: Repo = middleware_data.get('repo')
    db_products = await repo.get_products(session, category_id)

    data = {
        'products': db_products
        # 'products': [
        #     (product.name, product.product_id)
        #     for product in db_products
        # ],
    }
    return data


async def get_product_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    product_id = int(dialog_manager.current_context().dialog_data['product_id'])
    repo: Repo = middleware_data.get('repo')
    db_product = await repo.get_product(session, product_id)

    data = {
        'product': db_product
    }
    return data


async def get_product(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    context = dialog_manager.current_context()
    product_id = int(context.start_data['product_id'])
    repo: Repo = middleware_data.get('repo')
    db_product = await repo.get_product(session, product_id)
    quantity = context.dialog_data.get('quantity')
    data = {
        'product': db_product,
        'total_amount': int(quantity) * db_product.price if quantity else None,
        'quantity': quantity,
    }
    return data
