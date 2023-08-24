from django.urls import path
from.views import *

urlpatterns = [
    path('', subscriptions, name='subscription'),
    path('paymentProcess/<slug>/', payment_process, name='payment_process'),
    path('payment/<slug>/', payment, name="payment"),
    path('increment-file-count/<slug>/',incrementFileCount,name="increment-file-count"),
    path('file-payment/<int:id>/',single_file_Payment,name="single_file_payment"),
    path('singleFilePaymentProcess/<int:id>/', single_file_payment_process, name='single_file_payment_process'),
    path('upload-file/', upload_file, name="upload_file"),
    path('upload-brand/', upload_brand, name="upload_brand"),
    path('upload-blog-post/',upload_blog_post, name="upload_blog_post"),
    path('payment-process/',process_payment),
    path('payment-success',payment_success),
    path('payment-cancel',payment_success)
    
]