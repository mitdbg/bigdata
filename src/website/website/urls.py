from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'home.views.home', name='home'),
    # url(r'^website/', include('website.foo.urls')),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'home/index.html'}),
    (r'^accounts/password_change_done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'home/index.html'}),
    (r'^accounts/password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'home/index.html'}),
    (r'^accounts/password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'home/index.html'}),
    #(r'^accounts/', include('registration.backends.simple.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('home.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
