from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from mysite.views import *
from blog.views import *
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$',showBlogFirstList),
    (r'^blog/(\d+)/$',showBlogDetail),
    (r'^blog/$', showBlogFirstList),
    (r'^blog/page/(\d+)/$', showBlogList),
    (r'^blog/(\d{4})/(\d{2})/$', showBlogArchive),
    (r'^blog/category/(.*)/$', showBlogCategory),
    (r'^blog/setComment/$', setComment),
    (r'^search/$', search),
    (r'^about/$', about),
    (r'^resume/$', resume),
    (r'^resume/setMessage/$', setMessage),
    (r'^saying/$', saying),
    (r'^saying/setFavourite/$', setFavourite),
    (r'^saying/setReply/$', setReply),
    (r'^sayingContent/(\d+)/$', sayingCotent),
    (r'^projects/demo/$', pkdemo),
    (r'^account/$', account),
    (r'^addAccount/$', addAccount),
    (r'^clearAccount/$', clearAccount),
    (r'^love/$', love),
)


#urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
if settings.DEBUG is False:
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
