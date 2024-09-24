import requests, django, os

from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.db import IntegrityError

from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_news.settings')
django.setup()
from app_news.models import News, Authors, Categories

def create_news(url, category_name):
    name, create = Categories.objects.get_or_create(name=category_name)
    url_main = 'https://kun.uz'
    url_category = f"/news/category/{url}"
    url_news_body = []
    img_urls_list = []

    html = requests.get(f"{url_main}{url_category}").text
    soup = BeautifulSoup(html, 'html.parser')

    while True:
        links_list = soup.find('div', class_='news-page__list')
        links = links_list.find_all('a')
        for link in links:
            url_news_body.append(link['href'])
            if len(url_news_body) >= 15:
                break

        img_div = soup.find_all('div', class_='news-page__item-img')
        for img_tag in img_div:
            soup = BeautifulSoup(str(img_tag), 'html.parser')
            img_urls_list.append(soup.find('img')['src'])
            if len(img_urls_list) >= 15:
                break
        break

    i = 1
    while i <= 15:
        news_detail = {}

        html_body = requests.get(f"{url_main}{url_news_body[i - 1]}").text
        soup_body = BeautifulSoup(html_body, 'html.parser')

        title = soup_body.find('h1', class_='news-inner__content-title').text
        title = str(title)
        slug = slugify(title)

        for_body = []
        body_lists = soup_body.find('div', class_='news-inner__content-page')
        body_list = body_lists.find_all('p')
        for body in body_list:
            for_body.append(body.text.strip())
        if soup_body.find('p', {'style': 'text-align:right'}):
            author_name, author_create = Authors.objects.get_or_create(name=str(for_body.pop(-1)))
        else:
            author_name = get_object_or_404(Authors, name='admin')
        body = str(''.join(for_body))

        image = str(img_urls_list[i - 1])
        response = requests.get(str(image))
        filename = os.path.basename(str(image))
        file_path = f'C:/Users/qwert/python_projects/project_news/media/news/images/{filename}'
        filename = f"news/images/{filename}"
        with open(file_path, 'wb') as file:
            file.write(response.content)
        category = str(name)

        i += 1
        try:
            News.objects.create(
                title=title,
                slug=slug,
                body=body,
                image=filename,
                category=name,
                status='PB',
                author=author_name
            )
            print(f"add-{title}")
        except IntegrityError:
            print(f"not_add-{title}")
            continue


# create_news(category_name="fan-texnika", url='texnologiya')


