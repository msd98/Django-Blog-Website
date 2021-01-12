from django.urls import path
from . import views
from .views import AddPostView
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('autosuggest',views.autosuggest,name='autosuggest'),
    path('search',views.search,name='search'),
    path('add_post/',AddPostView.as_view(),name='add_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>',views.Likeview,name='like_post'),
    path('<slug:slug>/rate',views.rate,name='rate'),

]