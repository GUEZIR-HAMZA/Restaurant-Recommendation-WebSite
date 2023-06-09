from django.db import models
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.models import AbstractUser


class KitchenCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# def scrape_restaurant_data():
#     page = requests.get('https://www.tripadvisor.com/Restaurants-g293730-Morocco.html')
#     soup = BeautifulSoup(page.content, 'html.parser')
#
#     # get resaturants in each city and add them to the database
#     cities = soup.find_all('div', class_='geo_name')
#     for city in cities:
#         city_name = city.find('a').text
#         city_url = city.find('a')['href']
#         city_page = requests.get(city_url)
#         city_soup = BeautifulSoup(city_page.content, 'html.parser')
#         restaurants = city_soup.find_all('div', class_='geoList')
#         for restaurant in restaurants:
#             name = restaurant.find('a').text
#             address = restaurant.find('div', class_='item').text
#             phone_number = restaurant.find('div', class_='item').text
#             website = restaurant.find('div', class_='item').text
#             hours = restaurant.find('div', class_='item').text
#             menu = restaurant.find('div', class_='item').text
#             kitchen_category = restaurant.find('div', class_='item').text
#             price_range = restaurant.find('div', class_='item').text
#             accepts_reservations = restaurant.find('div', class_='item').text
#             offers_delivery = restaurant.find('div', class_='item').text
#             image_url = restaurant.find('img')['src']
#             image_name = f"{name}.jpg"
#             image_content = requests.get(image_url).content
#             image_file = BytesIO(image_content)
#             restaurant_obj = Restaurant.objects.create(
#                 name=name,
#                 address=address,
#                 phone_number=phone_number,
#                 website=website,
#                 hours=hours,
#                 menu=menu,
#                 kitchen_category=kitchen_category,
#                 price_range=price_range,
#                 accepts_reservations=accepts_reservations,
#                 offers_delivery=offers_delivery,
#             )
#             restaurant_obj.image.save(image_name, File(image_file))
#     print('Restaurants added successfully')


class restaurant_image(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurants', blank=True, null=True)

    def __str__(self):
        return self.restaurant.name


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    hours = models.CharField(max_length=100, blank=True, null=True)
    menu = models.URLField(blank=True, null=True)
    kitchen_category = models.ForeignKey(KitchenCategory, on_delete=models.PROTECT)
    priceRange = models.CharField(max_length=10)
    acceptsReservations = models.BooleanField(default=False)
    offersDelivery = models.BooleanField(default=False)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def update_rating(self, review):
        # update the rating of the restaurant
        self.rating = (self.rating + review.rating) / 2
        self.save()

    def get_reviews(self):
        return self.reviews.all()

    def accept_reservations(self):
        return self.acceptsReservations

    def offer_delivery(self):
        return self.offersDelivery


class Reviews(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('restaurant', 'user')

    def __str__(self):
        return f'{self.restaurant} - {self.user.username}'

    def get_rating(self):
        return self.rating

    def get_comment(self):
        return self.comment


class Users(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name='user groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username

    # def get_favorites(self):
    #     return self.favorites.all()
    #
    # def add_favorite(self, restaurant):
    #     self.favorites.add(restaurant)
    #
    # def remove_favorite(self, restaurant):
    #     self.favorites.remove(restaurant)


# class MenuItem(models.Model):
#     name = models.CharField(max_length=50)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     description = models.TextField(blank=True, null=True)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name
