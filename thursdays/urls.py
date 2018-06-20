from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'thursdays'

urlpatterns = [
    url(r'^$', views.ThursdayListView.as_view(), name='homepage'),
    url(r'^register/', views.ThursdayCreateView.as_view(), name='thursday-register'),
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^detail/(?P<pk>\d+)/$', views.ThursdayDetailView.as_view(), name='thursday-detail'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<pk>\d+)/$',
        views.activate, name='confirm'),
    url(r'^deactivate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.deactivate, name='deny'),
    url(r'^ajax/archived_current_pizza_my_mind_dates/', views.ArchiveView.as_view(), name='archive'),
    url(r'^update/(?P<pk>\d+)/$', views.ThursdayUpdateView.as_view(), name='thursday-update'),
    url(r'^all_thursdays/', views.PreviousPizzaMyMindListView.as_view(), name='all-thursdays'),
    url(r'^bind_form/(?P<pk>\d+)/$', views.bound_form, name='bind'),
    url(r'^create_thursdays/', views.create_thursdays, name='create_thursdays'),
    url(r'^contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    url(r'^clear_thursday_data/(?P<pk>\d+)/$', views.ThursdayClearData.as_view(), name='thursday-clear-data'),
    url(r'^delete_thursday/(?P<pk>\d+)/$', views.delete_thursday, name='delete_thursday'),
    url(r'^invoice/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<pk>\d+)/$',
        views.invoice, name='invoice')
]
