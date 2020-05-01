#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from example_project.forms import MDeditorTestForm


def test_form_view(request):
    form = MDeditorTestForm()
    return render(request, "example_project/home.html", {'form': form})


