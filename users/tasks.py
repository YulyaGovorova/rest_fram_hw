from celery import shared_task
from datetime import datetime, timedelta, timezone
from users.models import User


@shared_task
def check_user_activity():
    """Проверка непосещения сайта пользователем более 30 дней"""
    for user in User.objects.filter(is_active=True):
        if user.last_login:
            if datetime.now(timezone.utc) - timedelta(days=30) > user.last_login:
                user.is_active = False
                user.save()