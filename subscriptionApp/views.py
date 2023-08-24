from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from gsmApp.models import *
from subscriptionApp.models import *
import json
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
today=datetime.date.today()
from .forms import ResourceForm,blogPostForm
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from paypal.standard.forms import PayPalPaymentsForm






def subscriptions(request):
    packages=subscription.objects.all()
   
    data={
        'packages':packages   
    }
    return render(request, 'subscriptionApp/membership.html',data)    

from django.views.decorators.csrf import csrf_exempt  
@csrf_exempt  
def payment_process(request, slug):
    get_subscription=subscription.objects.get(slug=slug)
    
    userName=request.user
    subscription_type=get_subscription
    # print(subscription_type)
    current_date = timezone.now()
    expire_date=current_date+ relativedelta(months=+24)
    active=''
    if current_date > expire_date:
        active=False
    else:
        active=True    
    is_active=active
    # print(is_active)

    save_pro=pro_Members(userName=userName, subscription_type=subscription_type, start_date=current_date, expire_date=expire_date, is_active=is_active)
    save_pro.save()
    pro_profile=user_profile.objects.get(username=userName)
    permission=credits_permissions.objects.first()
    if permission and permission.referrad_credit_for_referrer_subsucription:
       if pro_profile.referral_code !="":
           referred_credit=user_profile.objects.get(referral_code=pro_profile.referrer_code)
           referred_credit.credits+=1
    
    # return redirect('/')
    return JsonResponse('Payment submitted..', safe=False)

def process_payment(request):
    
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '200',
        'item_name': 'subscription',
        
        'currency_code': 'USD',
       'notify_url': 'http://localhost:8000/subscription/paypal/',  
        'return_url': 'http://localhost:8000/subscription/success/',  
        'cancel_return': 'http://localhost:8000/subscription/cancel/',  
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'subscriptionApp/process_payment.html', { 'form': form})

@csrf_exempt
def payment_success(request):
    # Logic to handle successful payment
    return render(request, 'subscriptionApp/payment_success.html')

@csrf_exempt
def payment_cancel(request):
    # Logic to handle canceled payment
    return render(request, 'subscriptionApp/payment_cancel.html')
def payment(request, slug):
    package=subscription.objects.get(slug=slug)
    print(slug)
    packageData = {
        'slug': package.slug,
        'Price': package.Price,
        
    }
    data={
        'slug':slug,
        'package': json.dumps(packageData), 
    }
    return render(request, 'subscriptionApp/payment.html',data) 

def incrementFileCount(request,slug):
    if request.user.is_authenticated:
        try:
            userName = request.user
            pro_member = pro_Members.objects.get(userName=userName)
            Resource=resource.objects.get(slug=slug)
            size=int(Resource.size)
           
            if pro_member.is_active:
                pro_member.data_download = int(pro_member.data_download) + size
                pro_member.files_download = int(pro_member.files_download) + 1 
                print(pro_member.subscription_type.Files_to_download)
                if pro_member.files_download==int(pro_member.subscription_type.Files_to_download) or pro_member.data_download>=int(pro_member.subscription_type.Data_to_download):
                    pro_member.is_active=False   
 
                pro_member.save()
                return JsonResponse({'message': 'File count incremented'})
            else:
                return JsonResponse({'error': 'User is not active'})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'User is not authenticated'})

def single_file_Payment(request,id):
    resourceFile=resource.objects.get(id=id)

    fileData = {
        'slug': resourceFile.slug,
        'id': resourceFile.id,
        
    }
    data={
        "resourceFile":json.dumps(fileData)
    }
    return render(request, 'subscriptionApp/payment.html', data) 

def single_file_payment_process(request,id):
    return JsonResponse('Payment submitted..', safe=False)

def upload_file(request):
    models=model.objects.all()
    categories=category.objects.all()
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            # Redirect to the homepage
            return redirect('/')
    else:
        form = ResourceForm()
    data={
        "models":models,
        "categories":categories,
        "form":form
    }
    return render(request, 'contribution/addFile.html',data)

def upload_brand(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        new_brand = brand(name=brand_name)  # Update variable name to 'new_brand'
        new_brand.save()
        response_data = {'brand_id': new_brand.id, 'brand_name': new_brand.name}
        return JsonResponse(response_data)


def upload_blog_post(request):
    if request.method == "POST":
        form = blogPostForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.uploaded_by = request.user
            article.save()
            return redirect('/')
    else:
        form = blogPostForm()
    data={
        
        "form":form
    }
    return render(request, 'contribution/addBlogPost.html',data)    
# @staff_member_required
# def verify_resource(request, slug):
#     resource = get_object_or_404(resource, slug=slug)
#     resource.verified = True
#     resource.save()

#     # Add one credit to the contributor
#     contributor = resource.contributor
#     contributor.credits += 1
#     contributor.save()

#     # Send an email to the contributor notifying them of the credit
#     email_subject = 'Resource verified'
#     email_body = f'Your resource titled "{resource.title}" has been verified and you have received one credit.\n\nResource details:\nTitle: {resource.title}\nSize: {resource.size}\nDescription: {resource.desc}\nFile: {resource.file}\nURL: {resource.url}\nVarient: {resource.varient}\nBrand: {resource.brand_id}\nModel: {resource.model_id}\nCategory: {resource.category_id}\nTags: {resource.tags}'
#     email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, [contributor.user.email])
#     email.send()

#     return redirect('resource_detail', slug=slug)