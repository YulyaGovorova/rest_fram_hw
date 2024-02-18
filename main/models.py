from django.db import models

from users.models import User
from users.utils import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='education/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')


def __str__(self):
    return f' {self.name}'


class Meta:
    verbose_name = 'Курс'
    verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название урока')
    preview = models.ImageField(upload_to='education/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f' {self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    CHOICES_PAYMENT_METHOD = (
        ('transfer', 'онлайн'),
        ('cash', 'наличные')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    payment_date = models.DateTimeField(verbose_name='дата оплаты', auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    summ = models.PositiveIntegerField(verbose_name='сумма')
    payment_method = (models.CharField(max_length=15, choices=CHOICES_PAYMENT_METHOD,
                                       verbose_name='способ оплаты', default='transfer'))

    def __str__(self):
        return f' {self.user}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
