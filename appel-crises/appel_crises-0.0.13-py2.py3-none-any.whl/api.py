"""Real signature module."""

from django.core.exceptions import ValidationError
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse,
    HttpResponse,
)
from django.middleware import csrf
from django.shortcuts import redirect

from appel_crises.data import POSTAL_CODE_TO_DISTRICT, DISTRICT_TO_MP
from appel_crises.models import Signature, CallOutEmail


def sign(request: HttpRequest, is_ajax=False):
    """Main signature function"""
    # noinspection PyArgumentList
    try:
        first_name = request.POST['firstname']
        surname = request.POST['surname']
        email = request.POST['email']
    except KeyError as e:
        return HttpResponseBadRequest(f"Le champs {e} est requis.")

    signature = Signature(first_name=first_name, surname=surname, email=email)

    try:
        # Validate, among other things, the uniqueness of the email
        signature.full_clean()
    except ValidationError as e:
        # Probably a duplicate email, or a wrong email, or too long values
        return HttpResponseBadRequest("<br/>".join(e.messages))

    # I would put a try catch, but at this point i don't know what could go wrong
    signature.save()

    if is_ajax:
        return HttpResponse(status=200)
    else:
        return redirect('success')


def call_out_ajax(request: HttpRequest):
    """Form submission via an XHR request in the browser"""
    fields = [
        "content",
        "subject",
        "send_to_government",
        "circonscription_number",
        "sender",
        "from_email",
        "postal_code",
    ]
    try:
        values = {field: request.POST[field] for field in fields}
    except KeyError as e:
        return HttpResponseBadRequest(e)
    call_out_email = CallOutEmail(**values)
    call_out_email.send_to_government = int(call_out_email.send_to_government)

    try:
        call_out_email.full_clean()
    except ValidationError as e:
        # Probably a duplicate email, or a wrong email, or too long values
        return HttpResponseBadRequest(e)

    if call_out_email.circonscription_number not in DISTRICT_TO_MP:
        return HttpResponseBadRequest("Circonscription number not found")

    call_out_email.save()

    return HttpResponse(status=200)


def call_out(request: HttpRequest):
    """Form submission from no js page"""
    fields = [
        "content",
        "subject",
        "sender",
        "from_email",
        "postal_code",
    ]
    try:
        values = {field: request.POST[field] for field in fields}
    except KeyError as e:
        return HttpResponseBadRequest(e)
    call_out_email = CallOutEmail(**values)

    # noinspection PyCallByClass,PyTypeChecker
    if request.POST.get("send_to_government", "off") == 'on':
        call_out_email.send_to_government = 1
    else:
        call_out_email.send_to_government = False

    try:
        call_out_email.full_clean()
    except ValidationError as e:
        # Probably a duplicate email, or a wrong email, or too long values
        return HttpResponseBadRequest(e)

    # noinspection PyTypeChecker,PyCallByClass
    if request.POST.get("send_to_depute", False):
        postal_code = call_out_email.postal_code
        if postal_code not in POSTAL_CODE_TO_DISTRICT:
            return HttpResponseBadRequest("Postal code not found.")

        circo_number = POSTAL_CODE_TO_DISTRICT[postal_code][0]
        if circo_number not in DISTRICT_TO_MP:
            return HttpResponseBadRequest(
                "We don't know your circonscription. "
                "Please try and send him directly an email."
            )

        call_out_email.circonscription_number = circo_number

    call_out_email.save()

    return redirect("success-email")


def search_depute(request: HttpRequest):
    """Take input as POST parameter and return the corresponding depute as JSON"""

    postal_code = request.POST['postal_code']

    if postal_code not in POSTAL_CODE_TO_DISTRICT:
        return HttpResponseNotFound()

    districts = POSTAL_CODE_TO_DISTRICT[postal_code]

    mp_data = [(*DISTRICT_TO_MP[d], d) for d in districts if d in DISTRICT_TO_MP]

    # We have to pass safe=False, because we want to serialize an Array, see:
    # https://docs.djangoproject.com/en/3.0/ref/request-response/#serializing-non-dictionary-objects
    return JsonResponse(mp_data, safe=False)


def get_csrf_token(request: HttpRequest):
    """
    Return a CSRF token. Nothing big to do here, everything is done by the CSRF
    middleware.
    """
    return HttpResponse(csrf.get_token(request))
