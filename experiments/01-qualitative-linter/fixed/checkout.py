"""Checkout flow of a demo shop. Invented code for a talk: no real system, every value is fake."""
import hashlib
import logging

log = logging.getLogger("shop.checkout")


def mask(value, keep=4):
    """Hide everything except the last `keep` characters."""
    value = str(value)
    return "*" * len(value) if len(value) <= keep else "*" * (len(value) - keep) + value[-keep:]


def start_checkout(cart, customer, request, api_key_rotated):
    token_count = len(cart.items)
    log.info(f"checkout started, {token_count} items in cart")

    creds = request.headers["Authorization"]
    session = verify_session(creds)
    log.debug(f"verifying session with {mask(creds)}")

    contact = customer.email
    log.info(f"sending order confirmation to {contact}")
    log.info(f"shipping to {customer.address}")

    customer_ref = hashlib.sha256(customer.id.encode()).hexdigest()[:12]
    log.info(f"customer {customer_ref} checked out, total {cart.total} EUR")
    log.info(f"api key rotated this week: {api_key_rotated}")
    return session


def verify_session(creds):
    """Stub: a real shop would check the bearer token here."""
    return {"ok": bool(creds)}
