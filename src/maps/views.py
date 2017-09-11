from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import PostAddForm
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

    def queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Post.objects.filter(
                Q(author__username__iexact=slug) | Q(author__username__icontains=slug)
            )
        else:
            queryset = Post.objects.all()
        return queryset


class PostDetailView(DetailView):
    template_name = "post_detail.html"
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        return context


class PostAddView(CreateView):
    template_name = "post_add.html"
    form_class = PostAddForm
    success_url = "/posts/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
