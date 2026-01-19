from django.shortcuts import render
from .forms import DocumentoForm
from .nlp_service import ler_arquivo, processar_email_completo

def home(request):
    resultado_final = None 

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            
            texto_para_analise = ""
            if obj.arquivo:
                texto_para_analise = ler_arquivo(obj.arquivo.path)
            elif obj.texto_direto:
                texto_para_analise = obj.texto_direto
            
            if texto_para_analise:
                resultado_final = processar_email_completo(texto_para_analise)
            
            return render(request, 'home.html', {
                'form': form, 
                'resultado': resultado_final
            })

    else:
        form = DocumentoForm()
    
    return render(request, 'home.html', {'form': form})