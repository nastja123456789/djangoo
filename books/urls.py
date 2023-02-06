from django.urls import path
from . import views
urlpatterns = [
    path('', views.display_charts, name='index'),
    path('filters', views.filter_options, name='filter_options'),
    path('annual/<int:year>/sales', views.get_annual_sales, name='annual_chart'),
]