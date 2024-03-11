from django.db import models
from django.urls import reverse

from topfood.settings import AUTH_USER_MODEL


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Plat(models.Model):
    name = models.CharField(max_length=200)

    # slug = models.SlugField(max_length=200)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='category', null=True, on_delete=models.SET_NULL)
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)
    best = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plat", kwargs={"id": self.id})


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.plat} ({self.quantity})'

    def calculate_balance(self):
        return self.plat.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def cart_balance(self):
        balance = 0
        for order in self.orders:
            balance += order.calculate_balance()
        return balance


class DeliveryPrice(models.Model):
    price = models.IntegerField(default=800)

    def __str__(self):
        return f'Livraison : {self.price} FCFA'
