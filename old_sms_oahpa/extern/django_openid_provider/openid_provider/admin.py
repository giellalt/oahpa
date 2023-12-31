from django.contrib import admin

from openid_provider.models import TrustedRoot, OpenID

class TrustedRootInline(admin.TabularInline):
    model = TrustedRoot

class OpenIDAdmin(admin.ModelAdmin):
    list_display = ['openid', 'user', 'default']
    inlines = [TrustedRootInline, ]

admin.site.register(OpenID, OpenIDAdmin)
