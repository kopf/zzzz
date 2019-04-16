from django.contrib import admin
from django.utils.html import format_html_join

from api.models import User, Subdomain


class UserAdmin(admin.ModelAdmin):
    def subdomains(self):
        html = '<a href="/admin/api/subdomain/{}/">{}</a>'
        data = ((subdomain.id, subdomain.name) for subdomain in Subdomain.objects.filter(user__id=self.id))
        return format_html_join(', ', html, data)
    model = User
    list_display = ('id', 'username', 'email', subdomains, 'token', 'user_class', 'date_joined')
    search_fields = ['username', 'email', 'token']


class SubdomainAdmin(admin.ModelAdmin):
    model = Subdomain
    list_display = ('name', 'user', 'ip', 'ipv6')
    search_fields = ['name', 'user__username']

admin.site.register(User, UserAdmin)
admin.site.register(Subdomain, SubdomainAdmin)
