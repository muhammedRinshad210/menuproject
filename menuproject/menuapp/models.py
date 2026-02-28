from django.db import models

class Carousel(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='carousel/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='menu/')
    
    quantity = models.IntegerField(default=0)   # ✅ stock quantity



class Cart(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    session_key = models.CharField(max_length=100, null=True, blank=True)

    def total_price(self):
        if self.item.offer_price:
            return self.item.offer_price * self.quantity
        return self.item.price * self.quantity



from django.db import models

class SpecialItem(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='special_items/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # ✅ NEW
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

from django.db import models




from django.db import models

class ChatMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(default=0)   # ⭐ Add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# qr section : 

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='table_qr/', blank=True, null=True)

    def save(self, *args, **kwargs):
        qr_data = f"http://127.0.0.1:8000/table/{self.table_number}/"

        qr = qrcode.make(qr_data)
        canvas = BytesIO()
        qr.save(canvas, format='PNG')

        file_name = f'table_{self.table_number}.png'
        self.qr_code.save(file_name, File(canvas), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table_number}"



