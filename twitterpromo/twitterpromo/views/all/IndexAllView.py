from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

__author__ = 'Daniel'

class IndexAllView(View):
    @staticmethod
    def index(request):
        return render(request, 'index/index.html')
