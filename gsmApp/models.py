
from distutils.archive_util import make_zipfile
from distutils.command.upload import upload
from email.policy import default
from tkinter import CASCADE, MULTIPLE
from django.db import models
import uuid

from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext as _
# from taggit.models import TagBase, GenericTaggedItemBase


# class MyCustomTag(TagBase):
#     class Meta:
#         verbose_name = _("Tag")
        # verbose_name_plural = _("Tags")

# class TaggedWhatever(GenericTaggedItemBase):
#     tag = models.ForeignKey(
#         MyCustomTag,
#         on_delete=models.CASCADE,
#         related_name="%(app_label)s_%(class)s_items",
#     )



class category(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(default="", blank=True)

    def __str__(self):
     return self.title 

def slug_set(sender, instance, **kwargs):
     instance.slug = slugify(instance.title)
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
 
    def brandname(self):
        return self.Brand__title
    def categories(self):
        return ",".join([str(p) for p in self.Cat.all()])
    def __str__(self):
     return self.title

pre_save.connect(slug_set, sender=model)     

class resource(models.Model):
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
    slug=models.SlugField(default="", unique=True, blank=True)
    tags_char=models.TextField( blank=True)
    Tags = TaggableManager(blank=True) 

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
        self.tags_char= self.desc+","+self.size
        ans=[self.title ,self.desc,self.size]
        self.Tags.add(*ans)
        print(self.Tags.all())
        for tag in self.tags_char.split(','):
                print(tag)
        super(resource, self).save(*args, **kwargs)
        

 
    def Tag(self):
        return ",".join([str(p) for p in self.Tags.all()] )
    def __str__(self):
     return self.title
def tag_set(sender, instance, **kwargs):
 
    ans=[instance.title ,instance.desc,instance.size]
    instance.tags_char= instance.desc+","+instance.size
    

pre_save.connect(tag_set, sender=resource)
pre_save.connect(slug_set, sender=resource)

def array_tag(instance):
    return [instance.title ,instance.desc]
    

class user_profile(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    phoneNomber=models.CharField( max_length=12, blank=True)
    name=models.CharField(max_length=100, blank=True)
    address=models.CharField(max_length=500,blank=True)


# BLOG models start here
class article(models.Model):
    sno= models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    desc=models.TextField()
    Model=models.ManyToManyField(model, blank=True)
    Brand=models.ManyToManyField(brand, blank=True)
    view_count=models.IntegerField(blank=True , default=0)
    slug=models.SlugField(default="", blank=True) 
    

    class Meta:
        ordering = ('sno',)
    def __str__(self):
        return self.title
   
    def get_absolute_url(self):
     return self.get_url()
pre_save.connect(slug_set, sender=article)     

pre_save.connect(slug_set, sender=article)  
class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True,)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(article, on_delete=models.CASCADE, null=True)
    modelpost=models.ForeignKey(model, on_delete=models.CASCADE, null=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment




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


class onsitedata(models.Model):
    Website_Title=models.CharField(max_length=100,blank=True)
    Website_URL=models.URLField(max_length=200, blank=True)
    Website_Logo=models.ImageField(upload_to="logo", blank=True)
    Meta_Description=models.CharField(max_length=300, blank=True)
    Meta_Keywords= models.CharField( max_length=500, blank=True)
    Contact_email=models.EmailField(max_length=50, blank=True)
    Mail_Password=models.CharField(max_length=100, blank=True)

class pages(models.Model):
    title=models.CharField(max_length=500, default="")
    desc=models.TextField()       

    def __str__(self):
        return self.title


# payment and membership   

class subscription(models.Model):
    # duration_choice = (
    #   ("Monthly", "Monthly"),
    #   ("1 Year", "1 Year"),
    #   ("2 Year", "2 Year"),
    # )
    # Duration = models.CharField(max_length=100,choices=duration_choice)
    display_duration=models.CharField(max_length=300, default="")
    duration=models.IntegerField(blank=True, default=0)
    Price=models.IntegerField(default=0)
    slug=models.SlugField( blank=True)
    Files_to_download=models.IntegerField(default=0)

    def __str__(self):
        return self.display_duration

    def save(self, *args, **kwargs):
        self.slug=slugify(self.display_duration)
        super(subscription, self).save(*args, **kwargs)
            

class pro_Members(models.Model):
    userName=models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(subscription,on_delete=models.CASCADE,  default="")
    start_date=models.DateField(blank=True, null=True)
    expire_date= models.DateField(blank=True, null=True)
    files_download=models.CharField(max_length=50, default="", blank=True)
    is_active=models.BooleanField(default=False)

    