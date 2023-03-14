from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Contact)

admin.site.register(Skills)

admin.site.register(PortfolioProjects)
#class PortfolioProjectAdmin(admin.ModelAdmin):
    #readonly_fields = ('slug')

admin.site.register(PortfolioProfile)

admin.site.register(Home)

admin.site.register(About)
