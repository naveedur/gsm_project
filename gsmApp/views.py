from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import requests
from.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,UpdateUserForm
import json
import os
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from datetime import timedelta
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from django.core.serializers.json import DjangoJSONEncoder

today=datetime.date.today()
def social_form(request):
   

    return render(request, 'firmApp/social_form.html')
def register(request):
		form = CreateUserForm()
		if request.method == 'POST':    
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('login')
		data = {'form':form}
		return render(request, 'firmApp/register.html', data) 

def logIn(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        captcha_token=request.POST.get("g-recaptcha-response")
        cap_url="https://www.google.com/recaptcha/api/siteverify"
        cap_secret="6Lc678UgAAAAAKEk4w1Nw1rm5t3Wp9DOKhtbpXdP"
        cap_data={"secret":cap_secret,"response":captcha_token}
        cap_server_response=requests.post(url=cap_url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)

        if cap_json['success']==False:
            messages.error(request,"Invalid Captcha Try Again")
            return redirect('login')
         
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
       
     return render(request, 'firmApp/login.html')
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
def logoutUser(request):
	logout(request)
	return redirect('home')



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
    return render(request, 'firmApp/update_profile.html',data)    

# class home(ListView):
    
#     template_name='firmApp/home.html'

#     def get_context_data(self, **keywargs):
#         resourceList=resource.objects.all()
#         brands=brand.objects.all()
#         social_link=socialLinks.objects.all() 
#         context=super().get_context_data(**keywargs)
#         context["qs_query"]=json.dumps(list(brand.objects.values()))
#         data={
#             'context':context,
#             'brands':brands,
#         # 'Mods':Mods,
#           'resourceList':resourceList,
#         'social_link':social_link
#         }    
    
#         return data

def home(request):
    resourceList=resource.objects.all()
    brands=brand.objects.all()
    searchproducts=request.GET.get('Search')
    social_link=socialLinks.objects.all()  
    print(list(brand.objects.values()) )
    if searchproducts!='' and searchproducts is not None:
        brands=brand.objects.filter(title__icontains=searchproducts)
        
    data={
        'jsondata':json.dumps(list(brand.objects.values())),
        'resourcejsondata':json.dumps(list(resource.objects.values()),cls=DjangoJSONEncoder),

        'brands':brands,
        'resourceList':resourceList,
        'social_link':social_link
        }
    return render(request, 'firmApp/home.html', data)

def models(request, slug):
    resourceList=resource.objects.all()
    models=model.objects.filter(Brand__slug=slug)   
    print(models)
    data={
        'models':models,
        'brand_slug':slug,
        'resourceList':resourceList
        }
    return render(request, 'firmApp/model.html', data)


def search(request):
    resourceList=resource.objects.all()
    query=request.GET.get('model')
    models=model.objects.filter(title__icontains=query) | model.objects.filter(Model_code__icontains=query)
    data={
        'models':models,
        'resourceList':resourceList
        }
    return render(request, 'firmApp/search.html', data) 



      

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

def catagories(request, mTitle, cTitle):
    resourceList=resource.objects.all()
    mod=model.objects.filter(title=mTitle)
    resources=resource.objects.filter(Model__title=mTitle, Categories__title=cTitle) 
    Length=len(resources)

    data={
        'resources':resources,
        'mod':mod,
        'model_title':mTitle,
        'resourceList':resourceList
        }
    return render(request, 'firmApp/resource.html', data)   
                   
@login_required(login_url='/login/')
def download(request, slug):
    # resourceList=resource.objects.all()
    Resource=resource.objects.get(slug=slug)
    pro_members=pro_Members.objects.all()
    
    user=request.user
    if len(pro_members)>0:
        for i in pro_members:
         if user == i.userName:
          get_pro=i.is_active
         else:
          get_pro=False
    else:
        get_pro=False
         
    data={
        'limitjsondata':json.dumps(list(resource.objects.values()),cls=DjangoJSONEncoder),
        'get_pro':get_pro,
        'Resource':Resource,
        # 'resourceList':resourceList,
        'pro_member':pro_members,
        }
    return render(request, 'firmApp/download.html', data)

def membership(request):
    packages=subscription.objects.all()
   
    data={
        'packages':packages   
    }
    return render(request, 'firmApp/subscription/membership.html',data)    
def usermembership(request, slug):
    get_subscription=subscription.objects.get(slug=slug)
    
    userName=user=request.user
    subscription_type=get_subscription
    print(subscription_type)
    start_date=dt.now().date()
    expire_date=dt.now().date()+ relativedelta(months=+24)
    active=''
    if today > expire_date:
        active=False
    else:
        active=True    
    is_active=active
    print(is_active)

    save_pro=pro_Members(userName=userName, subscription_type=subscription_type, start_date=start_date, expire_date=expire_date, is_active=is_active)
    save_pro.save()
    return redirect('/')
def payment(request, slug):
    data={
        'slug':slug   
    }
    return render(request, 'firmApp/subscription/payment.html',data) 

def Category(request):
   
    return render(request, 'firmApp/category.html') 

def basic(request):
    resourceList=resource.objects.all()
    social_link=socialLinks.objects.all()
    onsite_data=onsitedata.objects.all()
    data={
        'resourcejsondata':json.dumps(list(resource.objects.values()),cls=DjangoJSONEncoder),
        'resourceList':resourceList,
        'social_link':social_link,
        'onsite_data':onsite_data
        }
    return render(request, 'firmApp/basic.html', data)    


def profile(request):
    resourceList=resource.objects.all()
    if request.method=="POST":
        phoneNomber=request.POST.get('phoneNumber')
        name=request.POST.get('Name')
        address=request.POST.get('address')
        username=request.user
        profile=user_profile(phoneNomber=phoneNomber, name=name, address=address,username=username)
        profile.save()
    data={
        'resourceList':resourceList
        }  
    return render(request, "firmApp/auth/profile.html",data)

def userProfile(request):
    resourceList=resource.objects.all()
    data={
        'resourceList':resourceList
        }
    return render(request, "firmApp/auth/user_profile.html",data)       

def dashboard(request):
    resourceList=resource.objects.all()
    print(request.user.username)
    userprofile=user_profile.objects.get(username=request.user)
    data={
        'userprofile':userprofile,
        'resourceList':resourceList
        
        }  
    return render(request, "firmApp/blog/profile.html",data) 


    
    # return render(request, f"{i.title}.html")      
    


# blogs function
def blogs(request):
    brands=brand.objects.all()
    blogs=article.objects.all().order_by('-sno')
    data={
        'blogs':blogs,
        'brands':brands
        }
    return render(request, "firmApp/blog/home.html", data)

def mod(request,Title):
    brands=brand.objects.all()
    Bran=brand.objects.get(title=Title)
    mod=model.objects.filter(Brand=Bran)

    # blogs=article.objects.all()
    data={
        'mod':mod,
        'brands':brands
        }
    return render(request, "firmApp/blog/home.html", data)    

  

def articles(request,slug):
    Mod=model.objects.get(slug=slug)
    brands=brand.objects.all()
   
    resources=resource.objects.filter(Model=Mod)
    comments= BlogComment.objects.filter(modelpost=Mod, parent=None)
    replies= BlogComment.objects.filter(modelpost=Mod).exclude(parent=None)
    

    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    data={
        'resources':resources,
        'Mod':Mod,
        'brands':brands,
        'comments':comments,
        'replyDict':replyDict,
        }
    return render(request, "firmApp/blog/article.html", data)   

def solution_articles(request):
    brands=brand.objects.all()
    solution=article.objects.all().order_by('-sno')[:1]
    data={
    'solution':solution,
    'brands':brands
    }
    return render(request, "firmApp/blog/home.html", data) 

def article_solution(request,Title):
    mod=model.objects.get(title=Title)
    solution=article.objects.filter(Model=mod)
    print(solution)
    
    data={
    'solution':solution,
    }
    return render(request, "firmApp/blog/article_solution.html", data)      
def popular_artiles(request):
    mostPopular=article.objects.all().order_by('-view_count')[:5]
    brands=brand.objects.all()
    data={
        'mostPopular':mostPopular,
        'brands':brands
        
    }
    return render(request, "firmApp/blog/home.html", data) 
def articlepage(request,slug):
    brands=brand.objects.all()
    solution=article.objects.get(slug=slug)
    solution.view_count=solution.view_count+1
    solution.save()
    comments= BlogComment.objects.filter(post=solution, parent=None)
    replies= BlogComment.objects.filter(post=solution).exclude(parent=None)
    
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    data={
        'solution':solution,
        'comments':comments,
        'replyDict':replyDict,
        'brands':brands
    }
    return render(request, "firmApp/blog/article.html", data)   

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get("postSno")
        modelSno=request.POST.get("modelSno")
        if postSno!='' and postSno is not None:
            post= article.objects.get(sno=postSno)
            a="post"
        else:    
            modelpost=model.objects.get(sno=modelSno)
            a="modelpost"        
        parentSno= request.POST.get('parentSno')
        print(parentSno)
        if parentSno =="":
            if a=="post":
                comment=BlogComment(comment= comment, user=user, post=post)
            else:
                comment=BlogComment(comment= comment, user=user, modelpost=modelpost )    
            comment.save()
            # messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            if a== "post":
             comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            else:
             comment=BlogComment(comment= comment, user=user, modelpost=modelpost , parent=parent)
            comment.save()
            # messages.success(request, "Your reply has been posted successfully")
    if a=="post":    
     return redirect(f"/articl/{post.slug}")
    else:
     return redirect(f"/article/{modelpost.slug}")    

