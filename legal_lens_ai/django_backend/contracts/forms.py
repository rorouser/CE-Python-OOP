from django import forms

from .models import Contract


class ContractUploadForm(forms.ModelForm):
    """Formulario para subir un nuevo contrato."""

    class Meta:
        model = Contract
        fields = ("client_name", "contract_type", "pdf_file")
        widgets = {
            "client_name": forms.TextInput(
                attrs={"placeholder": "Nombre del cliente"}
            ),
        }

    def clean_pdf_file(self):
        f = self.cleaned_data["pdf_file"]
        if not f.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Solo se aceptan archivos PDF.")
        if f.size > 10 * 1024 * 1024:
            raise forms.ValidationError("El archivo no puede superar los 10 MB.")
        return f
