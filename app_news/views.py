from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.db.models import Q
from hitcount.views import HitCountDetailView

from project_news.custom_permission import OnlyLoggedSuperUser
from .forms import ContactForm, EditNewsForm, CommentForm
from .models import News, Categories, Comment


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


class SinglePageView(HitCountDetailView):
    model = News
    template_name = 'main_pages/single_page.html'
    context_object_name = 'news_item'
    slug_field = 'slug'
    count_hit = True
    context = {}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_item = self.get_object()
        comments = Comment.objects.filter(news=news_item, active=True)
        comments_count = comments.count()
        comment_form = CommentForm()
        new_comment = None

        context = {
            'single_related': self.model.published.order_by('?')[:3],
            'news_item': news_item,
            'comments': comments,
            'new_comment': new_comment,
            'comments_count': comments_count,
            'comment_form': comment_form
        }
        return context

    def post(self, request, *args, **kwargs):
        news_item = self.get_object()
        single_related = News.published.order_by('?')[:3]
        comments = news_item.comments.filter(active=True)
        comment_count = comments.count()
        new_comment = None
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news_item
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()

        context = {
            'news_item': news_item,
            'single_related': single_related,
            'comments': comments,
            'comment_count': comment_count,
            'new_comment': new_comment,
            'comment_form': comment_form
        }
        return redirect('single_page', slug=news_item.slug,)

def single_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug, status=News.Status.Published)
    related_news = News.published.order_by('?')[:3]
    comments = news_item.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news_item
            new_comment.user = request.user
            new_comment.save()
            return redirect('single_page', slug=news_item.slug)
    else:
        comment_form = CommentForm()
    context = {
        'news_item': news_item,
        'single_related': related_news,
        'comment_count': comments_count,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'comments': comments
    }
    return render(request, 'main_pages/single_page.html', context)


def error_page_view(request):
    return render(request, 'main_pages/404.html')


def ContactPageView(reqeust):
    form = ContactForm(reqeust.POST or None)

    if reqeust.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2> Xabar yuborildi")

    context = {
        "form": form,
    }
    return render(reqeust, 'main_pages/contact.html', context)


class CategoryPageView(TemplateView):
    template_name = 'main_pages/category_page.html'

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

        context.update({
            "category": category,
            "news_main": news_main,
            "news_first__half": news_first__half,
            "news_second__half": news_second__half
        })
        return context


class NewsList(ListView):
    model = News
    template_name = 'main_pages/all_news__page.html'
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


        context.update({
            "news_list": news_item,
            "news_list__main": news_list__main,
            "news_list__first_half": news_list__first_half,
            "news_list__second_half": news_list__second_half,
            'news_list__all': news_list__all
        })
        return context


class EditNews(OnlyLoggedSuperUser, UpdateView):
    model = News
    form_class = EditNewsForm
    template_name = 'editing_pages/edit_delete_news.html'
    context_object_name = 'news_item'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'delete' in request.POST:
            self.object.delete()
            return redirect('home_page')
        return super().post(request, *args, **kwargs,)

    def get_success_url(self):
        return reverse('single_page', kwargs={'slug': self.object.slug})

class CreateNewsOne(OnlyLoggedSuperUser, CreateView):
    model = News
    form_class = EditNewsForm
    template_name = 'editing_pages/create_news.html'

    def get_success_url(self):
        return reverse('single_page', kwargs={'slug': self.object.slug})


# def create_news(request):
#     if request.method == 'POST':
#         # Ensure request.POST and request.FILES are passed correctly
#         form = EditNewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home_page')  # Replace with your desired redirect
#     else:
#         form = EditNewsForm()
#     return render(request, 'editing_pages/create_news.html', {'form': form})


class SearchResultView(ListView):
    model = News
    template_name = 'main_pages/search_result.html'
    context_object_name = 'search_result'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
        else:
            return News.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        results = self.get_queryset()
        index = len(results) // 2

        context['first'] = results[:index]
        context['second'] = results[index:]
        context['query'] = self.request.GET.get('q')
        return context


# class NewsCountDetailView(HitCountDetailView):
#     model = News
#     count_hit = True
#
#     def get_object(self, queryset=None):
#         news_item = News.objects.get(slug=self.kwargs['slug'])
#         return news_item