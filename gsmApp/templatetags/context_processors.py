from gsmApp.models import *
from Adsense.models import *
from subscriptionApp.models import pro_Members
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils import timezone
from django.contrib.auth.models import User


def user_data(request):   
   #  try:
   #   member = pro_Members.objects.get(userName=request.user)
   #   if member.expire_date is not None and member.expire_date < timezone.now():
   #      member.is_active = False
   #      member.save()   
   #   print("hello")
   #   print(member.is_active)   
   #  except pro_Members.DoesNotExist:
   #     pass   
    

    custom_header_page=custom_page.objects.filter(location="header")
    custom_footer_page=custom_page.objects.filter(location="footer")
    


    resourceList=resource.objects.all()
    adsense=adsense_ad.objects.filter(place_at="topBar").first()
    adsense_sideBar=adsense_ad.objects.filter(place_at="sideBar")
    social_links = socialLinks.objects.first()
    notifications=notification.objects.first()
    # Retrieve all social links from the database
    print(social_links)

    return {'social_links': social_links,
            'adsense':adsense,
            'adsense_sideBar':adsense_sideBar,
            'resourceList':resourceList,
            'resourcejsondata':json.dumps(list(resource.objects.values()),cls=DjangoJSONEncoder),
            'notifications':notifications,
            'custom_header_page':custom_header_page,
            'custom_footer_page':custom_footer_page
            }


