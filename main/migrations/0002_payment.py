# Generated by Django 4.0 on 2024-02-18 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_remove_user_username_user_avatar_and_more'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')),
                ('summ', models.PositiveIntegerField(verbose_name='сумма')),
                ('payment_method', models.CharField(choices=[('transfer', 'онлайн'), ('cash', 'наличные')], default='transfer', max_length=15, verbose_name='способ оплаты')),
                ('paid_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('paid_lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.lesson')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]
