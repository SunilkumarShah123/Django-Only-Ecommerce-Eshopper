from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from cart.cart import Cart
from .models import *
from django.core.paginator import Paginator
from .models import User
from django.db.models import Min,Max
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def home(request):
    carousel = carsousel.objects.all()
    context={
        'carousel':carousel
    }
    return render(request,'index.html',context)


def store(request, category_slug=None, sub_slug=None):
    search=request.GET.get('search')

    if search:
        products = Product.objects.filter(
        Q(product_name__icontains=search) |
        Q(description__icontains=search) |
        Q(category__slug__icontains=search) |
        Q(sub_category__sub_slug__icontains=search) |
        Q(brand__brand_slug__icontains=search)
    ).distinct()


    else:
         products = Product.objects.all()
    
    if category_slug:
        products = products.filter(category__slug=category_slug)

    if sub_slug:
        products = products.filter(sub_category__sub_slug=sub_slug)

    # brand filter
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__brand_slug=brand_slug)

    # price filter
    min_price = Product.objects.aggregate(Min('price'))
    max_price = Product.objects.aggregate(Max('price'))
    filtered_price = request.GET.get('FilterPrice')

    if filtered_price:
        products = products.filter(price__lte=int(filtered_price))

    paginator = Paginator(products, 2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'cate': Category.objects.all(),
        'brands': Brand.objects.all(),
        'selected_page': page_obj,
        'min_price': min_price,
        'max_price': max_price,
        'filtered_price': filtered_price,
        'searched_keyword':search
    }

    return render(request, 'store.html', context)
    
@login_required(login_url='user_login')
def product_detail(request, category_slug, sub_slug, brand_slug, product_slug):
    single_product = get_object_or_404(
        Product,
        slug=product_slug,
        category__slug=category_slug,
        sub_category__sub_slug=sub_slug,
        brand__brand_slug=brand_slug
    )
    cart = request.session.get('cart', {})
    
    #creating comment
    if request.method == 'POST':
        comment=Comment()
        comment.user=request.user
        comment.product=single_product
        comment.comment=request.POST.get('comment')
        comment.save()
        messages.success(request,f"{comment.user.username},your comment has been added successfully")
        return HttpResponseRedirect(request.path_info)
    
    #returning comment count
    comments=Comment.objects.filter(product=single_product)
    comment_count=comments.count()


    context = {
        'single_product': single_product,
        'cart_product_ids': cart.keys(),
        'comments':comments,
        'comment_count':comment_count
    }
    return render(request, 'product_detail.html', context)

@login_required(login_url='user_login')
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required(login_url='user_login')
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url='user_login')
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")
@login_required(login_url='user_login')
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")
@login_required(login_url='user_login')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")
@login_required(login_url='user_login')
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_total_amount = 0

    for item in cart.values():
        price = int(item['price'])        
        quantity = int(item['quantity'])  

        item['total_price'] = price * quantity
        cart_total_amount += item['total_price']

    tax = cart_total_amount * 0.13
    grand_total = cart_total_amount + tax

    context = {
        'cart_total_amount': cart_total_amount,
        'tax': round(tax, 2),
        'grand_total': round(grand_total, 2),
    }

    return render(request, 'cart.html', context)


@login_required(login_url='user_login')
def contact(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        phone_number=request.POST.get('phone')
        description=request.POST.get('message')
        if Contact.objects.filter(email=email).exists():
            messages.error(request,f"{email} already exits")
            return redirect('contact')
        elif Contact.objects.filter(phone_number=phone_number).exists():
            messages.error(request,f"{phone_number} alreay exits")
            return redirect('contact')
        else:
            Contact.objects.create(name=name,email=email,subject=subject,phone_number=phone_number,description=description)
            messages.success(request,f"Hy {name} ! successfully contacted")
            return redirect('contact')

    return render(request,'contact.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        print(remember_me)
        next_url=request.POST.get("next")
        user = authenticate(request,username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            if remember_me:
                request.session.set_expiry(1209600)  
            else:
                request.session.set_expiry(0)
            return redirect(next_url if next_url else "home")  
        else:
            messages.error(request, "Invalid username or password")
            return redirect("user_login")

    return render(request, "auth/user_login.html")

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("user_register")

        # Username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("user_register")

        # Email check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("user_register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("user_login")

    return render(request, "auth/user_register.html")


@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('home')

@login_required(login_url='user_login')
def profile(request):
    order=Order.objects.filter(user=request.user).order_by('-date')
    context={
        'order':order   
    }
    return render(request,'auth/profile.html',context)

@login_required(login_url='user_login')
def old_pass_change(request):
    if request.method == 'POST':
        fm=PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)#default nature of this form is after succesfull pass change it automatically logout and clear out session  but using this function will update the user change info in the session and donot logout automatically
            messages.success(request,f"{fm.user.username},your password changed successfully")
            return redirect('profile')
    else:
         fm=PasswordChangeForm(user=request.user)
        
    return render(request,'auth/pass/old_passchange.html',{'form':fm})
@login_required(login_url='user_login')
def checkout(request):
    #cart code for order summery
    cart = request.session.get('cart', {})
    cart_total_amount = 0

    for item in cart.values():
        price = int(item['price'])        
        quantity = int(item['quantity'])  

        item['total_price'] = price * quantity
        cart_total_amount += item['total_price']

    tax = cart_total_amount * 0.13
    grand_total = cart_total_amount + tax


    context = {
        'cart_total_amount': cart_total_amount,
        'tax': round(tax, 2),
        'grand_total': round(grand_total, 2),
    }

    return render(request,'checkout.html',context)

@login_required(login_url='user_login')
def do_order(request):
        if request.method == 'POST':
            full_name=request.POST.get('full_name')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            city=request.POST.get('city')
            full_address=request.POST.get('full_address')
            order_notes=request.POST.get('order_notes')
            cart=request.session.get('cart',{})
            user_id=request.session.get('_auth_user_id')
            user=User.objects.get(id=user_id)
            
            for i in cart:
                product=cart[i]['name']
                quantity=cart[i]['quantity']
                price=cart[i]['price']
                total=float(price)*int(quantity)
                image=cart[i]['image']
                Order.objects.create(user=user,full_name=full_name,email=email,phone=phone,city=city,full_address=full_address,order_notes=order_notes,product=product,quantity=quantity,price=price,total=total,image=image)
            messages.success(request,f"Dear {full_name},your order has been placed successfully")
            request.session['cart']={} 
            user_id=request.session.get('_auth_user_id')
            user=User.objects.get(id=user_id)
            return redirect('checkout')
        



          