from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('contact/', views.ContactPageView, name='contact_page'),
    path('404/', views.error_page_view, name='error_page'),
    path('news/c/', views.CreateNewsOne.as_view(), name='fsda'),
    path('news/list/', views.NewsList.as_view(), name='news_list'),
    path('category/<slug:slug>/', views.CategoryPageView.as_view(), name='category_page'),
    path('news/<slug:slug>/', views.SinglePageView.as_view(), name='single_page'),
    path('news/<slug:slug>/news', views.EditNews.as_view(), name='edit_news'),
]