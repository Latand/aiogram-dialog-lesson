from aiogram_dialog import DialogManager

from tgbot.services.repo import Repo


async def get_categories(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    repo: Repo = middleware_data.get('repo')
    db_categories = await repo.get_categories(session)

    data = {
        # 'categories': db_categories
        'categories': [
            (category.name, category.category_id)
            for category in db_categories
        ],
    }
    return data


async def get_products(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    category_id = int(dialog_manager.current_context().dialog_data['category_id'])
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
    product_id = int(dialog_manager.current_context().start_data['product_id'])
    repo: Repo = middleware_data.get('repo')
    db_product = await repo.get_product(session, product_id)

    data = {
        'product': db_product,
    }
    return data
