from datetime import datetime
from django.contrib.auth.models import AbstractUser,BaseUserManager,Group,Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 


class Usermanager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if email is None:
            raise ValueError("email is reqired")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class Customuser(AbstractUser):
    CHOICES = (
        ('admin','Admin'),
        ('customer','Customer'),
        ('seller','Seller')
    ) 
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(choices=CHOICES,max_length=50,default='customer')
    objects = Usermanager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    groups = models.ManyToManyField(
    Group,
    related_name='CustomUser',  # Change this to avoid conflict
    blank=True,
    )

    user_permissions = models.ManyToManyField(
    Permission,
    related_name='CustomUser',  # Change this to avoid conflict
    blank=True,
    )

    def __str__(self):
        return self.email
    

@receiver(post_save, sender=Customuser)
def add_to_group(sender, instance, created, **kwargs):
    if created:
        # Retrieve or create the group based on the role
        if instance.role == 'admin':
            group, created = Group.objects.get_or_create(name='Admins')
            instance.groups.add(group)
        elif instance.role == 'customer':
            group, created = Group.objects.get_or_create(name='Customers')
            instance.groups.add(group)
        elif instance.role == 'seller':
            group, created = Group.objects.get_or_create(name='Sellers')
            instance.groups.add(group)
        
        # Save the changes to the database
        instance.save()




class Profile(models.Model):
    user = models.OneToOneField(Customuser, on_delete = models.CASCADE)
    date_modified = models.DateTimeField(Customuser,auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 =   models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state =  models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    def _str_(self):
        return self.user.email
#Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance)
        user_profile.save()
#Automate the profile thing
post_save.connect(create_profile, sender=Customuser)






class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Seller(models.Model):
    seller_name = models.ForeignKey(Customuser,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.seller_name.username}" 


@receiver(post_save, sender=Customuser)
def add_to_seller(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'seller':
            Seller.objects.create(
                seller_name = instance
            )

      
class Product(models.Model):
    p_name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(upload_to = 'products/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    seller = models.ForeignKey(Seller,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.p_name
    


        




    # def create_superuser(self,email,password=None,**extra_fields):
    #     extra_fields.setdefault('is_staff',True)
    #     extra_fields.setdefault('is_superuser',True)
    #     extra_fields.setdefault('role', 'customer')
    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')
    #     return self.create_user(email, password, **extra_fields)