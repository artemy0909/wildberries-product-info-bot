from ._helpers import reply_keyboard
from ..buttons import MenuButtons


@reply_keyboard
def menu():
    return (
        MenuButtons.get_product_info,
        MenuButtons.stop_notifications,
        MenuButtons.get_database_info
    )


@reply_keyboard
def back_to_menu():
    return MenuButtons.back_to_menu
