from django import forms
from django.utils import timezone
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_cliente': forms.EmailInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'total_estimado': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrega = cleaned_data.get('fecha_entrega')
        modalidad = cleaned_data.get('modalidad')
        total_estimado = cleaned_data.get('total_estimado') or 0
        observaciones = cleaned_data.get('observaciones') or ""

        # 1. Validación de Fechas
        if fecha_entrega and fecha_entrega < timezone.now().date():
            self.add_error('fecha_entrega', 'La fecha de entrega no puede ser anterior a la fecha actual.')

        # 2. Restricción Despacho Express
        if modalidad == 'EXPRESS' and total_estimado < 15000:
            self.add_error('total_estimado', 'El monto para el Despacho Express debe ser de al menos $15.000 CLP.')

        # 3. Control de Productos Refrigerados / Bolsa térmica para PICKUP
        if modalidad == 'PICKUP' and 'bolsa termica' not in observaciones.lower() and 'bolsa térmica' not in observaciones.lower():
            self.add_error('observaciones', 'Para Retiro en Tienda con productos refrigerados debe indicar el uso de bolsa térmica en las observaciones.')

        return cleaned_data