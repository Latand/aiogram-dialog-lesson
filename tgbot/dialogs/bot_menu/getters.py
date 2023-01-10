from aiogram_dialog import DialogManager

categories = [
    {
        'id': 1,
        'name': 'Fruits 🍎',
        'items': [
            {
                'name': 'Apple 🍎',
                'id': 1,
                'price': 5.00,
                'stock': 10
            },
            {
                'name': 'Banana 🍌',
                'id': 2,
                'price': 3.00,
                'stock': 15
            },
        ]
    },
    {
        'id': 2,
        'name': 'Vegetables 🥕',
        'items': [
            {
                'name': 'Potato  🥔',
                'id': 3,
                'price': 4.00,
                'stock': 12
            },
            {
                'name': 'Tomato  🍅',
                'id': 4,
                'price': 2.00,
                'stock': 20
            }
        ]
    }
]


async def fake_db_get_categories(session) -> list:
    # stmt = select(Categories.category_name, Categories.category_id)
    # result = await session.execute(stmt)
    # categories = result.execute().all()
    return categories


async def fake_db_get_products(session, category_id) -> dict:
    # stmt = select(
    #   Products.product_name, Products.product_id, Products.price, Products.stock
    # ).where(Products.category_id == category_id)
    # result = await session.execute(stmt)
    # products = result.execute().all()
    for category in categories:
        if category['id'] == category_id:
            return category


async def fake_db_get_product(session, product_id) -> dict:
    # stmt = select(
    #   Products.product_name, Products.product_id, Products.price, Products.stock
    # ).where(Products.product_id == product_id)
    # result = await session.execute(stmt)
    # product = result.execute().all()
    for category in categories:
        for product in category['items']:
            if product['id'] == product_id:
                return product


async def fake_db_buy_product(session, product_id, amount) -> bool:
    # stmt = update(Products).where(Products.product_id == product_id).values(
    #   stock=Products.stock - amount
    # )
    # await session.execute(stmt)
    # await session.commit()
    for category in categories:
        for product in category['items']:
            if product['id'] == product_id:
                product['stock'] -= amount
                return True


async def get_categories(dialog_manager: DialogManager, **midlleware_data):
    session = None  # TODO: get session from middleware
    db_categories = await fake_db_get_categories(session)

    data = {
        'categories': [
            (category['name'], category['id'])
            for category in db_categories
        ],
        'window_text': 'Choose select_products that you`re interested in',
        'cancel_text': 'Exit',
    }
    return data


async def get_products(dialog_manager: DialogManager, **midlleware_data):
    session = None  # TODO: get session from middleware
    category_id = int(dialog_manager.current_context().dialog_data['category_id'])
    db_products = await fake_db_get_products(session, category_id)

    data = {
        'products': [
            (product['name'], product['id'])
            for product in db_products['items']
        ],
        'window_text': 'Choose product that you`re interested in',
        'back_text': '<< Choose another select_products',
    }
    return data


async def get_product_info(dialog_manager: DialogManager, **midlleware_data):
    session = None  # TODO: get session from middleware
    product_id = int(dialog_manager.current_context().dialog_data['product_id'])
    db_product = await fake_db_get_product(session, product_id)

    data = {
        'window_text': f'''Product: {db_product["name"]}
Price: {db_product["price"]}
In Stock: {db_product["stock"]} pcs''',
        'buy_text': 'Buy',
        'back_text': '<< Choose another product',
    }
    return data


async def get_amount(dialog_manager: DialogManager, **midlleware_data):
    session = None  # TODO: get session from middleware
    product_id = int(dialog_manager.current_context().start_data['product_id'])
    db_product = await fake_db_get_product(session, product_id)

    data = {
        'window_text': f'''How many {db_product["name"]} do you want to buy?
In Stock: {db_product["stock"]} pcs''',
        'cancel_text': '<< Choose another product',
    }
    return data


async def get_confirm(dialog_manager: DialogManager, **midlleware_data):
    session = None  # TODO: get session from middleware
    product_id = int(dialog_manager.current_context().start_data['product_id'])
    db_product = await fake_db_get_product(session, product_id)

    data = {
        'window_text': f'''You want to buy {db_product["name"]} for {db_product["price"]}$
Is it correct?''',
        'yes_text': 'Yes',
        'cancel_text': '<< Choose another product',
        'back_text': '<< Change amount',
    }
    return data
