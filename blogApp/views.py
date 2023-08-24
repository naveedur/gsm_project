from django.shortcuts import render,redirect
from gsmApp.models import *
from blogApp.models import *
from django.db.models import Q
from django.http import JsonResponse

def bloghome(request):
    
    models=model.objects.all()
    blogs=article.objects.all().order_by('-sno')
    data={
        'blogs':blogs,
        'models':models
        }
    return render(request, "blogApp/home.html", data)
    # return JsonResponse({'message': 'File count incremented','brands':list(brand.objects.values())})

def models(request,slug):
    brands=brand.objects.all()
    mod=model.objects.get(slug=slug)
    # mod=model.objects.filter(Brand=Bran)

    # blogs=article.objects.all()
    data={
        'mod':mod,
        'brands':brands
        }
    return render(request, "blogApp/home.html", data)    

  

def articles(request,mTitle,cTitle):
    Mod=model.objects.get(slug=mTitle)
    cat=category.objects.get(slug=cTitle)
    print(Mod)
    # Resources=resource.objects.filter()
    resources = resource.objects.filter(Q(Categories__slug=cTitle) & Q(Model=Mod))
    brands=brand.objects.all()
   
    # resources=resource.objects.filter(Model=Mod)
    comments= BlogComment.objects.filter(modelpost=Mod, categorypost=cat, parent=None)
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
        'cat':cat,
        'brands':brands,
        'comments':comments,
        'replyDict':replyDict,
        }
    return render(request, "blogApp/article.html", data)   

def solution_articles(request):
    brands=brand.objects.all()
    solution=article.objects.all().order_by('-sno')[:1]
    data={
    'solution':solution,
    'brands':brands
    }
    return render(request, "blogApp/home.html", data) 

def article_solution(request,Title):
    mod=model.objects.get(title=Title)
    solution=article.objects.filter(Model=mod)
    print(solution)
    
    data={
    'solution':solution,
    }
    return render(request, "blogApp/article_solution.html", data)      
def popular_artiles(request):
    mostPopular=article.objects.all().order_by('-view_count')[:5]
    brands=brand.objects.all()
    data={
        'mostPopular':mostPopular,
        'brands':brands
        
    }
    return render(request, "blogApp/home.html", data) 
def articlepage(request,postSlug):
    brands=brand.objects.all()
    solution=article.objects.get(slug=postSlug)
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
    return render(request, "blogApp/article.html", data)   

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get("postSno")
        modelSno=request.POST.get("modelSno")
        categoryId=request.POST.get("categoryId")
        if postSno!='' and postSno is not None:
            post= article.objects.get(sno=postSno)
            a="post"
        else:    
            modelpost=model.objects.get(sno=modelSno)
            categorypost=category.objects.get(id=categoryId)  
            a="modelpost"        
        parentSno= request.POST.get('parentSno')
        print(parentSno)
        if parentSno =="":
            if a=="post":
                comment=BlogComment(comment= comment, user=user, post=post)
            else:
                comment=BlogComment(comment= comment, user=user, modelpost=modelpost,categorypost=categorypost )    
            comment.save()
            # messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            if a== "post":
             comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            else:
             comment=BlogComment(comment= comment, user=user, modelpost=modelpost ,categorypost=categorypost, parent=parent)
            comment.save()
            # messages.success(request, "Your reply has been posted successfully")
    if a=="post":    
     return redirect(f"/blog/article/{post.slug}")
    else:
     return redirect(f"/blog/{modelpost.slug}/{categorypost.slug}")    
