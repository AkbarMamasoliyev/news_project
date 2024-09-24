from django.urls import path
from app_news import views
from accounts.views import admin_list_display
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('admin-list/', admin_list_display, name='admin_list'),
    path('contact/', views.ContactPageView, name='contact_page'),
    path('404/', views.error_page_view, name='error_page'),
    path('news/create/', views.CreateNewsOne.as_view(), name='news_create_page'),
    path('news/search/', views.SearchResultView.as_view(), name='search_result_page'),
    path('news/list/', views.NewsList.as_view(), name='news_list'),
    path('category/<slug:slug>/', views.CategoryPageView.as_view(), name='category_page'),
    path('news/<slug:slug>/', views.SinglePageView.as_view(), name='single_page'),
    path('news/<slug:slug>/edit/', views.EditNews.as_view(), name='edit_news'),
]