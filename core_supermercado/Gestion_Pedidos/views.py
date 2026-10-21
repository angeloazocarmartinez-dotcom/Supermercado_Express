from django.shortcuts import render, redirect
from .models import Producto, Categoria, Pedido
from .forms import PedidoForm

def catalogo_productos(request):
    categoria_id = request.GET.get('categoria')
    refrigerado = request.GET.get('refrigerado')

    productos = Producto.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if refrigerado is not None and refrigerado != '':
        productos = productos.filter(requiere_refrigeracion=(refrigerado == '1'))

    categorias = Categoria.objects.all()
    return render(request, 'gestion_pedidos/catalogo.html', {
        'productos': productos,
        'categorias': categorias
    })

def registrar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogo_productos')
    else:
        form = PedidoForm()

    return render(request, 'gestion_pedidos/registro_pedido.html', {'form': form})


