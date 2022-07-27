from django.contrib import admin

from organisations.models import Organisation, Invitation

admin.site.register(Organisation)
admin.site.register(Invitation)
