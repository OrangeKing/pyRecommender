"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from maps.views import IndexView, PostDetailView, PostListView, PostAddView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^about/', TemplateView.as_view(template_name="about.html")),
    url(r'^contact/', TemplateView.as_view(template_name="contact.html")),

    url(r'^test-page/', include('django.contrib.flatpages.urls')),

    url(r'^posts/$', PostListView.as_view()),
    url(r'^posts/add/$', PostAddView.as_view()),
    url(r'^posts/user/(?P<slug>\w+)/$', PostListView.as_view()),
    url(r'^posts/(?P<slug>[\w-]+)/$', PostDetailView.as_view()),
]
