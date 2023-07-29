import csv
import urllib
from urllib import parse

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from app.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    current_page = int(request.GET.get('page', 1))
    with open(BUS_STATION_CSV, encoding='cp1251', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        content = [row for row in reader]

        paginator = Paginator(content, 10)
        info = paginator.get_page(current_page)
        print(len(content) % 10)
    if (len(content) % 10 > 0 and current_page < (len(content) // 10) + 1) or\
            (len(content) % 10 == 0 and current_page < (len(content) // 10)):
        next_page_url = f'{reverse("bus_stations")}?{urllib.parse.urlencode({"page": str(current_page + 1)})}'
    else:
        next_page_url = None
    if current_page > 1:
        prev_page_url = f'{reverse("bus_stations")}?{urllib.parse.urlencode({"page": str(current_page - 1)})}'
    else:
        prev_page_url = None
    return render(request, 'index.html', context={
        'bus_stations': info,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
