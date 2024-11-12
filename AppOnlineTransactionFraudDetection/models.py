from django.db import models

class User_details(models.Model):
    user_id = models.CharField(max_length=20)
    Card_number = models.IntegerField(default=None)
    cvv = models.IntegerField(default=None)
    Expirydate = models.CharField(max_length=10)
    mobile = models.IntegerField(default=None)
    MaxTransAmount = models.IntegerField(default=None)
    Securityquestion1 = models.CharField(default=None,max_length=500)
    Securityanswer1 = models.CharField(default=None,max_length=200)
    Securityquestion2 = models.CharField(default=None,max_length=500)
    Securityanswer2 = models.CharField(default=None,max_length=200)
    Securityquestion3 = models.CharField(default=None,max_length=500)
    Securityanswer3 = models.CharField(default=None,max_length=200)
    attempts = models.IntegerField(default=0)
    status = models.CharField(max_length=200,default='Unblocked')
    
    
    class Meta:
        db_table = 'user_details'  


class Products(models.Model):
    Pid = models.CharField(max_length=200)
    pname = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    subcategory = models.CharField(max_length=10)
    cost = models.IntegerField(default=None)
    desc = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img/images')
    
    class Meta:
        db_table = 'products'  


class Card_details(models.Model):
    Cid = models.CharField(max_length=20)
    Uid = models.CharField(max_length=20)
    card_type = models.CharField(max_length=200)
    cardno = models.CharField(max_length=200)
    cvv = models.CharField(max_length=10)
    expiry = models.CharField(max_length=200)
    mobile = models.CharField(max_length=11)
    Email = models.EmailField()
    password = models.CharField(max_length=200)
    amount = models.IntegerField(default=None)
    
    class Meta:
        db_table = 'card_details'



class Order_details(models.Model):
    Tid = models.CharField(max_length=20)
    Uid = models.CharField(max_length=20)
    TotalAmount = models.IntegerField(null=True,default=None)
    date = models.CharField(max_length=200)
    productList = models.CharField(max_length=500,default=None)
    quantity = models.CharField(max_length=200,default=None)    
    status = models.CharField(max_length=200,default=None)

    
    class Meta:
        db_table = 'order_details'


class Cart(models.Model):
    Pid = models.CharField(max_length=20)
    Pname = models.CharField(max_length=200)
    qty = models.IntegerField(default=None)
    cost = models.IntegerField(default=None)
    Uid = models.CharField(max_length=200)
    total = models.IntegerField(default=None)
    category = models.CharField(max_length=200)
      
    class Meta:
        db_table = 'cart'


class Admin_details(models.Model):
    Aid = models.CharField(max_length=20)
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = 'admin_details'


class Blockrequest(models.Model):
    user_id = models.CharField(max_length=20)
    Card_number = models.IntegerField(default=None)
    cvv = models.IntegerField(default=None)
    Issue = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'blockrequest' 

