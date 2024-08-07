import os
import requests
from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from colorfield.fields import ColorField
from urllib.parse import  urljoin

#############################################################
# 個人資料Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用戶')
    real_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='真實姓名')
    contact_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='聯絡地址')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='聯絡電話')
    email = models.EmailField(verbose_name="電子信箱")
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    facebook_link = models.URLField(blank=True, verbose_name='Facebook 連結')
    instagram_link = models.URLField(blank=True, verbose_name='Instagram 連結')
    youtube_link = models.URLField(blank=True, verbose_name='YouTube 連結')

    def __str__(self):
        return self.real_name if self.real_name else self.user.username

    class Meta:
        verbose_name = "1.個人資料"
        verbose_name_plural = "1.個人資料"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
#############################################################
# 網頁基本訊息

class WebBasicInf(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='網頁標題')
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name='網頁Logo')

    def __str__(self):
        return self.title if self.title else "未設置標題"

    class Meta:
        verbose_name = "2.網頁標題 & logo"
        verbose_name_plural = "2.網頁標題 & logo"

# 刪除舊文件
@receiver(pre_save, sender=WebBasicInf)
def delete_old_logo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = WebBasicInf.objects.get(pk=instance.pk).logo
        except WebBasicInf.DoesNotExist:
            return
        new_file = instance.logo
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

# 刪除文件
@receiver(post_delete, sender=WebBasicInf)
def delete_logo_file(sender, instance, **kwargs):
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


#############################################################
# 輪播圖

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/', verbose_name='輪播背景圖')

    header = models.CharField(max_length=10, blank=True, null=True, verbose_name='標頭')

    title = models.CharField(max_length=10, blank=True, null=True, verbose_name='標題')

    content = models.TextField(blank=True, null=True, verbose_name='內容描述')

    color = ColorField(default='#FF0000', verbose_name='文字顏色選擇')

    def __str__(self):
        return f"Carousel Image {self.id}"

    class Meta:
        verbose_name = "3.輪播圖"
        verbose_name_plural = "3.輪播圖"

# 刪除舊文件
@receiver(pre_save, sender=CarouselImage)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = CarouselImage.objects.get(pk=instance.pk).image
        except CarouselImage.DoesNotExist:
            return
        new_file = instance.image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

# 刪除文件
@receiver(post_delete, sender=CarouselImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

#############################################################
# 關於我們

class AboutUs(models.Model):
    title  = models.CharField(max_length=10, verbose_name='標題', help_text="至多10個字")
    simple_introduce = models.CharField(max_length=100, blank=True, null=True, verbose_name='簡單介紹', help_text="至多100個字")
    introduce = models.TextField(blank=True, null=True, verbose_name='完整介紹')
    link = models.URLField(blank=True, null=True, verbose_name='外部連結')
    image = models.ImageField(upload_to='Aboutus')

    def __str__(self):
        return self.title if self.title else "未設置標題"

    class Meta:
        verbose_name = "4.關於我們"
        verbose_name_plural = "4.關於我們"

# 刪除舊文件
@receiver(pre_save, sender=AboutUs)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = AboutUs.objects.get(pk=instance.pk).image
        except AboutUs.DoesNotExist:
            return
        new_file = instance.image
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

# 刪除文件
@receiver(post_delete, sender=AboutUs)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

#############################################################
# 更新檔案儲存位置

def get_product_cover_image_upload_path(instance, filename):
    return f'products/{instance.product_name}/cover'

def get_product_image_upload_path(instance, filename):
    return f'products/{instance.product.product_name}/{filename}'

#############################################################
# 賣家資料

class SellerInfo(models.Model):
    seller_name = models.CharField(max_length=100, verbose_name='賣家姓名')
    seller_image = models.ImageField(upload_to='sellers/', verbose_name='圖片')
    target_url = models.URLField(verbose_name='目標網址')
    
    def __str__(self):
        return self.seller_name
    
    class Meta:
        verbose_name = "5.新增賣家"
        verbose_name_plural = "5.新增賣家"

@receiver(post_delete, sender=SellerInfo)
def delete_seller_image(sender, instance, **kwargs):
    if instance.seller_image:
        if os.path.isfile(instance.seller_image.path):
            os.remove(instance.seller_image.path)
    
#############################################################
# 商品資料

class ProductInfo(models.Model):
    seller = models.ForeignKey(SellerInfo, on_delete=models.CASCADE, related_name='products', verbose_name='賣家')
    name = models.CharField(max_length=100, verbose_name='姓名')
    email = models.EmailField(verbose_name='電子郵件')
    phone_number = models.CharField(max_length=20, verbose_name='電話號碼')
    address = models.CharField(max_length=255, verbose_name='地址')
    product_name = models.CharField(max_length=100, verbose_name='產品名稱')
    price = models.IntegerField(verbose_name='價格')
    description = models.TextField(verbose_name='描述')
    cover_image = models.ImageField(upload_to=get_product_cover_image_upload_path, verbose_name='商品封面圖片')

    def __str__(self):
        return self.product_name
    
@receiver(post_delete, sender=ProductInfo)
def delete_product_image(sender, instance, **kwargs):
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)

#############################################################
# 商品圖片

class ProductImage(models.Model):
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='images', verbose_name='產品')
    image = models.ImageField(upload_to=get_product_image_upload_path, verbose_name='商品照片')

    def __str__(self):
        return f'{self.product.product_name} - Image'

@receiver(post_delete, sender=ProductImage)
def delete_product_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
#############################################################
# 抓取商品資訊

@receiver(post_save, sender=SellerInfo)
def fetch_product_data(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                response = requests.get(f"{instance.target_url}/api/get_product_ids/")
                response.raise_for_status()
                product_ids = response.json()

                for product_id in product_ids:
                    product_response = requests.get(f"{instance.target_url}/api/get_product_details/{product_id}/")
                    product_response.raise_for_status()
                    product_data = product_response.json()

                    original_name = product_data['product_name']
                    unique_name = original_name
                    counter = 1

                    while ProductInfo.objects.filter(product_name=unique_name).exists():
                        unique_name = f"{original_name}_duplicate_{counter}"
                        counter += 1
                    
                    product_data['product_name'] = unique_name

                    cover_image_dir = os.path.join(settings.MEDIA_ROOT, 'products', unique_name)
                    if not os.path.exists(cover_image_dir):
                        os.makedirs(cover_image_dir)

                    cover_image_url = urljoin(instance.target_url, product_data['images'][0])
                    cover_image_name = 'cover.jpg'
                    cover_image_response = requests.get(cover_image_url)
                    cover_image_response.raise_for_status()
                    cover_image_path = os.path.join(cover_image_dir, cover_image_name)
                    with open(cover_image_path, 'wb') as f:
                        f.write(cover_image_response.content)

                    product = ProductInfo.objects.create(
                        seller=instance,
                        name=product_data['name'],
                        email=product_data['email'],
                        phone_number=product_data['phone_number'],
                        address=product_data['address'],
                        product_name=unique_name,
                        price=product_data['price'],
                        description=product_data['description'],
                        cover_image=os.path.join('products', unique_name, cover_image_name)
                    )

                    for i, image_url in enumerate(product_data['images'][1:]):
                        image_dir = os.path.join(settings.MEDIA_ROOT, 'products', unique_name)
                        if not os.path.exists(image_dir):
                            os.makedirs(image_dir)
                        full_image_url = urljoin(instance.target_url, image_url)
                        image_name = f'image{i}.jpg'
                        image_response = requests.get(full_image_url)
                        image_response.raise_for_status()
                        image_path = os.path.join(image_dir, image_name)
                        with open(image_path, 'wb') as f:
                            f.write(image_response.content)
                        ProductImage.objects.create(product=product, image=os.path.join('products', unique_name, image_name))
        except requests.exceptions.RequestException as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching product data: {e}")
            if instance.pk:
                instance.delete()
            raise
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"An unexpected error occurred: {e}")
            if instance.pk:
                instance.delete()
            raise

#############################################################
# 地圖資訊

class MapIframe(models.Model):
    map_iframe = models.TextField(
        help_text='''
        請輸入地圖的iframe，範例格式:
        <pre>
        &lt;iframe class="map" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3653.2541148558166!2d120.42691457479046!3d23.702617790610038!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x346eba072ee22f11%3A0x558aed05907207d7!2z5ZyL56uL6JmO5bC-56eR5oqA5aSn5a24!5e0!3m2!1szh-TW!2stw!4v1720886263664!5m2!1szh-TW!2stw" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"&gt;&lt;/iframe&gt;
        </pre>''',

        verbose_name='地圖嵌入代碼'
    )

    def __str__(self):
        return f"Product Image with map iframe"
    
    class Meta:
        verbose_name = "6.嵌入地圖"
        verbose_name_plural = "6.嵌入地圖"