"""DailySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from daily import views

urlpatterns = [
    # path函数将url映射到视图
    path('list/', views.list, name='list'),
    # 写日报
    path('create/', views.create, name='create'),
    # 导出所有日报
    path('excel_export/', views.excel_export, name='excel_export'),
    # 编辑日报
    path('edit/<int:id>/', views.edit, name='edit'),
    # 测试函数
    path('test/', views.test, name='test'),
]
