from django.contrib import admin
from django.urls import path
from fir import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('submit_fir/', views.submit_fir, name='submit_fir'),
    path('firs/', views.view_firs, name='view_firs'),  # NEW,
    path('fir/' , views.fir , name='fir'),
    path('login/', views.login, name='login'),
    path('suppport_forum/' , views.support_forum , name='support_forum'),
    path('new_post/' , views.new_post , name='new_post'),
    path('find_help/' , views.find_help , name='find_help'),






]


