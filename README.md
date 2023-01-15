# Lesson about aiogram-dialog

This is a lesson about aiogram-dialog. It is a library for creating dialogs in aiogram.
To create a dialog, you can create a package 'tgbot/dialogs' and store all your dialogs there.

You can either separate or not separate your dialogs into different files. It is up to you.
This is an example of how I believe it is convenient.

### Creating a dialog

```python
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Button
from aiogram_dialog.widgets.text import Format, Const

dialog = Dialog(
    Window(
        Const('Choose select_products that you`re interested in'),
        keyboards.paginated_categories(selected.on_chosen_category),
        Cancel(Const('Exit')),
        state=BotMenu.select_categories,
        getter=getters.get_categories
    ),
    Window(...),
    ...
)
```

Here:

- `Window` is a dialog window. It is a widget that contains other widgets.
- `TextInput` is a widget that allows you to enter text. You stay in the same window until you switch to another window
  explicitly.
- `Cancel` is a widget that allows you to cancel the dialog and close it.
- `Back` is a widget that allows you to go back to the previous window.
- `Button` is a widget that allows you to handle a button click.
- `Format` is a widget that allows you to format text using the `format_map` method of 'str' type.
- `Const` is a widget that allows you to output a constant string.
- `state` is a state in which the dialog will be launched. Each window must have its own unique state with unique name.

### Registering a dialog

```python
from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry


def setup_dialogs(dp: Dispatcher):
    registry = DialogRegistry(dp)
    for dialog in [
        dialog_1, dialog_2, ...
    ]:
        registry.register(dialog)  # register a dialog
```

### Packing windows/dialogs in functions

I find it very convenient to pack dialogs in functions.
This allows you to not only group windows and dialogs in one function (if you need a lot of them),
but you can also change the creation of the dialog with additional parameters if needed.

### `dialogs/__init__.py`

```python
from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

from . import bot_menu


def setup_dialogs(dp: Dispatcher):
    registry = DialogRegistry(dp)
    for dialog in [
        *bot_menu.bot_menu_dialogs(),
    ]:
        registry.register(dialog)  # register a dialog
```

### `dialogs/bot_menu/__init__.py`

Here we have a function that creates group of dialogs called `bot_menu_dialogs`.

```python
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
```

### Dialogs structure

I believe that we can store similar functions in the same module (getters, selected, keyboards, etc.).

These are for the arguments that `Window` takes. Each of them has a slightly different syntax and behavior.

Splitting by modules allows you to quickly find the function you need, and also allows you to quickly understand what
the dialog does.

Also, you can benefit from using **GitHub Copilot (AI Assistant)** with this structure, because the suggestions will be
more relevant since the functions are looking similar.

```
dialogs
├── __init__.py
└── bot_menu
    ├── __init__.py
    ├── windows.py
    ├── getters.py
    ├── selected.py
    ├── keyboards.py
    └── states.py

```

## Creating a Dialog

### Windows: `dialogs/bot_menu/windows.py`

```python
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
```

### Keyboard: `dialogs/bot_menu/keyboards.py`

Keyboard is a widget that is used to create a keyboard. For example, `Select` is a button that can be clicked.
`ScrollingGroup` is a widget that allows you to create a scrolling keyboard (with pagination).

```python
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
```

Here:

- `Select` is a widget that creates each button
- `Format` is a widget that allows you to format the text of the button (using the data from the `getter` of the window)
- `id` is a widget id. It must be unique for each widget in the dialog.
- `item_id_getter` is a function that is used to get the id of the item.
  This item_id will be passed to the on_click function in `selected.py`. You can use `operator.itemgetter` to get the id
  from the tuple, or you can use operator.attrgetter to get the id from the object (if you use a class).
- `items` argument is a name that is used to get the data from the getter.
- `on_click` is a function that is called when the button is clicked. It is used to change the state of the dialog.

### Getters: `dialogs/bot_menu/getters.py`

You need getter functions to get data from the database or other sources and to pass it to the dialog.

Getters always accept `dialog_manager: DialogManager` as the first argument and middleware data as keyword arguments.
You can either get them explicitly or use `**kwargs` to get them all. I use `middleware_data` instead of `kwargs` to
make it more clear.

```python
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
```

### States: `dialogs/bot_menu/states.py`

You need states to be able to switch between windows, each window must have its own unique state with unique name.

```python
from aiogram.dispatcher.filters.state import StatesGroup, State


class BotMenu(StatesGroup):
    select_categories = State()
    select_products = State()
    product_info = State()


class BuyProduct(StatesGroup):
    enter_amount = State()
    confirm = State()
```

### Selected: `dialogs/bot_menu/selected.py`

You need `selected` to store functions that will be called when the user presses buttons (`on_click` callbacks).
Each function accepts `event: [Event], widget: Any, manager: DialogManager`.
Some of them also accept other params, depending on the widget.

- `event` - event that triggered the callback, for example, `CallbackQuery` or `Message`
- `widget` - widget that triggered the callback, for example, `Button` or `TextInput`
- `manager` - dialog manager, you can use it to switch windows, get data, etc.

```python
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from tgbot.dialogs.bot_menu.states import BotMenu


# Example for a Select widget. Also, item_id is passed as a parameter.
async def on_chosen_category(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(category_id=item_id)
    await manager.switch_to(BotMenu.select_products)
```

Here:

- `manager.current_context()` - returns the current context of the dialog. You can use it to get the data from the
  current dialog. Each dialog has its own context and data.
- `ctx.dialog_data.update(category_id=item_id)` - updates the data in the context. You can use it to pass data to the
  next window.
- `await manager.switch_to(BotMenu.select_products)` - switches to another window.