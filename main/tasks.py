from django.core.mail import send_mail
from celery import shared_task

from config import settings
from main.models import Course, Subscription


@shared_task
def check_update_course(pk):
    """Проверка обновления курса"""
    course = Course.objects.get(pk=pk)
    subscriptions = Subscription.objects.filter(course=pk)

    if subscriptions:
        for subscription in subscriptions:
            send_mail(f"Your subscription on site.",
                      f"Привет, {subscription.user}! Курс {course.name} обновлен!",
                      recipient_list=[subscription.user.email],
                      from_email=settings.EMAIL_HOST_USER)
