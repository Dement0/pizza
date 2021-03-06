from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime

class Pizza(models.Model):
    pizza_name = models.CharField(max_length=25)
    pizza_type = models.CharField(max_length=25)
    pizza_description = models.CharField(max_length=200)
    pizza_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.pizza_name} ({self.pizza_type}) -- {self.pizza_description}"

    class Meta:
        ordering = ['pizza_type']


class Size(models.Model):
    size_text = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.size_text}"


class Topping(models.Model):
    topping_text = models.CharField(max_length=25)
    topping_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.topping_text} ({self.topping_price} €)"

    class Meta:
        ordering = ['topping_price']


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    pizza_count = models.PositiveIntegerField(default=0)
    topping_count = models.PositiveIntegerField(default=0)
    pizza_total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    topping_total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, you have {self.count} items. Total cost: {self.total}"


class Entry(models.Model):
    pizza = models.ForeignKey(Pizza, null=True, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    entry_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        if self.pizza is not None:
            return f"This entry contains {self.quantity} {self.pizza.pizza_name}"
        return f"This entry contains {self.quantity} {self.topping.topping_text}"


@receiver(post_save, sender=Entry)
def update_cart(sender, instance, **kwargs):
    if instance.pizza:
        line_cost = instance.quantity * instance.pizza.pizza_price
        instance.cart.pizza_total += line_cost
        instance.cart.pizza_count += instance.quantity
    elif instance.topping:
        line_cost = instance.quantity * instance.topping.topping_price
        instance.cart.topping_total += line_cost
        instance.cart.topping_count += instance.quantity
    else:
        print("error!")
    instance.cart.total += line_cost
    quantity = int(instance.quantity)
    instance.cart.count += quantity
    instance.cart.updated = datetime.now()
