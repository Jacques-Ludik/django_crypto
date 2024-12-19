from django.db import models

# Create your models here.
class CryptoPrice(models.Model):
    crypto_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto_name}: {self.price}"
