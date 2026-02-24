from django.contrib import admin
from django.urls import path,include
from app import views
from rest_framework.routers import DefaultRouter
from app.views import *

router = DefaultRouter()
router.register(r'employeerole', EmployeeRoleViewset)
router.register(r'employeeleave', EmployeeLeaveViewset)
router.register(r'employeesalary', EmployeeSalaryViewset)
router.register(r'employeeattandence', EmployeeAttandenceViewset)


urlpatterns = [
    path('', include(router.urls)),
    path("",views.index,name="index"),
    path("login_api",views.login_api,name="login_api"), 
    path("register",views.RegisterUser.as_view(),name="register"),
]
