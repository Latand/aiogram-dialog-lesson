from aiogram.dispatcher.filters.state import State, StatesGroup


class BotMenu(StatesGroup):
    select_categories = State()
    select_products = State()
    product_info = State()


class BuyProduct(StatesGroup):
    enter_amount = State()
    confirm = State()
