from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.display_charts, name='index'),
    path('filters', views.filter_options, name='filter_options'),
    path('annual/<int:year>/sales', views.get_annual_sales, name='annual_chart'),
    path('index', views.index, name='index'),
    path('books/<int:question_id>/', views.detail, name='detail'),
    path('books/<int:question_id>/results/', views.results, name='results'),
    path('books/<int:question_id>/vote/', views.vote, name='vote'),
]