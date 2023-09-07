from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.
def home(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(category,slug=c_slug)
        products_list=products.objects.filter(categ=c_page,availability=True)
    else:
        products_list=products.objects.all().filter(availability=True)
        paginator=Paginator(products_list,3)
        try:
            page=int(request.GET.get('page','1'))
        except:
            page=1
        try:
            product=paginator.page(page)
        except(EmptyPage,InvalidPage):
            product=paginator.page(paginator.num_pages)
    cat=category.objects.all()
    return render(request,'index.html',{'cat':cat,'prod':product})

def prodDetails(request,c_slug,product_slug):
    try:
        prod=products.objects.get(categ__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'item.html',{'pr':prod})

def searching(request):
    prod=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        prod=products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query))
    return render(request,"search.html",{'qr':query,'pr':prod})
