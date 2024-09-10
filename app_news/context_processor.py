from .models import News, Categories
from datetime import date

def common_views(request):
    latest_news = News.published.order_by('-published_time')[:10]
    popular_news = News.published.order_by('?')[:5]
    category_list = Categories.objects.all()

    context = {
        "latest_news": latest_news,
        "popular_news": popular_news,
        "category_list": category_list
    }
    return context