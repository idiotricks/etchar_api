from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from employees.views import EmployeeViewSet
from users.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
]

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'employees', EmployeeViewSet, basename='employee')
urlpatterns = router.urls

