from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from appel_crises.models import Signature, CallOutEmail

admin.site.unregister(Group)
admin.site.unregister(User)


class MyUserChangeForm(UserChangeForm):
    class Meta:
        fields = ["username", "password", "email", "is_active", "is_staff", "groups"]


@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
    )


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_filter = ("created_at",)
    list_display = (
        'email',
        'surname',
        'first_name',
        'created_at',
        'email_sent_at',
        'verified_at',
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CallOutEmail)
class CallOutEmailAdmin(admin.ModelAdmin):
    list_filter = ("created_at",)
    search_fields = ('email',)
    list_display = (
        'from_email',
        'sender',
        'postal_code',
        'circonscription_numbers',
        'send_to_government',
        'created_at',
        'email_sent_at',
        'verified_at',
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
