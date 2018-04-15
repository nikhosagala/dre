from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy


@staff_member_required(login_url=reverse_lazy('admin:login'))
def dashboard(request):
    return render(request, 'employee/dashboard.html')
