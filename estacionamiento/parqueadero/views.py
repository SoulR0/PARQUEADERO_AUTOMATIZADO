from django.shortcuts import render, redirect
from .forms import RegistroEntradaForm
from django.utils import timezone
from .models import RegistroParqueo
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Asegúrate de tener home.html en tu carpeta de templates

def registrar_entrada(request):
    if request.method == 'POST':
        form = RegistroEntradaForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.hora_entrada = timezone.now()
            entrada.save()
            return redirect('lista_registros')  # o cualquier otra vista de tu sistema
    else:
        form = RegistroEntradaForm()
        return render(request, 'parqueo/registrar_entrada.html', {'form': form})
