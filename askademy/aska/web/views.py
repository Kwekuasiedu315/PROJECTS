from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import generic

from records.users.forms import UpdateUserForm
from records.users.models import CustomUser
from records.feeds.models import Post

from . import dummy


class HomePageView(TemplateView):
    template_name = "web/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        return context


def about_view(request):
    return render(request, template_name="web/about_askademy.html")


def search_results(request):
    query = request.GET.get("q", "")
    name_filter = request.GET.get("name", "")
    location_filter = request.GET.get("location", "")
    job_title_filter = request.GET.get("job_title", "")

    # Filter the dummy data based on the search criteria
    results = []
    for item in dummy.dummy_data:
        if query and query.lower() not in item.name.lower():
            continue
        if name_filter and name_filter.lower() not in item.name.lower():
            continue
        if location_filter and location_filter.lower() not in item.location.lower():
            continue
        if job_title_filter and job_title_filter.lower() not in item.job_title.lower():
            continue
        results.append(item)

    # Paginate the search results
    paginator = Paginator(results, 10)  # Show 10 results per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "name_filter": name_filter,
        "location_filter": location_filter,
        "job_title_filter": job_title_filter,
        "results": page_obj,
    }
    return render(request, "web/search_results.html", context)


class UpdateUserProfileView(generic.UpdateView):
    model = CustomUser
    form_class = UpdateUserForm
    template_name = "auth/user_update.html"
    success_url = reverse_lazy("web:home")

    def get_object(self, *args, **kwargs):
        return self.request.user
