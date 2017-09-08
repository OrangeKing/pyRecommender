from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from .models import Post
from .forms import PostAddForm


# Create your views here.
def post_add_view(request):
    form = PostAddForm(request.POST or None)
    errors = None
    if form.is_valid():
        author = request.user
        obj = Post.objects.create(
            author=author, 
            title=form.cleaned_data.get('title'), 
            contents=form.cleaned_data.get('contents'), 
            location=form.cleaned_data.get('location')
            )
        return HttpResponseRedirect("/posts/")

        if form.errors:
            errors = form.errors
            print(form.errors)

    template_name = "post_add.html"
    context = {"form": form, "errors": errors}
    return render(request, template_name, context)

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
