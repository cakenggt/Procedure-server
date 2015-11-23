from django.conf.urls import url
from rest_framework.authtoken import views as authViews

from . import views

urlpatterns = [
    url(r'^api-token-auth/', authViews.obtain_auth_token),
    url(r'^get-all-checklists/$', views.GetAllChecklistsView.as_view(), name='get-all-checklists'),
    url(r'^create-checklist/$', views.CreateChecklistView.as_view(), name='create-checklist'),
    url(r'^save-checklist-order/$', views.SaveChecklistOrderView.as_view(), name='save-checklist-order'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^main/$', views.main, name='main'),
    url(r'^$', views.main, name='main'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^checklist/(?P<checklist_id>[0-9]+)/$', views.checklist, name='checklist'),
]
