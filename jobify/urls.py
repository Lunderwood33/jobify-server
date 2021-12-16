from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from jobifyapi.views import register_user, login_user
from rest_framework import routers
from jobifyapi.views.job_type import JobTypeView
from jobifyapi.views.job_listing import JobListingView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'jobtypes', JobTypeView, 'jobtype')
router.register(r'joblistings', JobListingView, 'joblisting')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
    
]
