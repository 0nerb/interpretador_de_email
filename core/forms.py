from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['arquivo', 'texto_direto']
        labels = {
            'arquivo': 'Upload de Arquivo (.txt ou .pdf)',
            'texto_direto': 'Ou digite/cole o texto aqui',
        }