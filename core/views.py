from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Category, Customer, Product, User, Order, OrderItem, CheckoutAddress
from core.forms import ProductForm, CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def index(request):
    products = Product.objects.all()

    return render(request, 'core/index.html', {'products' : products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('add_product')
        else:
            messages.error(request, "Product not added. Please check the form for errors.")
    else:
        form = ProductForm()

    return render(request, 'core/add_product.html', {'form': form})


def product_desc(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'core/product_desc.html', {'product': product})

def add_to_cart(request, pk):
    # get the particular item using pk
    product = Product.objects.get(pk=pk)

    # create order item
    order_item_created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    # get query set of Order Object of particular user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item = order.items.get(product__pk=pk)
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added Quantity item")
            return redirect('product_desc', pk=pk)
        else:
            order.items.add(order_item_created[0])
            messages.info(request, "Item added to Cart")
            return redirect('product_desc', pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item_created[0])
        messages.info(request, "Item added to cart")
        return redirect('product_desc', pk=pk)


def order_list(request):
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user = request.user, ordered=False)
        return render(request, 'core/order_list.html', {'order' : order})
    return render(request, 'core/order_list.html',{'message': "OPPSS!!! Your cart is empty. "})


def add_item(request, pk):
    # Get the particular product using pk
    product = Product.objects.get(pk=pk)

    # Create or get the order item associated with the product and user
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    # Get the query set of Order objects for the particular user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item already exists in the order
        if order.items.filter(product__pk=pk).exists():
            # Increment the quantity if it's less than the available count
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Added Quantity item")
            else:
                messages.warning(request, "Maximum quantity reached for this item.")
        else:
            # Add the order item to the order
            order.items.add(order_item)
            messages.info(request, "Item added to Cart")
    else:
        # Create a new order if one doesn't exist
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to cart")

    return redirect('product_desc', pk=pk)

def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False,
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk =pk).exists():
            order_item = OrderItem.objects.filter(
                product = item,
                user = request.user,
                ordered = False
            )[0]

            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity updated.")
            return redirect('order_list')
        
        else:
            messages.info(request, "Item not in cart.")
            return redirect('order_list')
    
    else:
        messages.info(request, "Sorry, You don't have any order")
        return redirect('order_list')
    
def checkout_page(request):
    if CheckoutAddress.objects.filter(user = request.user).exists():
        return render(request, 'core/checkout_address.html', {'payment_allow' : 'allow'})
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code  = form.cleaned_data.get('zip_code')

                checkout_address = CheckoutAddress(
                    user = request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip_code = zip_code
                )

                checkout_address.save()
                print("It should print checkout summary")
                return render(request, 'core/checkout_address.html', {'payment_allow' : 'allow'})
            
        except Exception as e:
            messages.warning(request, f"Checkout Failed: {e}")
            return redirect('checkout')
    else:
        form = CheckoutForm()
        return render(request, 'core/checkout_address.html', {'form' : form})