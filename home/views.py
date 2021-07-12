from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from product.models import *
from order.models import *
from django.contrib import messages
from .forms import SearchForm
import json


# Create your views here.


def index(request):

    slider_image = SliderImage.objects.all().order_by('-id')[:4]
    offer_image = OfferImage.objects.all().order_by('-id')[:3]
    latest_products = Product.objects.all().order_by('-id')
    products = Product.objects.all().order_by('id')[:4]
    random_products = Product.objects.all().order_by('?')
    page = "home"

    context = {'page': page,
               'slider_image': slider_image, 'offer_image': offer_image, 'products': products, 'latest_products': latest_products, 'random_products': random_products}
    return render(request, 'Home/index.html', context)


def aboutUs(request):
    context = {}
    return render(request, 'Home/about.html', context)


def contactUs(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            messages.success(
                request, "Your message has been sent. Thank you for your message")

            return redirect('/contact')

    context = {'form': form}
    return render(request, 'Home/contact.html', context)


def category_products(request, id, slug):
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    latest_products = Product.objects.all().order_by('-id')[:3]

    context = {'products': products, 'catdata': catdata,
               'latest_products': latest_products}
    return render(request, 'Home/category_product.html', context)


def search(request):

    latest_products = Product.objects.all().order_by('-id')[:3]
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                # SELECT * FROM product WHERE title LIKE '%query%'
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(
                    title__icontains=query, category_id=catid)

            context = {'products': products, 'query': query,
                       'latest_products': latest_products}
            return render(request, 'Home/search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_details(request, id, slug):
    query = request.GET.get('q')
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(
        product_id=id, status='True').order_by('-id')
    related_products = Product.objects.all().order_by('?')[:4]

    context = {'product': product,
               'images': images, 'related': related_products, 'comments': comments}
    
    
    if product.variant !="None": 
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
        
    
    return render(request, 'Home/product_details.html', context)


def Faq(request):
    
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")

    context = {
        'faq': faq,
    }
    return render(request, 'Home/faq.html', context)