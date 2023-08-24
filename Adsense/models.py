from django.db import models


class adsense_ad(models.Model):
    adsense_places = (
        ('topBar', 'topBar'),
        ('sideBar', 'sideBar'),
    )
    adsense_code=models.TextField(null=True,blank=True)
    place_at=models.CharField(max_length=20, choices=adsense_places)
    adsense_image=models.ImageField(upload_to="adsense", blank=True)
    adsense_url=models.URLField(blank=True)

class shortner_ad(models.Model):
    image=models.ImageField(upload_to="adsense",blank=False)  
    time=models.IntegerField(default=0, blank=False, help_text="The time value should be set in seconds")  

