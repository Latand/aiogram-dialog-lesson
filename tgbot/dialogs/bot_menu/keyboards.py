import operator

from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format

SCROLLING_HEIGHT = 6


def paginated_categories(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="s_scroll_categories",
            item_id_getter=operator.itemgetter(1),
            items="categories",
            on_click=on_click,
        ),
        id="category_ids",
        width=1, height=SCROLLING_HEIGHT,
    )


def paginated_products(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.name}"),
            id="s_scroll_products",
            item_id_getter=operator.attrgetter("product_id"),
            items="products",
            on_click=on_click,
        ),
        id="product_ids",
        width=1, height=SCROLLING_HEIGHT,
    )
