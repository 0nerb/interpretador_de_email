from django import forms
import os

class ArquivoForm(forms.Form):
    arquivo = forms.FileField(required=False)
    texto_direto = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        arquivo = cleaned_data.get('arquivo')
        texto_direto = cleaned_data.get('texto_direto')

        if not arquivo and not texto_direto:
            raise forms.ValidationError("Por favor, envie um arquivo ou digite um texto.")
        return cleaned_data

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        
        if arquivo:
            ext = os.path.splitext(arquivo.name)[1].lower()
            valid_extensions = ['.pdf', '.txt']
            if ext not in valid_extensions:
                raise forms.ValidationError("Extensão não permitida. Use apenas .txt ou .pdf.")
            valid_mime_types = ['application/pdf', 'text/plain', 'application/octet-stream']
            if arquivo.content_type not in valid_mime_types:
                if arquivo.content_type != 'application/octet-stream':
                     pass

            if arquivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("O arquivo é muito grande. Máximo de 10MB.")
        
        return arquivo