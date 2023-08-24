from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from gsmApp.models import *

def slug_set(sender, instance, **kwargs):
     instance.slug = slugify(instance.title)
class article(models.Model):
    sno= models.AutoField(primary_key=True)
    uploaded_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title=models.CharField(max_length=200)
    desc=models.TextField()
    Model=models.ForeignKey(model, on_delete=models.SET_NULL, null=True )
    # Brand=models.ManyToManyField(brand, blank=True)
    verified=models.BooleanField(default=False)
    view_count=models.IntegerField(blank=True , default=0)
    slug=models.SlugField(default="", blank=True)

    def save(self, *args, **kwargs):
       
        if self.verified and self.pk:
            username = self.uploaded_by
            user = User.objects.get(username=username)
            user_is_staff = user.is_staff
            if not user_is_staff:
                permission=credits_permissions.objects.first()  
                if permission and permission.upload_blog_post:  
                  contributer=user_profile.objects.get(username=user)
                  contributer.credits += 1
                  contributer.save()           
                if contributer.referrer_code != "":
                    if permission and permission.referrad_credit_for_blog_post:
                        referral_user=user_profile.objects.get(referral_code=contributer.referrer_code)
                        referral_user.credits+=1
                        referral_user.save()
                        


        super(article, self).save(*args, **kwargs)
    

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
    categorypost=models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment

