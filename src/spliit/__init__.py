from .client import Spliit
from .utils import get_current_timestamp, format_expense_payload

CATEGORIES = {
    "Uncategorized": {
        "General": 0,
        "Payment": 1
    },
    "Entertainment": {
        "Entertainment": 2,
        "Games": 3,
        "Movies": 4,
        "Music": 5,
        "Sports": 6
    },
    "Food and Drink": {
        "Food and Drink": 7,
        "Dining Out": 8,
        "Groceries": 9,
        "Liquor": 10
    },
    "Home": {
        "Home": 11,
        "Electronics": 12,
        "Furniture": 13,
        "Household Supplies": 14,
        "Maintenance": 15,
        "Mortgage": 16,
        "Pets": 17,
        "Rent": 18,
        "Services": 19
    },
    "Life": {
        "Childcare": 20,
        "Clothing": 21,
        "Education": 22,
        "Gifts": 23,
        "Insurance": 24,
        "Medical Expenses": 25,
        "Taxes": 26
    },
    "Transportation": {
        "Transportation": 27,
        "Bicycle": 28,
        "Bus/Train": 29,
        "Car": 30,
        "Gas/Fuel": 31,
        "Hotel": 32,
        "Parking": 33,
        "Plane": 34,
        "Taxi": 35
    },
    "Utilities": {
        "Utilities": 36,
        "Cleaning": 37,
        "Electricity": 38,
        "Heat/Gas": 39,
        "Trash": 40,
        "TV/Phone/Internet": 41,
        "Water": 42
    }
}

__all__ = ["Spliit", "CATEGORIES", "get_current_timestamp", "format_expense_payload"]