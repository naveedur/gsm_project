from datetime import date
from django.utils import timezone
from .models import pro_Members
# from celery import shared_task

# @shared_task
def update_membership_status():
    expired_members = pro_Members.objects.filter(expire_date__lt=timezone.now(), is_active=True)
    expired_members.update(is_active=False)