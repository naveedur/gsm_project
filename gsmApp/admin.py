from django.contrib import admin
from.models import *
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
from import_export import resources,fields
from import_export.fields import Field

def chec(self,instance):
    check=[]
    new=brand.objects.all()
    for p in new:
        check.append(p.title)
    if instance.title in check:
        return True
    else:
       
        return False
   
# brands
class brandResource(resources.ModelResource):
    def skip_row(self, instance, original):
        print(chec(self,instance))
        check=[]
        new=brand.objects.all()
        for p in new:
            check.append(p.title)
        if instance.title in check:
            return True
        else:
            print("no")
            return False
   
    class Meta:
        model = brand
        fields=('id','title')

    
class brandAdmin(ImportExportModelAdmin):
    resource_class = brandResource
    list_display=['id','title']
    search_fields = ['title',]
admin.site.register(brand,brandAdmin)

      
# models
class modelResource(resources.ModelResource):
    def skip_row(self, instance, original):
        check=[]
        new=model.objects.all()
        for p in new:
            check.append(p.title)
        if instance.title in check:
            return True
        else:
            
            return False
    Cat = fields.Field(
        column_name='Cat',
        attribute='Cat',
        widget=ManyToManyWidget(model=category, separator=",", field='title'))

    Brand = fields.Field(
        column_name='Brand',
        attribute='Brand',
        widget=ForeignKeyWidget(brand, 'title'))
    class Meta:
        model = model
        fields=('id','title','Model_code','Chipset','chipset_description','image','Brand','Cat')        

class modelAdmin(ImportExportModelAdmin):
    resource_class = modelResource
    list_display=['sno','title','Model_code','Chipset','chipset_description','Brand','categories']
    search_fields = ['title','Model_code','Chipset',]
    fields=('title','Model_code','Chipset','chipset_description','image','Brand','Cat','slug')
admin.site.register(model,modelAdmin)


# resourceFile
class fileResource(resources.ModelResource):
    def skip_row(self, instance, original):    
        check=[]
        new=resource.objects.all()
        for p in new:
            check.append(p.title)
        if instance.title in check:
            return True
        else:
            return False
    Model = fields.Field(
        column_name='Model',
        attribute='Model',
        widget=ForeignKeyWidget(model, 'title'))
    
    Categories = fields.Field(
        column_name='Categories',
        attribute='Categories',
        widget=ForeignKeyWidget(category, 'title'))

    Brand = fields.Field(
        column_name='Brand',
        attribute='Brand',
        widget=ForeignKeyWidget(brand, 'title'))


    class Meta:
        model = resource
        fields=('id','title','size','Brand','Model','Categories','file','Tags')

class resourceAdmin(ImportExportModelAdmin):
    list_display=('id','title',)
    resource_class = fileResource
admin.site.register(resource,resourceAdmin)         

admin.site.register(user_profile)
admin.site.register(category)
admin.site.register(BlogComment)
admin.site.register(ads)
admin.site.register(socialLinks)
admin.site.register(onsitedata)
admin.site.register(pages)
admin.site.register(subscription)
admin.site.register(pro_Members)
# admin.site.register(MyCustomTag)



class articleAdmin(SummernoteModelAdmin):
    summernote_fields = ('desc',)
    list_display = ("sno","title" )
admin.site.register(article,articleAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ("title","size","Brand", "Model", "Categories","Tag" )

