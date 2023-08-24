from django.contrib import admin
from.models import *
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
from import_export import resources,fields
from django_summernote.admin import SummernoteModelAdmin





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
    list_display=("id","title")
    search_fields = ("title","id")
    list_display_links=("title","id")
    
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
    # raw_id_fields = ['Cat']
    
    search_fields = ('title','Model_code','Chipset','Cat__title')
    list_display=('sno','title','Model_code','Chipset','chipset_description','Brand','categories')
   
    list_display_links=("title","sno")
    # list_editable=('t'Model_code','Chipset','Cat__title')
    
    fields=('title','Model_code','Chipset','chipset_description','image','Brand','Cat','slug')
admin.site.register(model,modelAdmin)


# resourceFile
class fileResource(resources.ModelResource):

    def save_model(self, request, obj, form, change):
        obj.save() # Call the save() method of the resource model
        super().save_model(request, obj, form, change)
    def skip_row(self, instance, original, row, index):
        title = instance.title
        existing_instances = resource.objects.filter(title=title)
        if existing_instances.exists():
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
        fields=('id','title','size','Brand','Model','Categories','file','varient')

class resourceAdmin(ImportExportModelAdmin):
    
    resource_class = fileResource
    list_display=('id','title','Brand','Model','varient')
    list_display_links=('id','title')
    list_per_page=15
    ordering=('-id',)
admin.site.register(resource,resourceAdmin)         

# user Profile
class profileAdmin(admin.ModelAdmin):
    list_display=('id','name','phoneNomber','referral_code','credits')
    list_display_links=('name','id','phoneNomber')
admin.site.register(user_profile,profileAdmin)

# category
class categoryAdmin(admin.ModelAdmin):
    list_display=('id','title')
    list_display_links=('id','title')
admin.site.register(category,categoryAdmin)
admin.site.register(ads)


admin.site.register(socialLinks)
admin.site.register(onsitedata)

class pageAdmin(SummernoteModelAdmin):
    summernote_fields=('description')
    
admin.site.register(pages,pageAdmin)

class customPageAdmin(SummernoteModelAdmin):
    summernote_fields=('description')
admin.site.register(custom_page,customPageAdmin)

# admin.site.register(MyCustomTag)



# class articleAdmin(SummernoteModelAdmin):
#     summernote_fields = ('desc',)
#     list_display = ("sno","title" )
# admin.site.register(article,articleAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ("title","size","Brand", "Model", "Categories","Tag" )
    

admin.site.register(notification)

admin.site.ordering = ['category', 'brand', 'model','category']