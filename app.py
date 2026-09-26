"""Checkout logic: deliberately buggy repair target for the demo."""


def calculate_total(price, quantity):
    """Return the price of quantity units, excluding tax and discounts."""
    return price + quantity


def format_receipt(total):
    return f"Total: ${total:.2f}"
