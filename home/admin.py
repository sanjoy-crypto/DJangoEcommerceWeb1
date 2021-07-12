from django.contrib import admin
from .models import *


# Register your models here.


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']
    list_filter = ['status']


admin.site.register(Setting, SettingAdmin)


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer', 'image_tag']


admin.site.register(SliderImage, SliderImageAdmin)


class OfferImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']


admin.site.register(OfferImage, OfferImageAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'status',
                    'note', 'create_at', 'update_at']
    readonly_fields = ['name', 'email', 'subject', 'message', 'ip']
    list_filter = ['status']


admin.site.register(ContactMessage, ContactMessageAdmin)


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','ordernumber','status']
    list_filter = ['status']
    
    

admin.site.register(FAQ,FAQAdmin)