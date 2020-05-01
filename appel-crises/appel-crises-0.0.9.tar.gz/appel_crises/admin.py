from django.contrib import admin

from appel_crises.models import Signature, CallOutEmail


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
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


@admin.register(CallOutEmail)
class CallOutEmailAdmin(admin.ModelAdmin):
    list_display = (
        'from_email',
        'sender',
        'postal_code',
        'circonscription_number',
        'send_to_government',
        'created_at',
        'email_sent_at',
        'verified_at',
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
