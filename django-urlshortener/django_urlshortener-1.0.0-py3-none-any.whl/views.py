from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from urlshortener.models import URLShortenerModel
from urlshortener.modelforms import URLShortenerModelForm


""" Homepage Template view """
class HomepageTemplateView(TemplateView):
    template_name = "vantage/urlshortener/homepage_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = URLShortenerModelForm()
        return context


""" Homepage Form view. """
class HomepageFormView(SuccessMessageMixin, FormView):
    template_name = "vantage/urlshortener/homepage_view.html"
    form_class = URLShortenerModelForm
    success_url = reverse_lazy("urlshortener:homepage")
    success_message = None

    def form_valid(self, form):
        form.save()
        self.success_message = form.instance.slug
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return(f"http://{self.request.headers['Host']}/{self.success_message}")


""" Homepage view configurations. """
class HomepageView(View):
    def get(self, request, *args, **kwargs):
        view = HomepageTemplateView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = HomepageFormView.as_view()
        return view(request, *args, **kwargs)


""" URL Shortener Detail View. """
class URLShortenerDetailView(DetailView):
    template_name = "vantage/urlshortener/url_shortener_detail_view.html"
    model = URLShortenerModel
    slug_url_kwarg = "slug"
