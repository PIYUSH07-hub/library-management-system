
from django.contrib import admin
from .models import Book, Member, Transaction

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'authors']

admin.site.register(Book, BookAdmin)
admin.site.register(Member)
admin.site.register(Transaction)



# https://frappe.io/api/method/frappe-library?title=Harry%20Potter&page=1