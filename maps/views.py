import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import PostAddForm, UserForm
from .models import Post


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        num = None
        context = {
            "num": num
        }
        return context


class PostListView(ListView):
    template_name = "post_list.html"
    model = Post
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs) 
        return context

    def get_queryset(self):
        # slug = self.kwargs.get("slug")
        slug = self.request.GET.get('q')

        if slug:
            queryset = Post.objects.filter(
                # | Q(author__username__icontains=slug)
                Q(author__username__iexact=slug).order_by('-timestamp')
            )
        else:
            queryset = Post.objects.all().order_by('-timestamp')
        return queryset


class PostDetailView(DetailView):
    template_name = "post_detail.html"
    queryset = Post.objects.all()

    def get_object(self, queryset=queryset):
        obj = super(PostDetailView, self).get_object(queryset=queryset)
        return obj

    def grab_location_data(self):
        # free service for ip geolocaton
        GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
        IP_MAPS_API_URL = 'http://freegeoip.net/json'

        loc = self.get_object().location
        if loc is None:
            ip_req = requests.get(IP_MAPS_API_URL)
            ip_res = ip_req.json()
            latitude = ip_res['latitude']
            longitude = ip_res['longitude']

            params = {
                'latlng': '{},{}'.format(latitude, longitude),
            }

        else:
            params = {
                'address': loc,
                'sensor': 'false',
            }

        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        result = res['results'][0]
        place_id = result['place_id']

        return place_id

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['query_loc'] = self.grab_location_data()
        return context


class PostAddView(LoginRequiredMixin, CreateView):
    template_name = "post_add.html"
    form_class = PostAddForm
    success_url = "/posts/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserFormView(CreateView):
    template_name = "registration/register.html"
    form_class = UserForm
    success_url = "/"

    def form_valid(self, form):
        return super().form_valid(form)

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, context={'form': form})
