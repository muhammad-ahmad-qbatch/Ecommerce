from django.contrib import admin
from .models import *

admin.site.register(Buyer)
admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Checkout)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name','content_type','object_id','content_object']
    fields = ['name','content_type','object_id', 'content_object']
    readonly_fields = ['content_object']
    class Meta:
        model = Tag
# Register your models here.

