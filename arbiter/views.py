from django.shortcuts import render
from django.views import View


class TestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'test.html', {})


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ms_responsive.html', {})


class GatewayView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'gateway.html', {})
