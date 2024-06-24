from datetime import timezone
import django.utils
import os
import django
import random
import requests
from faker import Faker
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure settings for the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art_by_mtr.settings')
django.setup()

# Import models
from store.models import Category, Medium, Artwork, Order, Cart, CheckOut
from blog.models import Post

fake = Faker('fr-FR')

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content)
    return None

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
    image_url_template = 'https://picsum.photos/200/300?art={}'

    for _ in range(n):
        title = fake.sentence(nb_words=4)
        image_url = image_url_template.format(random.randint(1, 1000))
        image_content = download_image(image_url)

        if image_content:
            artwork = Artwork.objects.create(
                title=title,
                slug=slugify(title),
                description=fake.text(),
                price=round(random.uniform(10.0, 1000.0), 2),
                stock=random.randint(1, 10),
                width=random.randint(10, 100),
                height=random.randint(10, 100),
                category=random.choice(categories),
                medium=random.choice(media),
                thumbnail=image_content  # Assigner le contenu de l'image à la miniature
            )
            artwork.thumbnail.save(f'{slugify(title)}.jpg', image_content)
            artworks.append(artwork)
    return artworks

def create_users(n=10):
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

def create_posts(artworks, n=15):
    posts = []
    image_url_template = 'https://picsum.photos/200/300?random={}'

    for _ in range(n):
        title = fake.sentence(nb_words=4)
        image_url = image_url_template.format(random.randint(1, 1000))
        image_content = download_image(image_url)

        post = Post.objects.create(
            title=title,
            slug=slugify(title),
            description=fake.text(),
            content=fake.text(max_nb_chars=250),
            event_date=fake.date_time_this_year(before_now=True, after_now=False, tzinfo=timezone.utc),
            event_place=fake.address(),
        )

        if image_content:
            post.thumbnail.save(f'{slugify(title)}.jpg', image_content)

        # Associer des œuvres au post
        if artworks:
            num_artworks = random.randint(0, 5)
            post.event_artworks.set(random.sample(artworks, k=num_artworks))

        posts.append(post)

    return posts

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

    print("Creating posts...")
    create_posts(artworks)

    print("Creating orders...")
    orders = create_orders(users, artworks)

    print("Creating carts...")
    create_carts(users, orders)

    print("Creating checkouts...")
    create_checkouts(users, orders)

    print("Data population complete!")

if __name__ == '__main__':
    populate_data()
