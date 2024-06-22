import os
import django
import random
from faker import Faker
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure settings for the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art_by_mtr.settings')
django.setup()

# Import models
from store.models import Category, Medium, Artwork, Order, Cart, CheckOut  
fake = Faker()

def create_categories(n=5):
    categories = []
    for _ in range(n):
        name = fake.word()
        category = Category.objects.create(name=name, description=fake.text())
        categories.append(category)
    return categories

def create_media(n=5):
    media = []
    for _ in range(n):
        name = fake.word()
        medium = Medium.objects.create(name=name)
        media.append(medium)
    return media

def create_artworks(categories, media, n=20):
    artworks = []
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        artwork = Artwork.objects.create(
            title=title,
            slug=slugify(title),
            description=fake.text(),
            price=random.uniform(10.0, 1000.0),
            stock=random.randint(1, 10),
            width=random.randint(10, 100),
            height=random.randint(10, 100),
            category=random.choice(categories),
            medium=random.choice(media)
        )
        artworks.append(artwork)
    return artworks

def create_users(n=5):
    User = get_user_model()
    users = []
    for _ in range(n):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123'
        )
        users.append(user)
    return users

def create_orders(users, artworks, n=30):
    orders = []
    for _ in range(n):
        order = Order.objects.create(
            customer=random.choice(users),
            artwork=random.choice(artworks),
            quantity=random.randint(1, 5),
            ordered=fake.boolean(chance_of_getting_true=50)
        )
        orders.append(order)
    return orders

def create_carts(users, orders):
    for user in users:
        cart = Cart.objects.create(customer=user)
        cart.orders.set(random.sample(orders, k=random.randint(1, 5)))
        cart.save()

def create_checkouts(users, orders):
    for user in users:
        checkout = CheckOut.objects.create(customer=user)
        checkout.orders.set(random.sample(orders, k=random.randint(1, 5)))
        checkout.save()

def populate_data():
    print("Creating categories...")
    categories = create_categories()

    print("Creating media...")
    media = create_media()

    print("Creating artworks...")
    artworks = create_artworks(categories, media)

    print("Creating users...")
    users = create_users()

    print("Creating orders...")
    orders = create_orders(users, artworks)

    print("Creating carts...")
    create_carts(users, orders)

    print("Creating checkouts...")
    create_checkouts(users, orders)

    print("Data population complete!")

if __name__ == '__main__':
    populate_data()
