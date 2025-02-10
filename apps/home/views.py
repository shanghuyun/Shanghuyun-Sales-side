import traceback
from django import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from .models import (
    Profile, WebBasicInf, CarouselImage, AboutUs, SellerInfo, ProductInfo, 
    ProductImage, MapIframe, Order, OrderItem, ShippingInfo, ECPayInfo
)
from .forms import ContactForm, ShippingInfoForm
from apps.ecpay_payment_sdk import ECPayPaymentSdk
import json
from datetime import datetime

# 發送訂單確認郵件
def send_order_confirmation_email(order, shipping_info, isSeller=False):
    try:
        # 獲取用戶的電子郵件
        profile_email = Profile.objects.get(user=order.user).email
    except Profile.DoesNotExist:
        profile_email = ''
    
    # 構建訂單項目的 HTML 列表
    items_html = "".join([f'<li>{item.product.name} x {item.quantity}</li>' for item in order.items.all()])
    
    # 設定郵件主題和收件人
    subject = '新訂單通知' if isSeller else '訂單成立通知'
    recipient_email = profile_email if isSeller else shipping_info.email
    
    # 設定郵件內容
    message_intro = f'您有一筆新訂單 {order.merchant_trade_no}，請盡快出貨。' if isSeller else f'您的訂單 {order.merchant_trade_no} 已成立，請等待出貨通知。'
    
    # 構建郵件的 HTML 內容
    order_msg = """
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
                border-radius: 8px;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                padding: 5px 0;
            }}
            .total {{
                font-weight: bold;
                margin-top: 20px;
            }}
            .info {{
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{subject}</h1>
            <p>{message_intro}</p>
            <p>細項如下：</p>
            <ul>
                {items_html}
            </ul>
            <p class="total">總金額：{total_amount}</p>
            <div class="info">
                <p>收件人：{recipient_name}</p>
                <p>地址：{address}</p>
                <p>電話：{phone_number}</p>
                {email_info}
            </div>
        </div>
    </body>
    </html>
    """.format(
        subject=subject,
        message_intro=message_intro,
        items_html=items_html,
        total_amount=order.total_amount,
        recipient_name=shipping_info.recipient_name,
        address=shipping_info.address,
        phone_number=shipping_info.phone_number,
        email_info=f'<p>Email：{shipping_info.email}</p>' if isSeller else ''
    )

    # 發送郵件
    send_mail(
        subject,
        '',
        settings.EMAIL_HOST_USER,
        [recipient_email],
        html_message=mark_safe(order_msg)
    )

# 首頁視圖
def index(request):
    context = {}
    try:
        # 獲取管理員的個人資料
        admin_user = User.objects.get(is_superuser=True)
        context['profiles'] = Profile.objects.get(user=admin_user)
    except Profile.DoesNotExist:
        pass
    try:
        # 獲取地圖 iframe
        context['mapIframe'] = MapIframe.objects.get()
    except MapIframe.DoesNotExist:
        pass
    try:
        # 獲取關於我們的信息
        context['about'] = AboutUs.objects.get()
    except AboutUs.DoesNotExist:
        pass
    try:
        # 獲取網站基本信息
        context['web_inf'] = WebBasicInf.objects.get()
    except WebBasicInf.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # 獲取表單數據
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            question = form.cleaned_data['question']

            # 構建郵件內容
            subject = '聯絡表單提交'
            message = f'姓名: {name}\n電子郵件: {email}\n電話號碼: {phone}\n提問內容: {question}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, context['profiles'].email]

            # 發送郵件
            send_mail(subject, message, email_from, recipient_list)
            
            context["send_success"] = True

    else:
        form = ContactForm()

    context["form"] = form
    context["carousels"] = CarouselImage.objects.all()
    context["parents"] = SellerInfo.objects.all()

    html_template = loader.get_template('home/Front page.html')
    return HttpResponse(html_template.render(context, request))

# 賣家詳細信息視圖
@csrf_exempt
def seller_detail_view(request, id):
    context = {}
    # 獲取賣家信息
    context["seller"] = get_object_or_404(SellerInfo, id=id)
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

# 靜態頁面視圖
def pages(request):
    context = {}
    try:
        # 獲取網站基本信息
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

# 商品列表視圖
def product_list(request, seller_id):
    # 獲取賣家的商品列表
    products = ProductInfo.objects.filter(seller__id=seller_id).values()
    return JsonResponse(list(products), safe=False)

# 商品照片視圖
def product_photos(request, product_id):
    # 獲取商品的照片列表
    images = ProductImage.objects.filter(product_id=product_id).values()
    return JsonResponse(list(images), safe=False)

# 結帳視圖
@login_required(login_url="account_login")
@csrf_exempt
def checkout(request):
    print(request.user)
    if request.method == 'POST':
        try:
            # 獲取綠界支付信息
            ecpay_info = ECPayInfo.objects.get()
        except ECPayInfo.DoesNotExist:
            return JsonResponse({'error': '商家尚未建立付款資訊'}, status=404)
        try:
            # 獲取購物車數據
            cart = json.loads(request.body)
            product_ids = [item['product_id'] for item in cart]
            products = ProductInfo.objects.filter(id__in=product_ids)

            if not products:
                return JsonResponse({'error': 'Products not found'}, status=404)

            total_amount = 0
            item_names = []
            # 創建訂單
            order = Order.objects.create(
                merchant_trade_no=datetime.now().strftime("NO%Y%m%d%H%M%S") + str(request.user.id),
                user=request.user,
                total_amount=0,
                status='尚未付款'
            )

            for item in cart:
                product = products.get(id=item['product_id'])
                total_amount += product.price * item['quantity']
                item_names.append(f"{product.name} x {item['quantity']}")
                # 創建訂單項目
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )

            order.total_amount = total_amount
            order.save()

            item_name_str = '#'.join(item_names)

            # 使用硬編碼的 URL
            url = request.build_absolute_uri(reverse('payment_callback'))
            back_shop_url = request.build_absolute_uri(reverse('seller_detail', args=[products[0].seller.id]))
            
            # 設定訂單參數
            order_params = {
                'MerchantTradeNo': order.merchant_trade_no,
                'StoreID': '',
                'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                'PaymentType': 'aio',
                'TotalAmount': total_amount,
                'TradeDesc': '訂單測試',
                'ItemName': item_name_str,
                'ReturnURL': url,
                'ChoosePayment': 'ALL',
                'ClientBackURL': back_shop_url,  # 成功後導向的 URL
                'ItemURL': back_shop_url,
                'Remark': '交易備註',
                'ChooseSubPayment': '',
                'OrderResultURL': url,  # 成功後導向的 URL
                'NeedExtraPaidInfo': 'Y',
                'DeviceSource': '',
                'IgnorePayment': '',
                'PlatformID': '',
                'InvoiceMark': 'N',
                'CustomField1': '',
                'CustomField2': '',
                'CustomField3': '',
                'CustomField4': '',
                'EncryptType': 1,
            }

            extend_params_1 = {
                'ExpireDate': 7,
                'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
                'ClientRedirectURL': '',
            }

            extend_params_2 = {
                'StoreExpireDate': 15,
                'Desc_1': '',
                'Desc_2': '',
                'Desc_3': '',
                'Desc_4': '',
                'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
                'ClientRedirectURL': '',
            }

            extend_params_3 = {
                'BindingCard': 0,
                'MerchantMemberID': '',
            }

            extend_params_4 = {
                'Redeem': 'N',
                'UnionPay': 0,
            }

            inv_params = {
                # 'RelateNumber': 'Tea0001', # 特店自訂編號
                # 'CustomerID': 'TEA_0000001', # 客戶編號
                # 'CustomerIdentifier': '53348111', # 統一編號
                # 'CustomerName': '客戶名稱',
                # 'CustomerAddr': '客戶地址',
                # 'CustomerPhone': '0912345678', # 客戶手機號碼
                # 'CustomerEmail': 'abc@ecpay.com.tw',
                # 'ClearanceMark': '2', # 通關方式
                # 'TaxType': '1', # 課稅類別
                # 'CarruerType': '', # 載具類別
                # 'CarruerNum': '', # 載具編號
                # 'Donation': '1', # 捐贈註記
                # 'LoveCode': '168001', # 捐贈碼
                # 'Print': '1',
                # 'InvoiceItemName': '測試商品1|測試商品2',
                # 'InvoiceItemCount': '2|3',
                # 'InvoiceItemWord': '個|包',
                # 'InvoiceItemPrice': '35|10',
                # 'InvoiceItemTaxType': '1|1',
                # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
                # 'DelayDay': '0', # 延遲天數
                # 'InvType': '07', # 字軌類別
            }

            # 初始化 ECPayPaymentSdk
            ecpay = ECPayPaymentSdk(MerchantID=ecpay_info.merchant_id, HashKey=ecpay_info.hash_key, HashIV=ecpay_info.hash_iv)

            # 合併延伸參數
            order_params.update(extend_params_1)
            order_params.update(extend_params_2)
            order_params.update(extend_params_3)
            order_params.update(extend_params_4)

            # 合併發票參數
            order_params.update(inv_params)

            # 產生綠界訂單所需參數
            final_order_params = ecpay.create_order(order_params)
            # 產生 html 的 form 格式
            # action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
            action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
            html = ecpay.gen_html_post_form(action_url, final_order_params)

            print('訂單參數:', final_order_params)

            return HttpResponse(html)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# 綠界支付回調視圖
@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        data = request.POST
        merchant_trade_no = data.get('MerchantTradeNo')
        rtn_code = data.get('RtnCode')
        rtn_msg = data.get('RtnMsg')
        trade_no = data.get('TradeNo')
        trade_amt = data.get('TradeAmt')
        payment_date = data.get('PaymentDate')
        payment_type = data.get('PaymentType')
        trade_date = data.get('TradeDate')
        simulate_paid = data.get('SimulatePaid')

        print(data)

        # 處理付款完成的邏輯，例如更新訂單狀態
        if rtn_code == '1':
            # 付款成功，更新訂單狀態
            try:
                order = Order.objects.get(merchant_trade_no=merchant_trade_no)
                order.status = '已付款'
                order.save()
                print('付款成功')
                return redirect(reverse('shipping_info', args=[order.id]))
            except Order.DoesNotExist:
                return HttpResponse('訂單不存在', status=404)
        else:
            try:
                order = Order.objects.get(merchant_trade_no=merchant_trade_no)
                order.status = '付款失敗'
                order.save()
                print('付款失敗')
            except Order.DoesNotExist:
                return HttpResponse('訂單不存在', status=404)
            return HttpResponse('付款失敗')

        return HttpResponse('OK')
    return HttpResponse('Invalid request method', status=405)

# 運送信息視圖
@login_required(login_url="account_login")
def shipping_info(request, order_id):
    try:
        # 獲取訂單
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return HttpResponse('訂單不存在', status=404)
    
    try:
        # 獲取用戶的電子郵件
        profile_email = Profile.objects.get(user=request.user).email
    except Profile.DoesNotExist:
        profile_email = ''

    if request.method == 'POST':
        form = ShippingInfoForm(request.POST)
        if form.is_valid():
            try:
                # 檢查是否已存在運送信息
                shipping_info = ShippingInfo.objects.get(order=order)
                return redirect('order_history')
            except ShippingInfo.DoesNotExist:
                # 保存運送信息
                shipping_info = form.save(commit=False)
                shipping_info.order = order
                shipping_info.user = request.user
                shipping_info.save()

                # 寄送訂單成立通知(客戶)
                send_order_confirmation_email(order, shipping_info, isSeller=False)
                # 寄送訂單成立通知(賣家)
                send_order_confirmation_email(order, shipping_info, isSeller=True)
                return redirect('order_history')
    else:
        form = ShippingInfoForm()

    return render(request, 'home/shipping_info.html', {'form': form, 'order': order})

# 訂單歷史視圖
@login_required(login_url="account_login")
def order_history(request):
    # 獲取用戶的訂單歷史
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_info = []
    for order in orders:
        items = list(order.items.all())
        try:
            shipping_info = ShippingInfo.objects.get(order=order)
            has_shipping_info = True
        except ShippingInfo.DoesNotExist:
            has_shipping_info = False
        order_info.append({
            'order': order,
            'items': items,
            'has_shipping_info': has_shipping_info
        })
    return render(request, 'home/order_history.html', {'order_info': order_info})
