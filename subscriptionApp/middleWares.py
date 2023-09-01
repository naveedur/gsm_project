from datetime import date
from .models import daily_download_limit, pro_Members, free_files_permissions

class DailyDownloadLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.user.is_authenticated:
            user = request.user

            daily_download = daily_download_limit.objects.filter(user=user).first()

            # Reset the download count if needed
            daily_download.reset_count_if_date_changed()

            resource_type = request.session.get('resource_type', False)
            response_type = request.session.get('response_type', 'subscription')

            has_subscription = pro_Members.objects.filter(userName=user, is_active=True).first()
            
            if has_subscription:
                user_subscription = pro_Members.objects.get(userName=user, is_active=True)
                if response_type == 'subscription':
                    download_limit = user_subscription.subscription_type.daily_download_limit
                    if daily_download.subscription_downloads >= download_limit:
                        request.session['download_limit_exceeded'] = True
                    else:
                        request.session['download_limit_exceeded'] = False
                else:
                    free_files_permission = free_files_permissions.objects.first()
                    download_limit = free_files_permission.daily_download_limit
                    if daily_download.free_file_downloads >= download_limit:
                        request.session['download_limit_exceeded'] = True
                    else:
                        request.session['download_limit_exceeded'] = False

            else:
                free_files_permission = free_files_permissions.objects.first()
                download_limit = free_files_permission.daily_download_limit
                if response_type == 'subscription':
                    request.session['download_limit_exceeded'] = False
                elif daily_download.free_file_downloads >= download_limit:
                    request.session['download_limit_exceeded'] = True
                else:
                    request.session['download_limit_exceeded'] = False

        response = self.get_response(request)
        return response
