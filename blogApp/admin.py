from django.contrib import admin
from.models import *
from django_summernote.admin import SummernoteModelAdmin




class articleAdmin(SummernoteModelAdmin):
    summernote_fields = ('desc',)
    list_display = ("title" ,"uploaded_by","Model","verified" )
    list_editable=("verified",)
    search_fields = ("title","uploaded_by","Model")
    
admin.site.register(article,articleAdmin)

class commentAdmin(admin.ModelAdmin):
    list_display=("user","comment","post","modelpost","categorypost","parent")
    search_fields = ("user","comment","post","modelpost","categorypost","parent")
admin.site.register(BlogComment,commentAdmin)
