from django.conf.urls import url

from .views import PostAddView, PostDetailView, PostListView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='list'),
    url(r'^add/$', PostAddView.as_view(), name='add'),
    url(r'^user/(?P<slug>\w+)/$', PostListView.as_view(), name='user'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),
]
