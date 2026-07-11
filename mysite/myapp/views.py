import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserUpdateForm, ProfileUpdateForm, ReviewForm
from django.db.models import Sum, Count, Avg


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'myapp/index.html', {'products': products})

def deals(request):
    products = Product.objects.all()
    pattern = re.compile(re.escape("mechanical switch"), re.IGNORECASE)
    for product in products:
        product.name = pattern.sub('<span class="highlight">\g<0></span>', product.name)
        product.description = pattern.sub('<span class="highlight">\g<0></span>', product.description)
    return render(request, 'myapp/deals.html', {'products': products})

def customer_service(request):
    return render(request, 'myapp/customer_service.html')

def contact(request):
    return render(request, 'myapp/contact.html')

def about(request):
    return render(request, 'myapp/about.html')

def set_location(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        state = request.POST.get('state')
        request.session['location'] = {'country': country, 'state': state}
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    return render(request, 'myapp/set_location.html')

# Authentication Views
def signup(request):
    if request.method == 'POST':
        u_form = UserCreationForm(request.POST)
        p_form = ProfileUpdateForm(request.POST)
        # Adding email manually since UserCreationForm doesn't include it by default
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            # Profile is created by signal, so we update it
            profile = user.userprofile
            p_form = ProfileUpdateForm(request.POST, instance=profile)
            if p_form.is_valid():
                p_form.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        u_form = UserCreationForm()
        p_form = ProfileUpdateForm()
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'myapp/auth/signup.html', context)

class MyLoginView(LoginView):
    template_name = 'myapp/auth/login.html'
    next_page = 'index'

@method_decorator(csrf_exempt, name='dispatch')
class MyLogoutView(LogoutView):
    next_page = 'index'

# Cart Views
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
            if not cart:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

def view_cart(request):
    cart = get_cart(request)
    return render(request, 'myapp/cart.html', {'cart': cart})

def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

# Order Views
@login_required
def checkout(request):
    cart = get_cart(request)
    if cart.items.count() == 0:
        return redirect('index')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()
        return redirect('order_history')
    
    return render(request, 'myapp/checkout.html', {'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'myapp/orders.html', {'orders': orders})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'myapp/profile.html', context)

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('index')
    
    orders = Order.objects.all().order_by('-created_at')
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    shipped_orders = Order.objects.filter(status='Shipped').count()
    returned_orders = Order.objects.filter(status='Returned').count()
    
    # Items purchased logic
    items_purchased = OrderItem.objects.values('product__name').annotate(total_qty=Sum('quantity')).order_by('-total_qty')
    
    # Items left to sell
    products_stock = Product.objects.all().order_by('stock')

    context = {
        'orders': orders,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'shipped_orders': shipped_orders,
        'returned_orders': returned_orders,
        'items_purchased': items_purchased,
        'products_stock': products_stock,
    }
    return render(request, 'myapp/dashboard.html', context)

@login_required
def track_package(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'myapp/track_package.html', {'order': order})

@login_required
def return_replace(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        item = get_object_or_404(OrderItem, id=item_id, order=order)
        
        if action == 'return':
            # Return back into inventory
            product = item.product
            product.stock += item.quantity
            product.save()
            
            # Item should disappear from the return or replace page
            item.delete()
            
            # If no more items in order, mark as returned
            if not order.items.exists():
                order.status = 'Returned'
                order.save()
            
            return redirect('order_history')
        elif action == 'replace':
            # For replacement, we could keep the item but mark it, 
            # or for simplicity if it "disappears", we handle it similarly 
            # but maybe don't change stock? 
            # User specifically mentioned "returned back into inventory" for return choice.
            order.status = 'Pending'
            order.save()
            return redirect('order_history')
            
    return render(request, 'myapp/return_replace.html', {'order': order})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form
    }
    return render(request, 'myapp/product_detail.html', context)
