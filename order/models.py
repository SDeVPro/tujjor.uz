from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from product.models import Product,Variants

class ShopCart(models.Model):#savatcha modeli
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    variant = models.ForeignKey(Variants,on_delete=models.SET_NULL, blank=True,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title
    @property
    def price(self):
        return (self.product.price)
    @property
    def amount(self):
        return (self.quantity * self.product.price)
    @property
    def varamount(self):
        return (self.quantity*self.variant.price)

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']

class Order(models.Model):
    STATUS = (
        ('New','Yangi'),
        ('Accepted','Qabul qilingan'),
        ('OnShipping','Xarid junatish '),
        ('Completed','Tugallangan'),
        ('Cancelled','Bekor qilingan!'),
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=15, editable=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    total = models.FloatField()
    status = models.CharField(max_length=150, choices=STATUS,default='New')
    ip = models.CharField(max_length=150, blank=True)
    adminnote = models.CharField(max_length=150, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    
class OrderForm(ModelForm):
    class Meta:
        model = Order 
        fields = ['first_name','last_name','address','phone','city','country']
    

class OrderProduct(models.Model):
    STATUS = (
        ('New','Yaxshi'),
        ('Accepted','Qabul qilingan'),
        ('Cancelled','Bekor qilingan'),
        )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=150, choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title