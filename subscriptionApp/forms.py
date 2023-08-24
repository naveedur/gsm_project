
from django import forms
from gsmApp.models import *
from blogApp.models import article
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from taggit.forms import TagField
from django_summernote.widgets import SummernoteWidget

# class ResourceForm(forms.ModelForm):
#     class Meta:
#         model = resource
#         fields = '__all__'
        # widgets = {
        #     'Brand': ModelSelect2Widget(
        #         model=brand,
        #         search_fields=['name__icontains'],
        #         new_item_label='Add new brand'
        #     ),
        # }
        # fields = ['title', 'size', 'desc','url','varient','Model','Categories','Tags']


    
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from taggit.forms import TagField
from gsmApp.models import brand, model, category, resource
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.urls import reverse_lazy


# class RawIdWidget(forms.TextInput):
#     template_name = 'templates/subscriptionApp/raw_id_widget.html'

#     def __init__(self, model, *args, **kwargs):
#         self.model = model
#         super().__init__(*args, **kwargs)

#     def get_url(self):
#         return reverse('admin:%s_%s_add' % (
#             self.model._meta.app_label, self.model._meta.model_name
#         ))

#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, value, attrs)
#         context['widget']['url'] = self.get_url()
#         return context


class BrandForm(forms.ModelForm):
    class Meta:
        model = brand
        fields = '__all__'


class ModelForm(forms.ModelForm):
    class Meta:
        model = model
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'


class ResourceForm(forms.ModelForm):
   class Meta:
        model = resource
        fields = '__all__'
#         widgets = {
#             'Brand': ForeignKeyRawIdWidget(
#                 rel=brand._meta.get_field('id').remote_field,
#                 # admin_site=admin.site,
#                 attrs={
#                     'class': 'vForeignKeyRawIdAdminField',
#                     'data-popup-url': reverse_lazy('create-brand')
#                 }
#             ),
#             'Model': ForeignKeyRawIdWidget(
#                 rel=model._meta.get_field('id').remote_field,
#                 # admin_site=admin.site,
#                 attrs={'class': 'vForeignKeyRawIdAdminField'}
#             ),
#             'Categories': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
#             'Tags': forms.TextInput(attrs={'class': 'form-control'}),
#         }

#    def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['Brand'].widget.can_add_related = True
# class Media:
#         js = ('js/resource_form.js',)

class blogPostForm(forms.ModelForm):
    desc = forms.CharField(widget=SummernoteWidget())
    
    class Meta:
        model=article
        fields=['title','desc','Model']