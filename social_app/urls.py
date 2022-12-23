from django.urls import path
from .import views
from django.conf.urls.static import static


urlpatterns=[
    
    path('register',views.Register,name='register'),   
    path('settings',views.settings,name="settings"),
    path("login",views.Login,name='login'),
    path('',views.index,name='index'),
    path("upload",views.upload,name="upload"),
    path("search",views.search,name="search"),
    path("liked-post",views.liked,name="liked-post"),
    path("follow",views.Follow,name="follow"),
    path('profile/<str:pk>',views.profileView,name="profile"),
    path('logout',views.Logout,name='logout'),
]
