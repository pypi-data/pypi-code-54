from django.contrib import admin
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_dashboard.url_names import url_names
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import mapitio_screening_admin
from ..eligibility import format_reasons_ineligible
from ..forms import SubjectScreeningForm
from ..models import SubjectScreening


@admin.register(SubjectScreening, site=mapitio_screening_admin)
class SubjectScreeningAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):
    form = SubjectScreeningForm

    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    additional_instructions = ""

    fieldsets = (
        [
            None,
            {"fields": ("report_datetime", "first_name", "last_name", "initials",),},
        ],
        [
            "Demographics",
            {"fields": ("age_in_years", "dob", "is_dob_estimated", "gender",)},
        ],
        [
            "Identity",
            {
                "fields": (
                    "hospital_identifier",
                    "confirm_hospital_identifier",
                    "ctc_identifier",
                    "confirm_ctc_identifier",
                )
            },
        ],
        ["Patient File", {"fields": ("file_number",)}],
        ["Enrollment", {"fields": ("clinic_registration_date", "last_clinic_date")},],
        audit_fieldset_tuple,
    )

    list_display = (
        "hospital_identifier",
        "clinic_registration_date",
        "age_in_years",
        "gender",
        "ctc_identifier",
        "user_created",
        "created",
    )

    list_filter = (
        "report_datetime",
        "clinic_registration_date",
        "gender",
    )

    search_fields = (
        "hospital_identifier",
        "subject_identifier",
        "ctc_identifier",
        "initials",
        "reasons_ineligible",
    )

    radio_fields = {
        "gender": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
    }

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    def demographics(self, obj=None):
        return mark_safe(
            f"{obj.get_gender_display()} {obj.age_in_years}yrs {obj.initials.upper()}"
        )

    def reasons(self, obj=None):
        return format_reasons_ineligible(obj.reasons_ineligible)

    def eligiblity_status(self, obj=None):
        return "Eligible" if obj.eligible else "Ineligible"

    def dashboard(self, obj=None, label=None):
        try:
            url = reverse(
                self.get_subject_dashboard_url_name(),
                kwargs=self.get_subject_dashboard_url_kwargs(obj),
            )
        except NoReverseMatch:
            url = reverse(url_names.get("screening_listboard_url"), kwargs={})
            context = dict(
                title=_("Go to enrollment listboard"),
                url=f"{url}?q={obj.screening_identifier}",
                label=label,
            )
        else:
            context = dict(title=_("Go to subject dashboard"), url=url, label=label)
        return render_to_string("dashboard_button.html", context=context)
