from django.db import models
from django.core.validators import FileExtensionValidator

class Documento(models.Model):
    arquivo = models.FileField(
        upload_to='uploads/',
        validators=[FileExtensionValidator(allowed_extensions=['txt', 'pdf'])],
        blank=True, null=True
    )
    texto_direto = models.TextField(blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento {self.id}"
