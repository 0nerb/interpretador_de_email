from django.shortcuts import render
from .forms import DocumentoForm
# Atualize a importação
from .nlp_service import ler_arquivo, analisar_email_com_gemini 

def home(request):
    resultado_analise = None 

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
                # AQUI MUDOU: Chamamos a função nova do Gemini
                resultado_analise = analisar_email_com_gemini(texto_para_analise)
            
            return render(request, 'home.html', {
                'form': form, 
                'resultado': resultado_analise
            })

    else:
        form = DocumentoForm()
    
    return render(request, 'home.html', {'form': form})