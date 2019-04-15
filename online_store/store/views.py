from django.shortcuts import render
from .models import Product, Transaction, Coupon
from .forms import Search, Add_To_Cart, Update_Cart, Apply_Coupon, Checkout
from .basics import unique_set
import itertools
from django.core.exceptions import ObjectDoesNotExist
from decimal import *
import taxjar


# Create your views here.
def index(request):
    products = []
    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data.get('search_text')
            for i in range(1, len(search_text.split(' ')) + 1):
                for combination in set(itertools.combinations(search_text.split(' '), i)):
                    for word in set(itertools.permutations(combination)):
                        products.append(Product.objects.filter(ProductName__icontains=' '.join(word)))
            productIDs = unique_set(products)
            products = []
            for productID in productIDs:
                products.append(Product.objects.get(ProductID=productID))
        else:
            products = Product.objects.all()[:10]
            return render(request, 'store/index.html', {'nbar': 'store', 'products': products})
        if len(products) == 0:
            return render(request, 'store/index.html', {'nbar': 'store', 'error': True})
        render(request, 'store/index.html', {'nbar': 'store', 'products': products, 'search_text': search_text})
    # TODO implement show more results option
    # TODO implement next page filtering
    else:
        products = Product.objects.all()[:10]
    return render(request, 'store/index.html', {'nbar': 'store', 'products': products})


def get_cart(request):
    cart = request.session.get('cart', {})
    coupon = request.session.get('coupon', None)
    data = []
    for key, quantity in cart.items():
        product = Product.objects.get(pk=key.split('_')[0])
        product_size = key.split('_')[1]
        if quantity > 0:
            data.append([product, product_size, product.ProductPrice, quantity, product.ProductPrice * quantity])
    data.sort(key=lambda p: (p[0].ProductID, p[1]))
    if len(data) == 0:
        return render(request, 'store/cart.html', {'nbar': 'cart'})
    if request.method == 'POST' or coupon is not None:
        if coupon is not None:
            try:
                coupon = Coupon.objects.get(CouponCode=coupon)
            except ObjectDoesNotExist:
                coupon = None
        form = Apply_Coupon(request.POST)
        if form.is_valid() or coupon is not None:
            try:
                if form.is_valid():
                    coupon = Coupon.objects.get(CouponCode=form.cleaned_data.get('CouponCode'))
                if coupon.is_valid():
                    request.session['coupon'] = coupon.CouponCode
                    applicable_items = coupon.ApplicableItems.replace(' ', '').split(',')
                    for item_id in applicable_items:
                        for p in data:
                            if int(p[0].ProductID) == int(item_id):
                                if coupon.CouponType == 'P':
                                    p[2] = round(p[2] * Decimal(1 - (coupon.CouponValue / 100)), 2)
                                    p[4] = p[3] * p[2]
                                else:
                                    p[2] -= coupon.CouponValue
                                    if p[2] < 0:
                                        p[2] = 0
                                    p[4] = p[3] * p[2]
                    coupon = coupon.CouponName
            except ObjectDoesNotExist:
                pass
    if request.method == 'POST':
        form = Update_Cart(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data.get('ProductID')
            product_size = form.cleaned_data.get('ProductSize')
            quantity = form.cleaned_data.get('Quantity')
            for key in cart:
                if key == str(product_id) + "_" + str(product_size):
                    cart[key] = quantity
            request.session['cart'] = cart
            request.method = 'GET'
            return get_cart(request)
    total = sum([p[4] for p in data])
    return render(request, 'store/cart.html', {'nbar': 'cart', 'cart': data, 'total': total, 'coupon': coupon})


def product(request, pk):
    if request.method == 'POST':
        form = Add_To_Cart(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data.get('ProductID')
            product_size = form.cleaned_data.get('ProductSize')
            quantity = form.cleaned_data.get('Quantity')
            cart = request.session.get('cart', {})
            if cart.get(str(product_id) + '_' + str(product_size)) is not None:
                cart[str(product_id) + '_' + str(product_size)] += quantity
            else:
                cart[str(product_id) + '_' + str(product_size)] = quantity
            request.session['cart'] = cart
            added = True
    else:
        added = False
    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return index(request)
    return render(request, 'store/product.html', {'product': product, 'added': added})


def checkout(request):
    cart = request.session.get('cart', {})
    coupon = request.session.get('coupon', None)
    data = []
    for key, quantity in cart.items():
        product = Product.objects.get(pk=key.split('_')[0])
        product_size = key.split('_')[1]
        if quantity > 0:
            data.append([product, product_size, product.ProductPrice, quantity, product.ProductPrice * quantity])
    data.sort(key=lambda p: (p[0].ProductID, p[1]))
    total_before_tax = sum([p[4] for p in data])
    print(coupon)
    if coupon is not None:
        try:
            coupon = Coupon.objects.get(CouponCode=coupon)
            if coupon.is_valid():
                request.session['coupon'] = coupon.CouponCode
                applicable_items = coupon.ApplicableItems.replace(' ', '').split(',')
                for item_id in applicable_items:
                    for p in data:
                        if int(p[0].ProductID) == int(item_id):
                            if coupon.CouponType == 'P':
                                p[2] = round(p[2] * Decimal(1 - (coupon.CouponValue / 100)), 2)
                                p[4] = p[3] * p[2]
                            else:
                                p[2] -= coupon.CouponValue
                                if p[2] < 0:
                                    p[2] = 0
                                p[4] = p[3] * p[2]
                coupon = coupon.CouponName
        except ObjectDoesNotExist:
            coupon = None
    if request.method == 'POST':
        form = Checkout(request.POST)
        if form.is_valid():
            FirstName = form.cleaned_data.get('FirstName')
            LastName = form.cleaned_data.get('LastName')
            Address = form.cleaned_data.get('Address')
            City = form.cleaned_data.get('City')
            State = form.cleaned_data.get('State')
            ZIP = form.cleaned_data.get('ZIP')

            client = taxjar.Client(api_key='75c83ef0d87597791151ab2057ff6b41')
            rates = client.rates_for_location(str(ZIP), {'city': City, 'country': 'US'})
            rate = rates['combined_rate']
            tax = round(Decimal(total_before_tax) * Decimal(rate), 2)
            total = total_before_tax + tax
            return render(request, 'store/checkout.html', {'cart': data, 'total_before_tax': total_before_tax, 'tax': tax, 'total': total, 'coupon': coupon})
    return render(request, 'store/checkout.html', {'cart': data, 'total_before_tax': total_before_tax, 'coupon': coupon})
