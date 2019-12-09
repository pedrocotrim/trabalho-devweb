from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Imagem, Text, Carro
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .forms import CarroForm, RemoveCarroForm, PesquisaCarroForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
  imagens = get_list_or_404(Imagem, pagina='index')
  html = get_list_or_404(Text, pagina='index')
  return render(request, 'carro/index.html', { 'imagens': imagens, 'text': html })

def somos(request):
  html = get_list_or_404(Text, pagina='somos')
  return render(request,'carro/somos.html', { 'text': html })

def fale(request):
  return render(request,'carro/fale.html')

def pesquisa_carro(request):
  form = PesquisaCarroForm()
  return render(request, 'carro/pesquisa_carro.html', {
    'form': form
  })

def lista_carro(request):
  form = PesquisaCarroForm(request.GET)
  if (form.is_valid()):
    busca_por = form.cleaned_data['busca_por']
    lista_de_carros = Carro.objects.filter(nome__icontains=busca_por).order_by('nome')

    paginator = Paginator(lista_de_carros, 5)
    pagina = request.GET.get('pagina')
    carros = paginator.get_page(pagina)

    lista_de_ids = []
    for carro in carros:
      lista_de_ids.append(carro.id)

    return render(request, 'carro/pesquisa_carro.html', {
        'form': form,
        'carros': carros,
        'lista_de_ids': lista_de_ids
    })

  else:
    raise ValueError('Ocorreu um erro inesperado ao tentar pesquisar um carro.')

@login_required
def cadastra_carro(request):
  if request.POST:
      carro_id = request.POST.get('carro_id')
      if carro_id:
          carro = get_object_or_404(Carro, pk=carro_id)
          carro_form = CarroForm(request.POST, instance=carro)
      else:
          carro_form = CarroForm(request.POST)

      if carro_form.is_valid():
          carro = carro_form.save()
          if carro_id:
              messages.add_message(request, messages.INFO, 'Carro alterado com sucesso!')
          else:
              messages.add_message(request, messages.INFO, 'Carro cadastrado com sucesso!')
          return redirect('carro:exibe_carro', id=carro.id)
      else:
          messages.add_message(request, messages.ERROR, 'Corrija o(s) erro(s) abaixo.')
  else:
      carro_form = CarroForm()
  return render(request, 'carro/cadastra_carro.html', {
      'form': carro_form
  })

def exibe_carro(request, id):
  carro = get_object_or_404(Carro, pk=id)
  form_remove_carro = RemoveCarroForm(initial={'carro_id': id})
  return render(request, 'carro/exibe_carro.html', {
      'carro': carro,
      'form_remove_carro': form_remove_carro
  })

def edita_carro(request, id):
  carro = get_object_or_404(Carro, pk=id)
  carro_form = CarroForm(instance=carro)
  carro_form.fields['carro_id'].initial = id

  return render(request, 'carro/cadastra_carro.html', {
      'form': carro_form
  })


def remove_carro(request):
  carro_id = request.POST.get('carro_id')
  carro = get_object_or_404(Carro, id=carro_id)
  carro.delete()
  messages.add_message(request, messages.INFO, 'Carro removido com sucesso.')
  return render(request, 'carro/exibe_carro.html', {'carro': carro})