from django.contrib import admin
from geo.models import Foo
from geo.forms import FooForm


class FooAdmin(admin.ModelAdmin):
    form = FooForm

    # prepopulated_fields = {'slug': ['title']}


admin.site.register(Foo, FooAdmin)