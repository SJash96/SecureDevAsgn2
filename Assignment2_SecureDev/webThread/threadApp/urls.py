from django.conf.urls import url
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'threadApp'

urlpatterns = [
    url(r'^$', views.index_v, name='index'),
    url(r'^details/(?P<id>\d+)/$', views.details_v, name='details'),
    url(r'^signup/', views.signup_v, name='signup'),
    url(r'^login/', views.login_v, name='login'),
    url(r'^accounts/login/', views.login_v, name='login'),
    url(r'^logout/', views.logout_v, name='logout'),
    url(r'^profile/', views.profile_v, name='profile'),
    url(r'^updateProf/', views.updateProfile_v, name='updateProf'),
    url(r'^deleteProf/', views.deleteProfile_v, name='deleteProf'),
    url(r'^password_reset/$', PasswordResetView.as_view(
        #template_name='password_reset.html',
        #email_template_name='password_reset_email.html',
        #subject_template_name='password_reset_subject.txt'
    ), 
        name='password_reset'
        ),
    url(r'^password_reset_done/$', PasswordResetDoneView.as_view(
        #template_name='password_reset_done.html'
    ), 
        name='password_reset_done'
        ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(
        #template_name='password_reset_confirm.html'
    ), 
        name='password_reset_confirm'
        ),
    url(r'^password_reset_complete/$', PasswordResetCompleteView.as_view(
        #template_name='password_reset_complete.html'
    ), 
        name='password_reset_complete'
        ),
    url(r'^createThread/', views.insertThread_v, name='createThread'),
    url(r'^uploadThread/', views.uploadThread_v, name='uploadThread'),
    url(r'^usersThread/', views.usersThread_v, name='usersThread'),
    url(r'^threadEdit/(?P<id>\d+)/$', views.threadEdit_v, name='threadEdit'),
    url(r'^threadDelete/(?P<id>\d+)/$', views.threadDelete_v, name='threadDelete'),
    url(r'^threadDownload/(?P<id>\d+)/$', views.threadDownload_v, name='threadDownload'),
]