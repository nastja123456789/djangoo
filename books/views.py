from django.db.models import Sum, F
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Purchase, Book, Choice
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.
from .utils import get_year_dict, months, generate_color_palette


def display_charts(request):
    return render(request, 'charts.html', {})


def ai(request):
    return render(request, 'ai.html')

import pandas as pd
import pickle
model = pickle.load(open('./model/breast_cancer.pkl', 'rb+'))

def predict(request):
    if request.method == 'POST':
        temp = {}
        temp['texture'] = float(request.POST.get('texture'))
        temp['radius'] = float(request.POST.get('radius'))
        temp['perimeter'] = float(request.POST.get('perimeter'))
        temp['smoothness'] = float(request.POST.get('smoothness'))
        temp['area'] = float(request.POST.get('area'))

        testdata = pd.DataFrame({'x': temp}).transpose()
        scoreval = model.predict(testdata)[0]
        if scoreval == 0:
            ans = "Benign"
        else:
            ans = "Malignant"
        return render(request, 'predict.html', {'result': ans})

def index(request):
    latest_question_list = Purchase.objects
    context = {
        'latest_question_list': latest_question_list.order_by('time_created')[:2],
    }
    return render(request, 'books/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Purchase, pk=question_id)
    return render(request, 'books/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Purchase, pk=question_id)

    return render(request, 'books/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Purchase, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'books/detail.html', {
            'question': question,
            'error_message': "Вы не сделали выбор."
        })
    else:
        selected_choice.votes += 1
        Purchase.objects.create(
            book=question.book,
            customer=question.customer,
            payment_method=question.payment_method,
            time_created=question.time_created,
            is_successful=question.is_successful
        )
        selected_choice.save()
        return HttpResponseRedirect(reverse('books:results', args=(question.id,)))


def filter_options(request):
    merged_purchases = Purchase.objects.annotate(
        year=ExtractYear(
            'time_created'
        )).values(
        'year'
    ).order_by(
        '-year'
    ).distinct()
    options = [purchase['year'] for purchase in merged_purchases]

    return JsonResponse(data={
        'options': options
    })


def get_annual_sales(request, year):
    purchases=Purchase.objects.filter(time_created__year=year)
    merged_purchases=purchases.annotate(
        price=F('book__price')
    ).annotate(month=ExtractMonth('time_created')).values(
        'month'
    ).annotate(
        average=Sum(
            'book__price'
        )
    ).values(
        'month',
        'average'
    ).order_by('month')
    sales_dict = get_year_dict()
    for merge in merged_purchases:
        sales_dict[months[merge['month']-1]]=round(merge['average'], 2)

    return JsonResponse({
        'title': f'Sales in {year}',
        'data': {
            'labels': list(sales_dict.keys()),
            'datasets': [{
                'label': 'Amount (KSHS)',
                'backgroundColor': generate_color_palette(7),
                'borderColor': generate_color_palette(5),
                'data': list(sales_dict.values())
            }]
        }
    })