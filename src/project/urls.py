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
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from maps.views import IndexView, PostAddView, PostDetailView, PostListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^contact/', TemplateView.as_view(template_name="contact.html"), name='contact'),
    url(r'^test-page/', include('django.contrib.flatpages.urls')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^posts/', include('maps.urls', namespace='posts')),

    url(r'^seba/home/$', TemplateView.as_view(template_name="home_page.html")),
    url(r'^seba/logged/$', TemplateView.as_view(template_name="logged_in_page.html")),
    url(r'^seba/register/$', TemplateView.as_view(template_name="register_page.html")),
]
