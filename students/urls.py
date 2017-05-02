from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
# from accounts.views import (login_view, register_view, logout_view)

from accounts.views import UserLoginView, LogoutView, UserRegisterView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^login/', login_view, name='login'),
    url(r'^login/', UserLoginView.as_view(), name='login'),
    url(r'^register/', UserRegisterView.as_view(), name='register'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^', include('webapp.urls')),
]
