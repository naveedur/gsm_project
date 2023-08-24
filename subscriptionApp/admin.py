from django.contrib import admin
from subscriptionApp.models import *

# subscription
class subscriptionAdmin(admin.ModelAdmin):
    list_display=("display_duration","Price","Files_to_download",'Data_to_download',"active")
    list_display_links=('display_duration',)
    list_editable=('Price','Files_to_download','Data_to_download','active')
admin.site.register(subscription,subscriptionAdmin)
admin.site.register(Single_File_Price)
admin.site.register(pro_Members)
admin.site.register(single_file_payment)


admin.site.register(user_credit)
admin.site.register(credits_permissions)
