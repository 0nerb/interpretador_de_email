from django.shortcuts import render
from .forms import ArquivoForm
from .nlp_service import processar_email_completo
import PyPDF2
import io

def home(request):
    resultado = None
    
    if request.method == 'POST':
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_obj = request.FILES.get('arquivo')
            texto_direto = form.cleaned_data.get('texto_direto')
            texto_final = ""

            if arquivo_obj:
                if arquivo_obj.name.lower().endswith('.pdf'):
                    try:
                        pdf_reader = PyPDF2.PdfReader(arquivo_obj)
                        for page in pdf_reader.pages:
                            texto_final += page.extract_text() + "\n"
                    except Exception as e:
                        texto_final = "Erro ao ler PDF."
                else:
                    texto_final = arquivo_obj.read().decode('utf-8')
            
            elif texto_direto:
                texto_final = texto_direto

            if texto_final:
                resultado = processar_email_completo(texto_final)
    else:
        form = ArquivoForm()

    return render(request, 'home.html', {'form': form, 'resultado': resultado})