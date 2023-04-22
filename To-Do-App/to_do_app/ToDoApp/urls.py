from django.urls import path
from . import views
from .views import Home,TaskDetail,user_login, addTask,TaskUpdate,DeleteView,register,TaskListView
from django.contrib.auth.views import LogoutView

app_name = 'ToDoApp'

urlpatterns = [
    path('',views.landingpage,name='landingpage'),
    path('home/',Home.as_view(),name = 'home'),
    path('listview/',TaskListView.as_view(),name = 'listview'),
    # path('register/',register.as_view(),name='register'),
    path('register/',views.register,name='register'),
    path('login/',user_login.as_view(),name ='login'),
    path('logout/',LogoutView.as_view(next_page='ToDoApp:login'),name ='logout'),
    path('addTask/',addTask.as_view(),name='addTask'),
    path('task-update<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('<int:pk>/',TaskDetail.as_view(), name='taskdetail'),
]

