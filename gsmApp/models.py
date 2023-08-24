
from distutils.archive_util import make_zipfile
from distutils.command.upload import upload
from email.policy import default
# from tkinter import CASCADE, MULTIPLE
from django.db import models
import uuid
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save,m2m_changed
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext as _
from subscriptionApp.models import *
from django.dispatch import receiver
from tagulous.models import TagField
from taggit.models import Tag


def slug_set(sender, instance, **kwargs):
     instance.slug = slugify(instance.title)
class category(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(default="", blank=True)

    def __str__(self):
     return self.title 


pre_save.connect(slug_set, sender=category)  

class brand(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(default="", blank=True, unique=True)


    def __str__(self):
     return self.title


pre_save.connect(slug_set, sender=brand)     

class model(models.Model):
    sno= models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    Model_code=models.CharField(max_length=100, default="")
    image=models.ImageField(upload_to='images', default='')
    Chipset=models.CharField(max_length=200, default="")
    Cat=models.ManyToManyField(category, blank=True)
    chipset_description=models.CharField(max_length=400, null=True)
    Brand = models.ForeignKey(brand,on_delete=models.CASCADE, default="")
    slug=models.SlugField(default="", blank=True)
    skills = TagField() 
 
    def brandname(self):
        return self.Brand__title
    def categories(self):
        return ",".join([str(p) for p in self.Cat.all()])
    def __str__(self):
     return self.title

pre_save.connect(slug_set, sender=model)   

def get_default_superuser():
    return User.objects.filter(is_superuser=True).first()
class resource(models.Model):
    uploaded_by=models.ForeignKey(User,blank=True, on_delete=models.SET_NULL, null=True)
    title=models.CharField(max_length=100)
    size=models.CharField( max_length=20, default="")
    desc=models.TextField(default="")
    file=models.FileField(default="", blank=True)
    url= models.URLField(max_length=200, blank=True)
    varient=models.CharField(max_length=100, default="")
    Brand = models.ForeignKey(brand,on_delete=models.CASCADE, default="")
    Model = models.ForeignKey(model,on_delete=models.CASCADE, default="")
    Categories = models.ForeignKey(category,on_delete=models.CASCADE, default="")
    update_at=models.DateField(auto_now=True)
    pro=models.BooleanField(default=False)
    verified=models.BooleanField(default=False)
    slug=models.SlugField(default="", unique=True, blank=True)
    tags_char=models.TextField( blank=True)
    Tags = TaggableManager(blank=True) 
    

    
    # def save(self, *args, **kwargs):
    #     tags = [self.Brand, self.Model, self.title]
    #     self.Tags.set("first")
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        check=resource.objects.all()
        if check.count() == 0:
            newid=1
        else:
            getlast=check.last()
            getid=getlast.id
            print(getid)
            newid=int(getid)+1
        if not self.pk:
            self.pk=newid
        
        # tag_names = [self.title, self.varient, self.size]
        # for tag_name in tag_names:
        #     tag, created = Tag.objects.get_or_create(name=tag_name)
        #     self.Tags.add(tag)
        # self.Tags.set("first")
        # self.Tags.add(self.title)
        # self.Tags.add(self.varient)
        tags = [self.title, self.varient,"firmware"]
        for tag in tags:
            if tag not in self.Tags.names():
                self.Tags.add(tag)
        if self.verified and self.pk:
            username = self.uploaded_by
            user = User.objects.get(username=username)
            user_is_staff = user.is_staff
            if not user_is_staff:
                permission=credits_permissions.objects.first()  
                if permission and permission.upload_Resource:  
                  contributer=user_profile.objects.get(username=user)
                  contributer.credits += 1
                  contributer.save()           
                if contributer.referrer_code != "":
                    if permission and permission.referrad_credit_for_resource:
                        referral_user=user_profile.objects.get(referral_code=contributer.referrer_code)
                        referral_user.credits+=1
                        referral_user.save()
                        


        super(resource, self).save(*args, **kwargs)
        
    
# @receiver(pre_save, sender=resource)
# def add_tags(sender, instance, **kwargs):
#     tags=instance.varient
#     instance.Tags.add(tags)

@receiver(m2m_changed, sender=resource.Tags.through)
def add_tags(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        tags = [instance.title, instance.varient,"firmware"]
        for tag in tags:
            if tag not in instance.Tags.names():
                instance.Tags.add(tag)


# @receiver(post_save, sender=resource)
# def add_tags(sender, instance, **kwargs):
#     tags=instance.varient
#     instance.Tags.add(tags)    
      

# @receiver(post_save, sender=resource)
# def tag_set(sender, instance, **kwargs):
#     instance.size = instance.title
#     instance.Tags.add(instance.varient)
#     print(instance.Tags.all())
#     instance.Tags.set(*instance.Tags.all(), clear=True)
#     print(instance.Tags.all())
pre_save.connect(slug_set, sender=resource)


    

class user_profile(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    phoneNomber=models.CharField( max_length=14, blank=True)
    name=models.CharField(max_length=100, blank=True)
    address=models.CharField(max_length=500,blank=True)
    referral_code=models.CharField(max_length=10, default='', blank=True )
    referrer_code=models.CharField(max_length=10, default='', blank=True)
    credits=models.IntegerField(default=0)
    
    def __str__(self):
     return self.username.username
# ads managments  

class ads(models.Model):
    
     CHOICES = (
      ("localads", "local ads"),
      ("adsenseads", "adsense ads"),
      ("affliateads", "affliate ads"),
    )

     adschoice = models.CharField(max_length=15,choices=CHOICES)
     banner_image=models.ImageField(upload_to="ads", blank=True)
     url=models.URLField()
     Time=models.DateTimeField(default=now)
     Timestemp=models.CharField(max_length=3, help_text="in days")

     @property
     def value(self):
        if  self.adschoice=="localads":
            return self.url
        if self.adschoice=="adsenseads":
            return self.banner_image
        else:
            return self.Time  


class  socialLinks(models.Model):
    Facebook_URL=models.URLField(max_length=200, blank=True) 
    Instragram_URL=models.URLField(max_length=200, blank=True) 
    Twitter_URL=models.URLField(max_length=200, blank=True) 
    Youtube_URL=models.URLField(max_length=200, blank=True) 

def get_facebook_url():
        social_links = socialLinks.objects.first()
        return social_links.Facebook_URL 
 


class onsitedata(models.Model):
    Website_Title=models.CharField(max_length=100,blank=True)
    Website_URL=models.URLField(max_length=200, blank=True)
    Website_Logo=models.ImageField(upload_to="logo", blank=True)
    Meta_Description=models.CharField(max_length=300, blank=True)
    Meta_Keywords= models.CharField( max_length=500, blank=True)
    Contact_email=models.EmailField(max_length=50, blank=True)
    Mail_Password=models.CharField(max_length=100, blank=True)

class pages(models.Model):
    page = (
      ("about", "About"),
      ("contact", "Contact"),
      ("refund-policy", "Refund Policy"),
      ("return-policy", "Return Policy"),
      ("privacy-policy", "Privacy Policy"),
      ("cancellation-policy", "Cancellation Policy"),
      ("terms-of-services", "Terms Of Services"),
    )
    
    select_page = models.CharField(max_length=50,choices=page, default='')
    title=models.CharField(max_length=500, default="")
    description=models.TextField()    
    active=models.BooleanField(default=True)   

    def __str__(self):
        return self.title  

class custom_page(models.Model):
    set = (
      ("header", "header"),
      ("footer", "footer"),
    )
    location = models.CharField(max_length=15,choices=set, default='')
    title=models.CharField(max_length=500, default="")
    description=models.TextField()    
    active=models.BooleanField(default=False)  
    slug=models.SlugField(default="",  blank=True)

    def __str__(self):
        return self.title 
pre_save.connect(slug_set, sender=custom_page)



class notification(models.Model):
    message=models.CharField(max_length=300, blank=False)
    time_stemp=models.IntegerField(help_text="enter in days", default=0, blank=False ) 
    created_at = models.DateTimeField(default=timezone.now)

    def is_displayable(self):
        time_elapsed = timezone.now() - self.created_at
        display_duration = timezone.timedelta(days=self.time_stemp)
        return time_elapsed <= display_duration    

    def __str__(self):
        return self.message 

    