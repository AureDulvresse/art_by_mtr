import json
import paypalrestsdk
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from art_by_mtr.settings import ELEMENTS_PER_PAGE
from store.models import Artwork, Cart, CheckOut, Order, Payment


stripe.api_key = settings.STRIPE_SECRET_KEY



def home_page(request) -> HttpResponse:
    artworks = Artwork.objects.all().order_by('-updated_at')[:3]

    context = {
        'artworks': artworks,
        'events': 4,
    }

    return render(request, 'store/pages/home.html', context)

def about_page(request) -> HttpResponse:
    context = {
        "testimonials": "testi",
    }

    return render(request, "store/pages/about.html", context)


def gallery_page(request) -> HttpResponse:
    artworks =  Artwork.objects.all().order_by("-updated_at")

    paginator = Paginator(artworks, ELEMENTS_PER_PAGE)
    page = request.GET.get('page')
    artworks = paginator.get_page(page)

    context = {
        'artworks': artworks,
    }

    return render(request, 'store/pages/gallery.html', context)


def artwork_detail_page(request, slug):

    artwork = get_object_or_404(Artwork, slug=slug)
    
    current_category = artwork.category
    
    related_artworks = Artwork.objects.exclude(id=artwork.id)
    
    related_artworks = related_artworks.filter(category=current_category)[:3]
    
    
    context = {
        'artwork': artwork,
        'related_artworks': related_artworks,
    }

    return render(request, 'store/pages/artwork-detail.html', context)

def contact_page(request) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validation simple des données du formulaire
        if not name or not email or not subject or not message:
            messages.error(request, "Tous les champs sont requis.")
            return redirect('store:contact')

        # Validation de l'adresse email
        if '@' not in email or '.' not in email:
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('store:contact')

        # Construire le message complet avec un formatage amélioré
        logo_url = request.build_absolute_uri('/static/img/logo_bg_white.png')
        html_message = render_to_string('store/components/contact_email.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'logo_url': logo_url,
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Assurez-vous de définir cette variable dans vos settings
                fail_silently=False,
                html_message=html_message
            )
            messages.success(request, "Votre message a été envoyé avec succès!")
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite: {e}")

        return redirect('store:contact')

    return render(request, "store/pages/contact.html")


@login_required
def cart_page(request):
    cart = get_object_or_404(Cart, customer = request.user)

    cart_cumul = 0

    orders = cart.orders.all().order_by('-created_at')

    for order in orders:
        cart_cumul += (order.artwork.price * order.quantity)

    context = {
        "orders": orders,
        "cart_cumul": cart_cumul,
    }

    return render(request, "store/pages/cart.html", context)

@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        artwork_id = data.get("artwork_id")
        quantity = int(data.get("quantity", 1))

        print(request.POST.get("artwork_id"), artwork_id, type(artwork_id))

        try:
            artwork = Artwork.objects.get(id=artwork_id)
        except Artwork.DoesNotExist:
            return JsonResponse({"error": "Artwork not found"}, status=404)

        cart, created = Cart.objects.get_or_create(customer=request.user)
        order, created = Order.objects.get_or_create(customer=request.user, artwork=artwork, ordered=False)

        if not created:
            order.quantity += quantity
        else:
            order.quantity = quantity

        order.save()
        cart.orders.add(order)

        return JsonResponse({"message": "Artwork ajouté au panier avec succès", "quantity": order.quantity}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def checkout_page(request):
    user = request.user
    cart = get_object_or_404(Cart, customer = user)

    if request.method == "POST":
        CheckOut.objects.create(customer = user, orders = cart.orders.all())
        cart.delete()
        return redirect("store:shop")

    cart_cumul = 0
    orders = cart.orders.all().order_by('-created_at')

    for order in orders:
        cart_cumul += (order.product.price * order.quantity)

    context = {
        "orders": orders,
        "order_cumul": cart_cumul,
    }


    return render(request, "store/pages/checkout.html", context)
    

@method_decorator(login_required, name='dispatch')
class StripePaymentView(TemplateView):
    template_name = 'payments/stripe_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context

@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'  # Remplacez par votre domaine
        checkout = CheckOut.objects.create(customer=request.user)
        orders = request.user.orders.filter(ordered=False)
        for order in orders:
            checkout.orders.add(order)

        line_items = []
        for order in orders:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'artwork_data': {
                        'name': order.artwork.title,
                    },
                    'unit_amount': int(order.artwork.price * 100),  # Convert to cents
                },
                'quantity': order.quantity,
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=domain_url + 'payments/success/',
                cancel_url=domain_url + 'payments/cancel/',
            )
            
            # Enregistrer les détails du paiement dans la base de données
            Payment.objects.create(
                user=request.user,
                stripe_checkout_id=checkout_session.id,
                amount=sum(order.artwork.price * order.quantity for order in orders),
                currency='usd',
                status='created',
                checkout=checkout
            )

            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Mettre à jour l'état du paiement
        payment = Payment.objects.get(stripe_checkout_id=session['id'])
        payment.status = 'completed'
        payment.save()

    return HttpResponse(status=200)

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

@login_required
def create_paypal_payment(request):
    if request.method == 'POST':
        orders = request.user.orders.filter(ordered=False)
        total_amount = sum(order.artwork.price * order.quantity for order in orders)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
             "redirect_urls": {
                "return_url": "http://localhost:8000/payments/success/",
                "cancel_url": "http://localhost:8000/payments/cancel/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": order.artwork.title,
                        "sku": order.artwork.slug,
                        "price": str(order.artwork.price),
                        "currency": "USD",
                        "quantity": order.quantity
                    } for order in orders]
                },
                "amount": {
                    "total": str(total_amount),
                    "currency": "USD"
                },
                "description": "This is the payment transaction description."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            return JsonResponse({'error': payment.error}, status=400)

@login_required
def execute_paypal_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Enregistrer les détails du paiement dans la base de données
        orders = request.user.orders.filter(ordered=False)
        checkout = CheckOut.objects.create(customer=request.user)
        for order in orders:
            checkout.orders.add(order)

        Payment.objects.create(
            user=request.user,
            stripe_checkout_id=payment.id,
            amount=payment.transactions[0].amount.total,
            currency=payment.transactions[0].amount.currency,
            status='completed',
            checkout=checkout
        )

        for order in orders:
            order.ordered = True
            order.ordered_at = timezone.now()
            order.save()

        return redirect('payments/success/')
    else:
        return JsonResponse({'error': payment.error}, status=400)
    


@login_required
def payment_success(request):
    return render(request, 'store/payments/success.html')

@login_required
def payment_cancel(request):
    return render(request, 'store/payments/cancel.html')

