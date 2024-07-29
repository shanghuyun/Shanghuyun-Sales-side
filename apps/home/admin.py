from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import (
    Profile,
    WebBasicInf, 
    CarouselImage, 
    AboutUs,
    SellerInfo,
    ProductInfo,
    ProductImage,
    MapIframe
)

#############################################################
# 取消Group顯示
admin.site.unregister(Group)

#############################################################
# 不能刪除用戶

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

#############################################################
# 確保只有一個用戶

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def save_model(self, request, obj, form, change):
        # 限制只允許一個用戶存在
        if not change and User.objects.exists():
            raise Exception("只能存在一個用戶。")
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # 禁止在後台管理中添加新用戶
        if User.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#############################################################
# 個人資料顯示

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'real_name', 'contact_address', 'phone_number', 'facebook_link', 'instagram_link', 'youtube_link')

    def has_add_permission(self, request):
        # 限定只有一筆Profile
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.register(Profile, ProfileAdmin)

#############################################################
# 網頁基本資料

class WebBasicInfAdmin(admin.ModelAdmin):
    list_display = ('title', 'logo')

    def has_add_permission(self, request):
        # 禁止在後台管理中添加新 WebBasicInf 實例
        if WebBasicInf.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.register(WebBasicInf, WebBasicInfAdmin)

#############################################################
# 網頁輪播圖

class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

admin.site.register(CarouselImage, CarouselImageAdmin)

#############################################################
# 關於我們

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'simple_introduce', 'introduce', 'image')

    def has_add_permission(self, request):
        # 禁止在後台管理中添加新 AboutUs 實例
        if AboutUs.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.register(AboutUs, AboutUsAdmin)

#############################################################
# 新增賣家


class SellerInfoAdmin(admin.ModelAdmin):
    list_display = ('seller_name', 'seller_image', 'target_url')

admin.site.register(SellerInfo, SellerInfoAdmin)

#############################################################
# 地圖嵌入代碼

class MapIframeAdmin(admin.ModelAdmin):
    list_display = ('map_iframe',)

    def has_add_permission(self, request):
        # 禁止在後台管理中添加新 AboutUs 實例
        if MapIframe.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.register(MapIframe, MapIframeAdmin)

#############################################################
# 自定義管理站點的標題和標頭

admin.site.site_header = "管理後台"
admin.site.site_title = "管理站點標題"
admin.site.index_title = "管理站點首頁"
