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

    def total_price(self):
        if self.item.offer_price:
            return self.item.offer_price * self.quantity
        return self.item.price * self.quantity



from django.db import models

class SpecialItem(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='special_items/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
