from django.contrib import admin

from .models import *

class ImagesTublerinLine(admin.TabularInline):
    model = Images

class TagTublerinLine (admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinLine,TagTublerinLine]

class OrderItemTubleinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubleinline]


admin.site.register(Images)
admin.site.register(Tag)

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(filter_price)
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact_us)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)