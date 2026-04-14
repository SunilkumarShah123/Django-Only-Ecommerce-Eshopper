from django.db import models
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
             email = f"{extra_fields.get('username')}@github.local"
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
    


class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    subname=models.CharField(max_length=100,unique=True)
    cate=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_category')
    sub_slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subname
    
class Brand(models.Model):
    title=models.CharField(max_length=100,blank=True)
    brand_slug=models.SlugField(max_length=100,unique=True,blank=True,null=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category        = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.sub_category.sub_slug,self.brand.brand_slug,self.slug,])
    
class carsousel(models.Model):
    heading=models.CharField(max_length=100)
    subheading=models.CharField(max_length=200)
    short_description=models.TextField(max_length=300,blank=True)
    image=models.ImageField(upload_to='photos/carousel')
    carsousel_product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=150)
    phone_number = PhoneNumberField(region="NP",unique=True)  # Nepal
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

class Comment(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     comment=models.CharField(max_length=255)
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)

     def __str__ (self):
        return self.title
     
     class Meta:
        verbose_name_plural='Comments'


class Order(models.Model):
    product = models.CharField(max_length=200)
    email=models.EmailField()
    full_name=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    total = models.CharField(max_length=200)
    image = models.ImageField(upload_to="order_images")
    phone = models.CharField(max_length=200)
    full_address = models.CharField(max_length=200)
    is_pay = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    order_notes=models.TextField()

    def __str__(self):
        return self.product
    
