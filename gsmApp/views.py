from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# import requests
from.models import *
from subscriptionApp.models import *
from Adsense.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,UpdateUserForm
import json
import uuid
# import os
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime as dt
from django.core.serializers.json import DjangoJSONEncoder
from subscriptionApp.middleWares import DailyDownloadLimitMiddleware  
from django.http import HttpResponse

# from django.http import JsonResponse



import uuid

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            # user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user.username)

            randomCode = str(uuid.uuid4())[:8]
            referralCode=user.username[:2] + randomCode
            userReferral = user_profile(username=user, referral_code=referralCode)
            userReferral.save()
            if request.POST.get('referral'):
                permissions = credits_permissions.objects.first()
                if permissions and permissions.register:
                    referral=request.POST.get('referral')
                    userReferral=user_profile.objects.filter(referral_code=referral).first()
                    userReferral.credits+=1
                    userReferral.save()
                   
                    
        return redirect('login')
    data = {'form': form}
    return render(request, 'firmApp/register.html', data)

def logIn(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        # captcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6Lc678UgAAAAAKEk4w1Nw1rm5t3Wp9DOKhtbpXdP"
        # cap_data={"secret":cap_secret,"response":captcha_token}
        # cap_server_response=requests.post(url=cap_url,data=cap_data)
        # cap_json=json.loads(cap_server_response.text)

        # if cap_json['success']==False:
        #     messages.error(request,"Invalid Captcha Try Again")
        #     return redirect('login')
         
        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
       
     return render(request, 'firmApp/login.html')
def logoutUser(request):
	logout(request)
	return redirect('home')
def social_form(request):
   

    return render(request, 'firmApp/social_form.html')
def socialpassword(request):
    currentuser=request.user
    print('current user name is ')
    print(currentuser)
    print('save it')
    if currentuser.has_usable_password():
            print('userhas pas')
            return redirect('home')
            
    elif request.method == 'POST':
        password = request.POST.get('password')
        print(password)
        currentUser=User.objects.get(username=currentuser)      
        print(currentUser)
        currentUser.set_password(password)
        try:
            currentUser.save()
            return redirect('home')
        except AttributeError:
            print("Couldn't save password")
    return render(request, 'firmApp/auth/socialpassword.html')          

def userProfile(request):
    profile=user_profile.objects.get(username=request.user)
    subscription=pro_Members.objects.filter(userName=request.user).first()
    

    data={
        'userProfile':profile,
        'subscription':subscription
    }
    return render(request, "userDashboard/user_profile.html",data) 
def update_profile(request):
    if request.method=='POST':
        form=UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid:
            form.save()
    else:
        form=UpdateUserForm(instance=request.user)        
    form=UpdateUserForm(instance=request.user)
    data={
        'form':form
    }
    return render(request, 'userDashboard/update_profile.html',data)    

def profile(request):
    resourceList=resource.objects.all()
    userName=request.user
    userProfile=user_profile.objects.all()
    user=userProfile.filter(username=userName).first()
    print(userProfile)

    if request.method=="POST":
        phoneNomber=request.POST.get('phoneNumber')
        name=request.POST.get('Name')
        address=request.POST.get('address')
        username=request.user
        if user:
            user.name=name
            user.phoneNomber=phoneNomber
            user.address=address
            user.save()
        else:
            profile=user_profile(phoneNomber=phoneNomber, name=name, address=address,username=username)
            profile.save()
    data={
        'resourceList':resourceList,
        'user':user
        }  
    return render(request, "userDashboard/profile.html",data)


def home(request):
    adsense=adsense_ad.objects.filter(place_at="topBar").first()
    adsense_sideBar=adsense_ad.objects.filter(place_at="sideBar")
    print(adsense)
    brands=brand.objects.all()
    searchproducts=request.GET.get('Search')
    social_link=socialLinks.objects.all()  
    # print(list(brand.objects.values()) )
    if searchproducts!='' and searchproducts is not None:
        brands=brand.objects.filter(title__icontains=searchproducts)
        
    data={ 
        'jsondata':json.dumps(list(brand.objects.values())),
        'resourcejsondata':json.dumps(list(resource.objects.values()),cls=DjangoJSONEncoder),
        'brands':brands,
        'social_link':social_link
        }
    return render(request, 'firmApp/home.html', data)

def models(request, slug):
    models=model.objects.filter(Brand__slug=slug)   
    print(models)
    data={
        'models':models,
        'brand_slug':slug,
        }
    return render(request, 'firmApp/model.html', data)


def resources(request, slug):
    resourceList=resource.objects.all()
    mod=model.objects.filter(slug=slug)
    query=request.GET.get('search')
    if query!='' and query is not None:
        resources=resource.objects.filter(Model__tile__icontains=query) | resource.objects.filter(varient__icontains=query) | resource.objects.filter(Model__Model_code__icontains=query)

    print(mod)

    Length=[]
    for cat in mod:
        for i in cat.Cat.all():
            Leng=resource.objects.filter(Categories__title=i, Model__slug=slug)
            Leng=len(Leng)
            Length.append(Leng)
  
  
    resources=resource.objects.filter(Model__slug=slug) 

    data={
        
        'mod':mod,
        'resources':resources,
        'model_title':slug,
        'Length':Length,
        'resourceList':resourceList
        }
    return render(request, 'firmApp/resource.html', data)

def catagories(request, mSlug, cSlug):
    resourceList=resource.objects.all()
    mod=model.objects.filter(slug=mSlug)
    resources=resource.objects.filter(Model__slug=mSlug, Categories__slug=cSlug) 
    Length=len(resources)

    data={
        'resources':resources,
        'mod':mod,
        
        'resourceList':resourceList
        }
    return render(request, 'firmApp/resource.html', data)   
                   
@login_required(login_url='/login/')
def download(request, slug):
    Resource=resource.objects.get(slug=slug)

    # Determine if the resource is of type "pro" or not
    is_resource_pro = Resource.pro
    
    # Store the resource type and download limit preference in the session
    request.session['resource_type'] = is_resource_pro
    request.session['response_type'] = 'subscription' if is_resource_pro else 'free'
    request.session.save()



    if request.session.get('download_limit_exceeded', False):
         messages.error(request, "You have reached your daily download limit.")
         del request.session['download_limit_exceeded']  # Clear the flag
         return render(request, 'firmApp/download.html', {"Resource": Resource})
    
    
    pro_members=pro_Members.objects.all()
    shortner_ads=shortner_ad.objects.first()
    
    try:
        user_exist=user_credit.objects.get(user=request.user)
        contributor=True
    except:
        contributor=False    
    user=request.user
    if len(pro_members)>0:
        for i in pro_members:
         if user == i.userName:
          get_pro=i.is_active
         else:
          get_pro=False
    else:
        get_pro=False


    resourceData = {
        'slug': Resource.slug,
    } 
    print(resourceData)    
    data={
        'resource': json.dumps(resourceData,cls=DjangoJSONEncoder), 
        'limitjsondata':json.dumps(list(resource.objects.values()),cls=DjangoJSONEncoder),
        'get_pro':get_pro,
        'Resource':Resource,
        'pro_member':pro_members,
        'contributer':contributor,
        'shortner_ads':shortner_ads
        }
    return render(request, 'firmApp/download.html', data)

def Category(request):
   
    return render(request, 'firmApp/category.html') 

def search(request):
    resourceList=resource.objects.all()
    query=request.GET.get('model')
    models=model.objects.filter(title__icontains=query) | model.objects.filter(Model_code__icontains=query)
    data={
        'models':models,
        'resourceList':resourceList
        }
    return render(request, 'firmApp/search.html', data) 

def returnPolicy(request):
    Return=pages.objects.filter(select_page='return-policy').first()
    data={
        'return':Return
    }
    return render(request, 'firmApp/policies/returnPolicy.html',data)

def refundPolicy(request):
    refund=pages.objects.filter(select_page='refund-policy').first()
    data={
        'refund':refund
    }

    return render(request, 'firmApp/policies/refundPolicy.html',data)

def cancellationPolicy(request):
    cancellation=pages.objects.filter(select_page='cancellation-policy').first()
    data={
        'cancellation':cancellation
    }
    return render(request, 'firmApp/policies/cancellationPolicy.html',data)

def privacyPolicy(request):
    privacy=pages.objects.filter(select_page='privacy-policy').first()
    data={
        'privacy':privacy
    }
    return render(request, 'firmApp/policies/privacyPolicy.html',data)

def termsOfServices(request):
    terms=pages.objects.filter(select_page='terms-of-services').first()
    data={
        'terms':terms
    }
    return render(request, 'firmApp/policies/termsOfServices.html',data)

def contactUs(request):
    contact=pages.objects.filter(select_page='contact').first()
    data={
        'contact':contact
    }
    return render(request, 'firmApp/companyInfo/contactUs.html',data)   

def aboutUs(request):
    about=pages.objects.filter(select_page='about').first()
    
    data={
        'about':about
    }
    return render(request, 'firmApp/companyInfo/aboutUs.html',data)    

def customPage(request, slug):
    page=custom_page.objects.get(slug=slug)

    data={
        'page':page
    } 
    return render(request, 'firmApp/customPages/customPageBasic.html',data)


# def basic(request):
#     resourceList=resource.objects.all()
#     social_link=socialLinks.objects.all()
#     onsite_data=onsitedata.objects.all()
#     data={
        
#         'resourceList':resourceList,
#         'social_link':social_link,
#         'onsite_data':onsite_data
#         }
#     return render(request, 'firmApp/basic.html', data)    


      

# def dashboard(request):
    
#     print(request.user.username)
#     userprofile=user_profile.objects.get(username=request.user)
#     data={
#         'userprofile':userprofile,
            
#         }  
#     return render(request, "firmApp/blog/profile.html",data) 


# def adminHome(request):
#     resources=resource.objects.all()
#     data={
#         'length':len(resources)
#     }
#     return render( request, "admin/index.html", data)