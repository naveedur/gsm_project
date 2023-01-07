from unicodedata import name
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


from.views import *
from.import views

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),

    path('', home, name="home"),
    
    path('brand/<slug>/', models, name='models'),
    path('model/<slug>/', resources, name='resources'),
    path('login/', logIn, name='login'),
    path('socialpassword/',socialpassword, name='socialpassword'),
    path('register/', register, name='register'),
    path('logout/', logoutUser, name="logout"),
    path('Update_profile/',update_profile, name="update_profile"),
    path('social_form/',social_form, name="social_form"),
    path('download/<slug>/', download, name='download'),
    path('membership/', membership, name='membership'),
    path('membership/<slug>/', usermembership, name='usermembership'),
    path('payment/<slug>/', payment, name="payment"),
    path('category/', Category, name='category'),
    path('search/', search, name='search'),
    path('basic/', basic, name='basic'),
    path('userProfile/', userProfile, name='userProfile'),
    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('blogs/', blogs, name='blogs'),
    path('article/<slug>/',articles, name="article"),
    path('mod/<slug:Title>',mod, name='mod'),
    path('recent_articles/', solution_articles, name='post'),
    path('solutions/<slug:Title>/',article_solution, name="article-solution"),
    path('articl/<slug>/', articlepage, name='postpage'),
    path('popular_articles/',popular_artiles, name='popular_articles'),
    path('catagories/<slug:mTitle>/<slug:cTitle>/', catagories, name='catagories'),
    path( 'change_password/', auth_views.PasswordChangeView.as_view() ,name='password_change'),
    path( 'change_password/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="firmApp/auth/password_reset.html"),  name="reset_password"),
    path('reset_password_sent/',  auth_views.PasswordResetDoneView.as_view(template_name="firmApp/auth/password_reset_sent.html"),   name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="firmApp/auth/password_reset_form.html"),  name='password_reset_confirm'),
    path('reset_password_complete/',  auth_views.PasswordResetCompleteView.as_view(template_name="firmApp/auth/password_reset_done.html"),    name="password_reset_complete"),
]