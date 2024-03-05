import stripe


from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_payment(validated_data):
    # Получение данных из validated_data
    paid_course = validated_data['paid_course']
    summ = validated_data['summ']

    # Создание продукта в Stripe
    product = stripe.Product.create(
        name=paid_course.name,  # Имя продукта соответствует названию курса
        type='service'  # Тип продукта (service или good)
    )

    # Создание цены для продукта в Stripe
    price = stripe.Price.create(
        product=product.id,
        unit_amount=summ * 100,  # Сумма в копейках (умножаем на 100)
        currency='usd'  # Валюта (можно изменить на нужную)
    )

    # Создание сессии оплаты в Stripe
    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': price.id,
                'quantity': 1
            }
        ],
        mode='payment',
        success_url='https://127.0.0.1:8000/',  # URL для перенаправления после успешной оплаты
    )
    return session

# def create_stripe_product(name):
#     product = stripe.Product.create(
#         name=name,
#         type="service",
#     )
#     return product["id"]
#
# def create_stripe_price(amount, currency, product_id):
#     stripe_price = stripe.Price.create(
#         unit_amount=amount,
#         currency=currency,
#         product=product_id,
#     )
#     return stripe_price["id"]
#
# def create_stripe_session(stripe_price_id):
#     session = stripe.checkout.Session.create(
#         success_url="https://127.0.0.1:8000/",
#         payment_method=["card"],
#         line_items=[{"price":  stripe_price_id, "quantity": 1}],
#         mode="payment",
#     )
#     return session["url"], session["id"]
#
#



