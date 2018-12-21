from django.contrib import admin
from .models import Poet, Poem


class PoetAdmin(admin.ModelAdmin):
    pass


class PoemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Poet, PoetAdmin)
admin.site.register(Poem, PoemAdmin)
