"""Module that provides the views of the app."""
from django.http import HttpRequest
from django.shortcuts import render

from appel_crises.constants import ASSOCIATIONS
from appel_crises.models import Signature


def home(request: HttpRequest):
    """Home view."""
    signatures = '{:,}'.format(Signature.get_count()).replace(',', ' ')
    context = dict(counter=signatures, associations=ASSOCIATIONS,)
    return render(request, "home.html", context=context)


def success(request: HttpRequest):
    """Signature success page"""
    return render(request, "success.html")


def success_email(request: HttpRequest):
    """Signature success page"""
    return render(request, "success_email.html")


def form_no_js(request: HttpRequest):
    """Special page without js for signature"""
    return render(request, "form_no_js.html")


def call_out_no_js(request: HttpRequest):
    """Special page without js for call_out"""
    return render(request, "call_out_no_js.html")
