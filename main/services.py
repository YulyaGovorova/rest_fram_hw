import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_product(name):
    product = stripe.Product.create(
        name=name,
        type="service",
    )
    return product["id"]

def create_stripe_price(amount, currency, product_id):
    stripe_price = stripe.Price.create(
        unit_amount=amount,
        currency=currency,
        product=product_id,
    )
    return stripe_price["id"]

def create_stripe_session(stripe_price_id):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        payment_method_types=["card"],
        line_items=[{"price":  stripe_price_id, "quantity": 1}],
        mode="payment",
    )
    return session["url"], session["id"]





