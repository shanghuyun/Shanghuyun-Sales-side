import traceback
from django import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import(
    Profile,
    WebBasicInf,
    CarouselImage,
    AboutUs,
    SellerInfo,
    ProductInfo,
    ProductImage,
    MapIframe
)
from .forms import ContactForm


def index(request):
    context = {}
    try:
        context['profiles'] = Profile.objects.get()
    except Profile.DoesNotExist:
        pass
    try:
        context['mapIframe'] = MapIframe.objects.get()
    except MapIframe.DoesNotExist:
        pass
    try:
        context['about'] = AboutUs.objects.get()
    except AboutUs.DoesNotExist:
        pass
    try:
        context['web_inf'] = WebBasicInf.objects.get()
    except WebBasicInf.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            question = form.cleaned_data['question']

            subject = '聯絡表單提交'
            message = f'姓名: {name}\n電子郵件: {email}\n電話號碼: {phone}\n提問內容: {question}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, context['profiles'].email]

            send_mail(subject, message, email_from, recipient_list)
            
            context["send_success"] = True

    else:
        form = ContactForm()

    context["form"] = form

    context["carousels"] = CarouselImage.objects.all()
    context["parents"] = SellerInfo.objects.all()


    html_template = loader.get_template('home/Front page.html')
    return HttpResponse(html_template.render(context, request))

def seller_detail_view(request, id):
    context = {}
    context["seller"] = get_object_or_404(SellerInfo, id=id)
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def pages(request):
    context = {}
    try:
        context['web_inf'] = WebBasicInf.objects.get()
    except WebBasicInf.DoesNotExist:
        pass
    try:
        load_template = request.path.split('/')[-1]
        
        # 後台
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        # 紀錄目前是哪個模板
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        traceback.print_exc()
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        traceback.print_exc()
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def product_list(request, seller_id):
    products = ProductInfo.objects.filter(seller__id=seller_id).values()
    return JsonResponse(list(products), safe=False)

def product_photos(request, product_id):
    images = ProductImage.objects.filter(product_id=product_id).values()
    return JsonResponse(list(images), safe=False)