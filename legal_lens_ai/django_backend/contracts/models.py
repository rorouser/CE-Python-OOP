from django.conf import settings
from django.db import models
from django.urls import reverse


class Contract(models.Model):
    """Contrato subido por un abogado para auditar."""

    class Type(models.TextChoices):
        RENTAL = "RENTAL", "Alquiler"
        NDA = "NDA", "Confidencialidad (NDA)"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PROCESSING = "PROCESSING", "Procesando"
        CLEAN = "CLEAN", "Limpio"
        FLAGGED = "FLAGGED", "Banderas Rojas"
        ERROR = "ERROR", "Error"

    lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name="Abogado",
    )
    client_name = models.CharField("Cliente", max_length=200)
    contract_type = models.CharField(
        "Tipo", max_length=10, choices=Type.choices, default=Type.RENTAL
    )
    pdf_file = models.FileField("Archivo PDF", upload_to="contracts/%Y/%m/")
    uploaded_at = models.DateTimeField("Subido el", auto_now_add=True)
    status = models.CharField(
        "Estado", max_length=12, choices=Status.choices, default=Status.PENDING
    )

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def __str__(self):
        return f"{self.client_name} - {self.get_contract_type_display()}"

    def get_absolute_url(self):
        return reverse("contracts:detail", args=[self.pk])

    @property
    def is_clean(self) -> bool:
        return self.status == self.Status.CLEAN

    @property
    def is_flagged(self) -> bool:
        return self.status == self.Status.FLAGGED


class AuditReport(models.Model):
    """Resultado del análisis IA sobre un contrato."""

    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        related_name="report",
        verbose_name="Contrato",
    )
    extracted_text = models.TextField("Texto extraido del PDF", blank=True)
    key_data = models.JSONField(
        "Datos clave",
        default=dict,
        help_text="Firmantes, DNIs, fechas, importes, duracion, etc.",
    )
    red_flags = models.JSONField(
        "Banderas rojas",
        default=list,
        help_text="Lista de objetos {clausula, problema, articulo_legal, severidad}.",
    )
    summary = models.TextField("Resumen del informe", blank=True)
    processing_time_ms = models.PositiveIntegerField(
        "Tiempo de procesado (ms)", default=0
    )
    created_at = models.DateTimeField("Creado el", auto_now_add=True)

    class Meta:
        verbose_name = "Informe de Auditoria"
        verbose_name_plural = "Informes de Auditoria"

    def __str__(self):
        return f"Informe de {self.contract}"

    @property
    def num_red_flags(self) -> int:
        return len(self.red_flags or [])
