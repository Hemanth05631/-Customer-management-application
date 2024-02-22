from django.db import models
from django.contrib.auth.models import User

class customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    # CASCADE meaning is whenever the user is deleted then its relation is also deleted in customer
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    profile_pic = models.ImageField(default='default_image.jpg',null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else ' '

class Tag(models.Model):

    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor')
    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    description = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name




class order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('out for delivery','out for delivery'),
        ('Delivered','Delivered')
    )

    customer = models.ForeignKey(customer,null=True,on_delete=models.SET_NULL)
    note = models.CharField(max_length=1000,null=True,blank=True)
    product = models.ForeignKey(product,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)

    def __str__(self):
        return str(self.product.name) if self.product else ''
     
    



# Create your models here.
