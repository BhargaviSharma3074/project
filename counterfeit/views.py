from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Product
from .forms import ProductForm, UserRegistrationForm

def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser

def home(request):
    """Home page - redirects to dashboard if logged in"""
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin_dashboard')
        else:
            return redirect('user_dashboard')
    return redirect('login')

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'counterfeit/register.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_admin(user):
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'counterfeit/login.html')

@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_dashboard')
    
    products = Product.objects.all()
    total_products = products.count()
    context = {
        'products': products[:10],  # Show latest 10
        'total_products': total_products,
    }
    return render(request, 'counterfeit/admin_dashboard.html', context)

@login_required
def user_dashboard(request):
    """User dashboard view"""
    products = Product.objects.all()[:10]  # Show latest 10
    context = {
        'products': products,
    }
    return render(request, 'counterfeit/user_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def add_product(request):
    """Add new product (Admin only)"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('view_products')
    else:
        form = ProductForm()
    return render(request, 'counterfeit/add_product.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def view_products(request):
    """View all products (Admin only)"""
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(product_id__icontains=query) | 
            Q(description__icontains=query)
        )
    return render(request, 'counterfeit/view_products.html', {'products': products, 'query': query})

@login_required
@user_passes_test(is_admin)
def update_product(request, pk):
    """Update product (Admin only)"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('view_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'counterfeit/update_product.html', {'form': form, 'product': product})

@login_required
def verify_product(request):
    """Verify product authenticity (All users)"""
    result = None
    product = None
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '').strip()
        if product_id:
            try:
                product = Product.objects.get(product_id=product_id)
                result = 'authentic'
            except Product.DoesNotExist:
                result = 'counterfeit'
        else:
            messages.error(request, 'Please enter a product ID.')
    
    return render(request, 'counterfeit/verify_product.html', {
        'result': result,
        'product': product,
    })
