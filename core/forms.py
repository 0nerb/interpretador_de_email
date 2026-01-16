from django import forms
from .models import Documento
import os

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['arquivo', 'texto_direto']
        labels = {
            'arquivo': 'Upload de Arquivo (.txt ou .pdf)',
            'texto_direto': 'Ou digite/cole o texto aqui',
        }
    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        
        if arquivo:
            # 1. Validação de Extensão (O nome do arquivo)
            ext = os.path.splitext(arquivo.name)[1].lower()
            valid_extensions = ['.pdf', '.txt']
            
            if ext not in valid_extensions:
                raise forms.ValidationError("Extensão não permitida. Use apenas .txt ou .pdf.")

            # 2. Validação de Content-Type (O tipo de conteúdo declarado pelo navegador)
            # application/pdf = PDF
            # text/plain = TXT
            valid_mime_types = ['application/pdf', 'text/plain']
            
            if arquivo.content_type not in valid_mime_types:
                raise forms.ValidationError("O arquivo enviado não é um PDF ou TXT válido.")
                
            # (Opcional) Validação de tamanho (ex: limitar a 5MB)
            if arquivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("O arquivo é muito grande. Máximo de 5MB.")

        return arquivo