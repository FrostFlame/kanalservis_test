"""Модели приложения web."""
from django.db import models

# Create your models here.


class Order(models.Model):
    """Модель заказа."""
    """Номер заказа"""
    order_number = models.IntegerField(blank=False, null=False, unique=True, verbose_name='Номер заказа')
    """Стоимость в долларах"""
    price_dol = models.IntegerField(blank=False, null=False, verbose_name='Стоимость, $')
    """Срок поставки"""
    date = models.DateField(blank=False, null=False, verbose_name='Дата заказа')
    """Стоимость в рублях по курсу на дату поставки"""
    price_rub = models.IntegerField(blank=False, null=False, verbose_name='Стоимость, руб')


class Chat(models.Model):
    """Модель чата с ботом."""
    """Идентификатор чата с ботом"""
    chat_id = models.IntegerField(blank=False, null=False, verbose_name='ID чата')
