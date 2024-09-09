from datetime import time
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from .forms import ContactForm
from .models import News, Categories


class HomePageView(TemplateView):
    model = News
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_news"] = self.model.published.order_by('?')[:10]
        context['uzbekiston_main'] = self.model.published.filter(category__name="o'zbekiston").order_by('-published_time').first()
        context['uzbekiston_side'] = self.model.published.filter(category__name="o'zbekiston").order_by('-published_time')[1:5]

        context['jahon_main'] = self.model.published.filter(category__name="jahon").order_by('?').first()
        context['jahon_side'] = self.model.published.filter(category__name="jahon").order_by('?')[1:5]

        context['iqtisodiyot_main'] = self.model.published.filter(category__name="iqtisodiyot").order_by('?').first()
        context['iqtisodiyot_side'] = self.model.published.filter(category__name="iqtisodiyot").order_by('?')[1:5]

        context['sport_main'] = self.model.published.filter(category__name="sport").order_by('?').first()
        context['sport_side'] = self.model.published.filter(category__name="sport").order_by('?')[1:5]

        context['texnologiya'] = self.model.published.filter(category__name="fan-texnika").order_by('?')[1:5]

        context['photography'] = self.model.published.order_by('?')[:6]
        return context


class SinglePageView(DetailView):
    model = News
    template_name = 'pages/single_page.html'
    context_object_name = 'news_item'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["single__related"] = self.model.published.order_by('?')[:3]
        return context


def error_page_view(request):
    return render(request, 'pages/404.html')


def ContactPageView(reqeust):
    form = ContactForm(reqeust.POST or None)

    if reqeust.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2> Message sent")

    context = {
        "form": form,
    }
    return render(reqeust, 'pages/contact.html', context)


class CategoryPageView(TemplateView):
    template_name = 'pages/category_page.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        category = get_object_or_404(Categories, slug=slug)
        news_items = News.published.filter(category=category).order_by("-published_time")
        news_main = news_items.first()
        total_items = len(news_items)
        if total_items > 4:
            split_index = (total_items - 4) // 2
            news_first__half = news_items[1:split_index + 1]
            news_second__half = news_items[split_index + 1:]
        else:
            news_first__half = []
            news_second__half = news_items[1:]

        context = {
            "category": category,
            "news_main": news_main,
            "news_first__half": news_first__half,
            "news_second__half": news_second__half
        }
        return context


class NewsList(ListView):
    model = News
    template_name = 'pages/all_news__page.html'
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        news_item = self.model.objects.all().order_by("-published_time")
        news_list__main = news_item.first()
        news_list__all = news_item[1:]
        total_news = len(news_item)

        if total_news > 4:
            split_index = (total_news - 4) // 2
            news_list__first_half = news_item[1:split_index + 1]
            news_list__second_half = news_item[split_index + 1:]
        else:
            news_list__first_half = []
            news_list__second_half = news_item[1:]


        context = {
            "news_list": news_item,
            "news_list__main": news_list__main,
            "news_list__first_half": news_list__first_half,
            "news_list__second_half": news_list__second_half,
            'news_list__all': news_list__all
        }
        return context





