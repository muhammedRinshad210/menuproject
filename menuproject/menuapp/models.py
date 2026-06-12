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
    

class SpecialCart(models.Model):
    item = models.ForeignKey(SpecialItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    session_key = models.CharField(max_length=100, null=True, blank=True)

    def total_price(self):
        if self.item.offer_price:
            return self.item.offer_price * self.quantity
        return self.item.price * self.quantity


    

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
        qr_data = f"https://byte-studio-menu.onrender.com/table/{self.table_number}/"

        qr = qrcode.make(qr_data)
        canvas = BytesIO()
        qr.save(canvas, format='PNG')

        file_name = f'table_{self.table_number}.png'
        self.qr_code.save(file_name, File(canvas), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table_number}"



# offer 

class Offer(models.Model):
    message = models.CharField(max_length=300)
    speed = models.CharField(max_length=10, choices=[
        ('slow','Slow'),
        ('medium','Medium'),
        ('fast','Fast')
    ], default='medium')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message





class Order(models.Model):
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def subtotal(self):
        return self.price * self.quantity
