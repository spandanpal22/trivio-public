from django.urls import path
from django.conf.urls import url
from trivioapp import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    #url(r'^question/(?P<pk>\d+)/$', views.question, name='question'),
    url(r'^leaderboard/(?P<pk>\d+)/$', views.leaderboard,name='leaderboard'),
    #path('test', TemplateView.as_view(template_name='question.html'), name='test'),
    #path('test',views.test,name='test'),
    path('home/', views.home,name='home'),
    path('', views.question,name=''),
    path('profile/',views.profile,name='profile'),
    path('contact-us/',views.contact,name='contact'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('test/',views.test,name='test'),
    path('test2/',views.test2,name='test2'),
    #url(r'^(?P<string>[ \w\-]+)/$',views.question, name=''),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
