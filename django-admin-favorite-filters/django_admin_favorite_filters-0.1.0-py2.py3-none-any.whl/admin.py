from django import forms
from django.contrib import admin
from django.forms import HiddenInput, TextInput
from django.utils.safestring import mark_safe

from .models import FavoriteFilter


class ReadOnlyWidget(forms.Widget):
    def __init__(self, original_value, display_value):
        self.original_value = original_value
        self.display_value = display_value

        super(ReadOnlyWidget, self).__init__()

    def render(self, name, value, attrs=None, renderer=None):
        if self.display_value is not None:
            return mark_safe(self.display_value)
        return str(self.original_value)

    def value_from_datadict(self, data, files, name):
        return self.original_value


class FavoriteFilterAdminForm(forms.ModelForm):

    class Meta:
        model = FavoriteFilter
        exclude = ("date_created", )

    def __init__(self, *args, **kwargs):
        super(FavoriteFilterAdminForm, self).__init__(*args, **kwargs)
        self.fields["user"].initial = self.request.user
        # self.fields["user"].widget = ReadOnlyWidget(original_value=self.request.user.id, display_value=self.request.user)
        self.fields["filtered_model"].disabled = True
        self.fields["query_parameters"].disabled = True
        self.fields["query_parameters"].widget = TextInput()


class FavoriteFilterAdmin(admin.ModelAdmin):
    list_display = ('filtered_model', 'name', 'date_created', 'is_public')
    form = FavoriteFilterAdminForm
    readonly_fields = ['date_created']
    fieldsets = [
        ("", {
            "fields": ['name', 'is_public'],
        }),

        ("Information", {
            "classes": ("collapse",),
            "fields": ('filtered_model', 'query_parameters', 'user', 'date_created'),
        }),

    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(FavoriteFilterAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form


admin.site.register(FavoriteFilter)
