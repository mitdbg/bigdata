from django.conf.urls import patterns, url

from home import views
from forms import SubmitForm

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^account$', views.profile, name='profile'),
  url(r'^visualization$', views.visualization, name='visualization'),
  url(r'^submitvis/$', views.submit_vis, name='submit_vis'),
  url(r'^submitvis$', views.submit_vis, name='submit_vis'),
  url(r'^prediction_test1$', views.test1, name='test1'),
  url(r'^prediction_test1/$', views.test1, name='test1'),
  url(r'^download/(?P<fname>\w+(\.\w+)*)$', views.download, name='download'),
  url(r'^stats/(?P<password>\w+)$', views.stats, name='stats'),
  url(r'^(?P<pagename>\w+)$', views.page, name="page"),
  #url(r'^info$', views.info, name='info'),
  #url(r'^prediction$', views.prediction, name='prediction'),
  #url(r'^visualization$', views.visualization, name='visualization')
)