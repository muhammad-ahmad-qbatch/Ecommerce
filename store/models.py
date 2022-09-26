from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length= 254, null=True, blank=True)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type','object_id')
    
class Seller(models.Model):
    tags = GenericRelation(Tag)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length= 254, null=True, blank=True)
    password = models.CharField(max_length=50)
    image = models.ImageField(null =True, blank = True)
    name = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)
    def __str__(self):
        return self.name
 
class Product(models.Model):
    tags = GenericRelation(Tag)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=550)
    brand = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField()
    image = models.ImageField(null = True, blank = True)
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
            
class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete= models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        cart_total = sum([items.get_total for items in cartitems])
        return cart_total
    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        items = sum([items.quantity for items in cartitems])
        return items    
    @property
    def get_cart_id(self):
        cartid = self.cartitem_set.get(order = self)
        return cartid.id
class Checkout(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete= models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Cart, on_delete= models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True) #Null should be false in these case but I have to make it true for performing late migrations
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

class Payment(models.Model):
    pass
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Cart, on_delete= models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True, blank=True, default = 0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
   
        