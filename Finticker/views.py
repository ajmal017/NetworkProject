from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.db import connection

from graphos.renderers.yui import LineChart
from graphos.sources.simple import SimpleDataSource
from .models import *

# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)	

def show_graph(request):
  	cursor = connection.cursor()
  	cursor.execute("SELECT * FROM data")
  	data_list = cursor.fetchall()
  	data =  [['Data number', 'Value']]
  	for i in range(0, len(data_list)):
  		data.append([i, data_list[i][1]])
  	data_source = SimpleDataSource(data=data)
  	chart = LineChart(data_source)
  	context = {'chart': chart}
  	return render(request, 'graph.html', {'chart': chart})

  	