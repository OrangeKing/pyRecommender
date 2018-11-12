import requests
import random
import tmdbsimple as tmdb

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.template import RequestContext, Context


from .forms import PostAddForm, UserForm
from .models import Post, movies, links, Profile

from .recommendation import *

tmdb.API_KEY = '568dc1eab493883fb6a83c2ae42234d2'

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


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
                Q(author__username__iexact=slug)
            )
            queryset.order_by('-timestamp')
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
        #context['query_loc'] = self.grab_location_data()
        return context


class PostAddView(LoginRequiredMixin, CreateView):
    template_name = "post_add.html"
    form_class = PostAddForm
    success_url = "/posts/"

    def get(self, request):
        instance = Profile.objects.get(user=request.user)
        vectorized_watchlist = get_watchlist(instance.watchlist)
        watchlist = []
        for movie_id in vectorized_watchlist:
            mov = movies.objects.get(imdb_id=movie_id)
            watchlist.append({'imdb_id': mov.imdb_id, 'movie_name': mov.movie_name, 'movie_id': mov.movie_id})

        variables = {
        'watchlist': watchlist
        }
		

        return render(request, self.template_name, context=variables)

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


class MovieView(DetailView):
    template_name = 'movie.html'

    def get_movie_status(self, watchlist, slug):
        data = watchlist.split(",")
        return slug in data

    def get_movie_data(self, slug):
        instance = Profile.objects.get(user=self.request.user)
        movie_status = self.get_movie_status(instance.watchlist,str(slug))

        imdb_id = str(slug)
        external_source = 'imdb_id'

        find = tmdb.Find('tt0'+imdb_id)
        resp = find.info(external_source=external_source)

        if not resp['movie_results']:
            find = tmdb.Find('tt00'+imdb_id)
            resp = find.info(external_source=external_source)

        if not resp['movie_results']:
            find = tmdb.Find('tt'+imdb_id)
            resp = find.info(external_source=external_source)

        id = find.movie_results[0]['id']
        movie = tmdb.Movies(id)
        movie_info = movie.info()
        
        context = {}
        context['status'] = movie_status
        context['title'] = movie_info['title']
        context['genres'] = movie_info['genres']
        context['overview'] = movie_info['overview']
        context['runtime'] = movie_info['runtime']
        context['score'] = movie_info['vote_average']

        movie_credits = movie.credits()
        context['crew'] = movie_credits['crew']
        context['director'] = [ context['crew'][i]['name'] for i in range(len(context['crew'])) if context['crew'][i]['job'] == 'Director' ]
        context['cast'] = movie_credits['cast'][:12]
        context['poster'] = "https://image.tmdb.org/t/p/w500" + movie.poster_path

        return context

    def update_watchlist(self, watchlist, slug):
        new_watchlist = watchlist + slug + ","
        return new_watchlist

    def get(self, request, slug):
        query = ""
        if request.GET:
            query = request.GET['query']
        return render(request, self.template_name, context=self.get_movie_data(slug))


    def post(self, request, slug):
        success_url = "/mymovies/"

        instance = Profile.objects.get(user=self.request.user)
        instance.watchlist = self.update_watchlist(instance.watchlist,str(slug))
        instance.save()  
  
        return HttpResponseRedirect(success_url)


class MovSearchView(DetailView):
    template_name = 'movie_search.html'
    def get(self, request):
        query = ""
        if request.GET:
            query = request.GET['query']

        return render(request, self.template_name)

def search(request):
    template_name = "movie_search.html"
    query = "no results found"
    neighbors = []
    recommended = []
    results = []
    posters = []
    show_results = False
    no_data = False

    if request.GET:
        query = request.GET['query']
        results = movies.objects.filter (movie_name__icontains=query)[:10]

        if results:
            show_results = True
            neighbors = recommend(results[0].movie_id)

            for i in neighbors[:10]:
                recommends = movies.objects.get(movie_id=i)
                recommended.append(recommends)
                poster = links.objects.get(movie_id=i)
                posters.append(poster)

        else:
            no_data = True

    variables = {
        'posters': posters,
        'recommended': recommended,
        'results': results,
        'show_results': show_results,
        'no_data': no_data
    }
		
    return render(request, template_name, context=variables)

def get_watchlist(watchlist):
    data = watchlist.split(",")
    data = list(filter(None, data))
    return data

def profile(request):
    template_name = "movie_profile.html"

    instance = Profile.objects.get(user=request.user)
    vectorized_watchlist = get_watchlist(instance.watchlist)
    watchlist = []
    for movie_id in vectorized_watchlist:
        mov = movies.objects.get(imdb_id=movie_id)
        watchlist.append({'imdb_id': mov.imdb_id, 'movie_name': mov.movie_name, 'movie_id': mov.movie_id})

    neighbors = []
    recommended = []
    results = []
    show_results = False

    if watchlist:
        results = movies.objects.filter (movie_name__icontains=watchlist[0]['movie_name'])[:10]

    if results:
        show_results = True
        sample = random.choice(watchlist)
        neighbors = recommend(sample['movie_id'])

        for i in neighbors[:10]:
            recommends = movies.objects.get(movie_id=i)
            recommended.append(recommends)

    variables = {
        'watchlist': watchlist,
        'recommended': recommended,
        'results': results,
        'show_results': show_results
    }
		
    return render(request, template_name, context=variables)
