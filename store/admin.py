from django.contrib import admin, messages #messages to show error, debug or other message
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse, re_path
from . import models


# It creates a filter for the admin page with different filters.
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory' #used in the query url

# returns a tuple for the filters
# It returns a list of tuples, where each tuple is a pair of values. 
# The first value is the value that will be stored in the database. 
# The second value is the human-readable name for the option that will appear in the admin.

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        """
        If the value of the filter is '<10', then return the queryset filtered by inventory less than 10
        """
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection'] #enable auto -complete
  # Used to create a slug field in the admin page. example brown-shoes , slug uses the - (hyphen)
    prepopulated_fields = {
        'slug': ['title']
    }
   
    actions = ['clear_inventory'] # Used to delete or clear the inventory and update it to the latest.
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]  #filtering on the right side of the admin page by invemtory
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

# used to delete or clear the inventory and update it to the latest
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        # A message that is displayed on the admin page when the inventory is cleared.
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    search_fields = ['title'] #used to auto complete when searching collections, it references the customer admin

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        re_path = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', re_path, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        re_path = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', re_path, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer'] #autocomplete when adding an order
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
