from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('chart', views.display_charts, name='chart'),
    path('filters', views.filter_options, name='filter_options'),
    path('ai', views.ai, name="ai"),
    path('predict', views.predict, name="predict"),
    path('annual/<int:year>/sales', views.get_annual_sales, name='annual_chart'),
    path('', views.index, name='index'),
    path('books/<int:question_id>/', views.detail, name='detail'),
    path('books/<int:question_id>/results/', views.results, name='results'),
    path('books/<int:question_id>/vote/', views.vote, name='vote'),
]