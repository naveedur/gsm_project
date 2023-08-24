from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# from gsmApp.models import *
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

class subscription(models.Model):
    display_duration=models.CharField(max_length=300, default="")
    duration=models.IntegerField(blank=True, default=0)
    Price=models.IntegerField(default=0)
    slug=models.SlugField( blank=True)
    Files_to_download=models.IntegerField(default=0)
    Data_to_download=models.IntegerField(default=0)
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.display_duration

    def save(self, *args, **kwargs):
        self.slug=slugify(self.display_duration)
        super(subscription, self).save(*args, **kwargs)
            
class Single_File_Price(models.Model):
    price=models.IntegerField(default=0)

    def __str__(self):
        return f"set_price is {str(self.price)}"
class pro_Members(models.Model):
    userName=models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(subscription,on_delete=models.CASCADE,  default="")
    start_date=models.DateTimeField(default=timezone.now)
    expire_date= models.DateTimeField(default=timezone.now)
    files_download=models.IntegerField(default=0,blank=True,null=True)
    data_download=models.IntegerField(default=0, blank=True, null=True)
    is_active=models.BooleanField(default=False)
    

    
    def __str__(self):
        return f"{self.userName.username} subscribed for {self.subscription_type.display_duration}"
    
@receiver(pre_save, sender=pro_Members)
def check_subscription_expiry(sender, instance, **kwargs):
    if instance.expire_date is not None and instance.expire_date < timezone.now():
        instance.is_active = False    


class single_file_payment(models.Model):
    userName=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.ForeignKey("gsmApp.resource",on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.userName.username}"   
    

class user_credit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username   

class credits_permissions(models.Model):
    register=models.BooleanField(default=True, help_text="The user will receive credit when any user registers with his referral code.")
    upload_Resource=models.BooleanField(default=True, help_text="The user will receive credit when they upload a file.")
    upload_blog_post=models.BooleanField(default=True, help_text="The user will receive credit when they upload a post.")  
    referrad_credit_for_resource=models.BooleanField(default=False, help_text="The referred user will receive credit when their referrer upload a file.")  
    referrad_credit_for_blog_post=models.BooleanField(default=False, help_text="The referred user will receive credit when their referrer upload a post.")
    referrad_credit_for_referrer_subsucription=models.BooleanField(default=False, help_text="The referred user will receive credit when their referrer buy subscription.")
    referrad_credit_for_referrer_buying_file=models.BooleanField(default=False, help_text="The referred user will receive credit when their referrer buy a file.")
    
    def __str__(self):
        return "credits permissions"   