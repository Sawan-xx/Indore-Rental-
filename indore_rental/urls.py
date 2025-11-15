"""
URL configuration for indore_rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from listing import views 

#  for image showing setting in url 
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path ('',views.home,name='home'),
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
    path('search/',views.Search,name="search"),
    path('filter/',views.Filter,name='filter'),
    path("Register/",views.Register_as,name='register'),
    path("Login/",views.Login_as , name="login_as" ),
    path('logout/',views.Logout_as,name='logout_as'),
    path("booking",views.Booking_as,name="booking"),
    path("booking_request/<int:pk>/",views.Booking_req,name="book_room"),
    path("booking_cancle/<int:pk>/",views.Booking_cancle , name ='book_can'),
    path("account_center/",views.Account_Center , name = "account"),
    path("Add_room/",views.add_room,name='add_room'),
    path("Update_room/<int:pk>/",views.update_Room,name='up_room'),
    path("Delete_room/<int:pk>/",views.delete_Room , name="room_Delete"),
    path("Edit_Profile/",views.edit_Profile ,name="edit_Profile"),
    path("About_us/",views.about_Us,name="About"),


]


# ADD THIS FOR MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)