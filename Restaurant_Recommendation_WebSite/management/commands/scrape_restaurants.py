from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup

from Restaurant_Recommendation_WebSite.models import Restaurant


class Command(BaseCommand):
    help = 'Scrape restaurants and add them to the database'

    def handle(self, *args, **options):
        # Scrape restaurants from a website and add them to the database
        page = requests.get('https://www.tripadvisor.com/Restaurants-g293730-Morocco.html')
        soup = BeautifulSoup(page.content, 'html.parser')

        # get resaturants in each city and add them to the database
        cities = soup.find_all('div', class_='geo_name')
        for city in cities:
            city_name = city.find('a').text
            city_url = city.find('a')['href']
            city_page = requests.get(city_url)
            city_soup = BeautifulSoup(city_page.content, 'html.parser')
            restaurants = city_soup.find_all('div', class_='geoList')
            for restaurant in restaurants:
                name = restaurants.find('a').text
                address = restaurant.find('div', class_='item').text
                phone_number = restaurant.find('div', class_='item').text
                website = restaurant.find('div', class_='item').text
                hours = restaurant.find('div', class_='item').text
                menu = restaurant.find('div', class_='item').text
                kitchen_category = restaurant.find('div', class_='item').text
                price_range = restaurant.find('div', class_='item').text
                accepts_reservations = restaurant.find('div', class_='item').text
                offers_delivery = restaurant.find('div', class_='item').text
                Restaurant.objects.create(
                    name=name,
                    address=address,
                    phone_number=phone_number,
                    website=website,
                    hours=hours,
                    menu=menu,
                    kitchen_category=kitchen_category,
                    price_range=price_range,
                    accepts_reservations=accepts_reservations,
                    offers_delivery=offers_delivery,
                )
        self.stdout.write(self.style.SUCCESS('Restaurants added successfully'))

# Path: Restaurant_Recommendation_WebSite\management\commands\scrape_reviews.py