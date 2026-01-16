from django.shortcuts import render, redirect
from .forms import DocumentoForm

def home (request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            
            # AQUI: É onde você vai inserir sua lógica de processamento depois.
            # O arquivo está em: obj.arquivo.path
            # O texto está em: obj.texto_direto
            
            return render(request, 'sucesso.html')
    else:
        form = DocumentoForm()
    
    return render(request, 'home.html', {'form': form})

