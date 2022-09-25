from django.urls import path
from .views import PostList, PostDetail, create_post, PostUpdate, PostDelete
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import IndexView
from .views import upgrade_me

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', create_post, name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('signin/', IndexView.as_view()),
    path('login/',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
]