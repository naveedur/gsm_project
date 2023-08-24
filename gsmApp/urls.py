from unicodedata import name
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


from.views import *
from.import views

urlpatterns = [
    # path('postComment', views.postComment, name="postComment"),
    
    path('register/', register, name='register'),
    path('login/', logIn, name='login'),
    path('logout/', logoutUser, name="logout"),
    path('social_form/',social_form, name="social_form"),
    path('socialpassword/',socialpassword, name='socialpassword'),
    path('userProfile/', userProfile, name='userProfile'),
    path('update-profile/',update_profile, name="update_profile"), 
    path('profile/', profile, name='profile'),

    path('', home, name="home"), 
    path('brand/<slug>/', models, name='models'),
    path('model/<slug>/', resources, name='resources'),
    path('download/<slug>/', download, name='download'),
    path('category/', Category, name='category'),
    path('catagories/<slug:mSlug>/<slug:cSlug>/', catagories, name='catagories'),
    path('search/', search, name='search'),

    path('return-policy/' ,returnPolicy, name="return-policy"),
    path('refund-policy/' ,refundPolicy, name="refund-policy"),
    path('cancellation-policy/' ,cancellationPolicy, name="cancellation-policy"),
    path('privacy-policy/' ,privacyPolicy, name="privacy-policy"),
    path('terms-of-services/' ,termsOfServices, name="terms-of-services"),
    path('contact-us/' ,contactUs, name="contact-us"),
    path('about-us/' ,aboutUs, name="about-us"),
    path('page/<slug>/',customPage, name="page"),
    # path('basic/', basic, name='basic'),
    
    # path('dashboard/', dashboard, name='dashboard'), 
    
    path( 'change_password/', auth_views.PasswordChangeView.as_view(template_name='firmApp/auth/password_change.html'), name='password_change'),
    path( 'change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='firmApp/auth/password_change_done.html'),name='password_change_done'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="firmApp/auth/password_reset.html"),  name="reset_password"),
    path('reset_password_sent/',  auth_views.PasswordResetDoneView.as_view(template_name="firmApp/auth/password_reset_sent.html"),   name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="firmApp/auth/password_reset_form.html"),  name='password_reset_confirm'),
    path('reset_password_complete/',  auth_views.PasswordResetCompleteView.as_view(template_name="firmApp/auth/password_reset_done.html"),    name="password_reset_complete"),
]