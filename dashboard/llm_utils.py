import json

from accounts.models import CustomUser
from dashboard.models import Order, Product
from mahour_ai import settings
from .serializers import OrderWithItemsSerializer, ProductSerializer

# TODO: Cache data
def get_initial_context(user: CustomUser|None = None) -> str:
    """Prepares context for LLM API calls by fetching products, user, orders data."""
    if not user:
        return get_store_context_text()

    return "\n".join((get_store_context_text(), get_user_context_text(user),))

def get_store_context_text() -> str:
    store_context = get_store_context()
    store_context_message = settings.INITIAL_LLM_CONTEXT
    if store_context:
        products = store_context.get("products")
        if products:
            store_context_message += (
                "\nHere is the list of all products with their prices and categories:\n"
                f"{json.dumps(products)}\n"
            )
    return store_context_message

def get_user_context_text(user: CustomUser) -> str:
    user_context = get_user_context(user)
    user_context_message = ""
    username = user_context.get("username")
    orders = user_context.get("orders")
    if username:
        user_context_message += f"\nPlease call the user by their username: {username}.\n"
    if orders:
        user_context_message += f"\nHere is the customer's order history:\n{json.dumps(orders)}\n"

    return user_context_message


def get_store_context() -> dict:
    products = Product.objects.all()
    serialized_products = ProductSerializer(products, many=True)
    return {
        "products": serialized_products.data,
    }

# TODO: get only the last N orders of the user
def get_user_context(user: CustomUser) -> dict:
    orders = Order.objects.filter(user=user).prefetch_related('items')
    serialized_orders = OrderWithItemsSerializer(orders, many=True)
    return {
        "username": user.username,
        "orders": serialized_orders.data,
    }
