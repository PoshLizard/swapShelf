from django.contrib.auth.models import User
from django.db import models


class Listing(models.Model):
    CATEGORIES = [
        ("books", "Books"),
        ("electronics", "Electronics"),
        ("furniture", "Furniture"),
        ("bikes", "Bikes"),
        ("other", "Other"),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    status = models.CharField(max_length=12, default="available")
    seller_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Thread(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="threads")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buying_threads")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
