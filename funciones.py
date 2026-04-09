
import csv
import os
from datetime import datetime

PRODUCTOS_FILE = "productos.csv"
MESAS_FILE = "mesas.csv"
CLIENTES_FILE = "clientes.csv"
FACTURAS_FILE = "facturas.csv"


def escribir_con_header_si_no_existe(nombre_archivo, fieldnames, fila):
    archivo_existe = os.path.isfile(nombre_archivo)
    archivo_vacio = not archivo_existe or os.path.getsize(nombre_archivo) == 0

    with open(nombre_archivo, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if archivo_vacio:
            writer.writeheader()
        writer.writerow(fila)


def buscar_por_campo(nombre_archivo, campo, valor):
    with open(nombre_archivo, "r", newline="") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila[campo] == valor:
                return fila
    return None


def crear_producto():
    head = ["codigo", "nombre", "precio", "iva"]

    codigo = input("codigo: ")
    nombre = input("nombre: ")
    precio = input("precio: ")
    iva = input("iva: ")

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "iva": iva
    }

    escribir_con_header_si_no_existe(PRODUCTOS_FILE, head, producto)
    print("Producto guardado.")


def crear_mesa():
    headmesas = ["codigo", "nombre", "puestos"]

    codigo = input("codigo: ")
    nombre = input("nombre: ")
    puestos = input("puestos: ")

    mesa = {
        "codigo": codigo,
        "nombre": nombre,
        "puestos": puestos
    }

    escribir_con_header_si_no_existe(MESAS_FILE, headmesas, mesa)
    print("Mesa guardada.")


def crear_cliente():
    headcliente = ["identificacion", "nombre", "telefono", "email"]

    identi = input("identificacion: ")
    nombre = input("nombre: ")
    telefono = input("telefono: ")
    email = input("email: ")

    cliente = {
        "identificacion": identi,
        "nombre": nombre,
        "telefono": telefono,
        "email": email
    }

    escribir_con_header_si_no_existe(CLIENTES_FILE, headcliente, cliente)
    print("Cliente guardado.")


def facturacion():
    mesa_encontrada = None
    mesa_deseada = input("codigo mesa: ")
    mesa_encontrada = buscar_por_campo(MESAS_FILE, "codigo", mesa_deseada)

    if not mesa_encontrada:
        print("Mesa no encontrada")
        return

    cliente_deseado = input("id cliente: ")
    cliente_encontrado = buscar_por_campo(CLIENTES_FILE, "identificacion", cliente_deseado)

    if not cliente_encontrado:
        print("Cliente no encontrado")
        return

    items = []

    while True:
        codigo = input("codigo producto: ")
        producto_encontrado = buscar_por_campo(PRODUCTOS_FILE, "codigo", codigo)

        if not producto_encontrado:
            print("Producto no encontrado")
            continue

        cantidad = int(input("cantidad: "))
        precio = float(producto_encontrado["precio"])
        iva = float(producto_encontrado["iva"])
        subtotal = (precio + iva) * cantidad

        item = {
            "codigo": producto_encontrado["codigo"],
            "nombre": producto_encontrado["nombre"],
            "cantidad": cantidad,
            "precio": precio,
            "iva": iva,
            "subtotal": subtotal
        }

        items.append(item)

        decision = input("¿agregar otro producto? (s/n): ").lower()
        if decision == "n":
            break

    total = sum(item["subtotal"] for item in items)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("\n===== FACTURA =====")
    print("Fecha:", fecha)
    print("Mesa:", mesa_encontrada["nombre"])
    print("Cliente:", cliente_encontrado["nombre"])
    print("Identificación:", cliente_encontrado["identificacion"])
    print("Teléfono:", cliente_encontrado["telefono"])
    print("Email:", cliente_encontrado["email"])

    print("\nProductos:")
    print("codigo | nombre | cantidad | precio | iva | subtotal")
    print("--------------------------------------------------")
    for item in items:
        print(item["codigo"], "|", item["nombre"], "|", item["cantidad"], "|", item["precio"], "|", item["iva"], "|", item["subtotal"])

    print("\nTOTAL A PAGAR:", total)

    guardar = input("¿Desea guardar la factura? (s/n): ").lower()
    if guardar == "s":
        with open(FACTURAS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([fecha, mesa_encontrada["codigo"], mesa_encontrada["nombre"],
                             cliente_encontrado["identificacion"], cliente_encontrado["nombre"],
                             cliente_encontrado["telefono"], cliente_encontrado["email"], total])
            for item in items:
                writer.writerow([item["codigo"], item["nombre"], item["cantidad"], item["precio"], item["iva"], item["subtotal"]])
            writer.writerow([])

        print("Factura guardada.")


def reporte_ventas():
    resumen_mesas = {}

    try:
        with open(FACTURAS_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            filas = list(reader)
    except FileNotFoundError:
        print("No existe facturas.csv")
        return

    i = 0
    while i < len(filas):
        fila = filas[i]


        if fila and len(fila) == 8:
            fecha, _, mesa, _, cliente, _, _, total_str = fila
            total = float(total_str)

            items = []
            i += 1

            while i < len(filas) and filas[i]:
                item_fila = filas[i]

                if len(item_fila) == 6:
                    codigo, nombre, cantidad_str, precio_str, iva_str, subtotal_str = item_fila

                    cantidad = int(cantidad_str)
                    precio = float(precio_str)
                    iva = float(iva_str)
                    subtotal = float(subtotal_str)

                    items.append((cantidad, precio, iva, subtotal))

                i += 1

            total_productos = sum(c for c, _, _, _ in items)
            subtotal_bruto = sum(p * c for c, p, _, _ in items)
            subtotal_iva = sum(i * c for c, _, i, _ in items)

            if mesa not in resumen_mesas:
                resumen_mesas[mesa] = {
                    "total_productos": 0,
                    "subtotal_bruto": 0,
                    "subtotal_iva": 0,
                    "subtotal": 0
                }

            resumen_mesas[mesa]["total_productos"] += total_productos
            resumen_mesas[mesa]["subtotal_bruto"] += subtotal_bruto
            resumen_mesas[mesa]["subtotal_iva"] += subtotal_iva
            resumen_mesas[mesa]["subtotal"] += total

        else:
            i += 1


    print("\n===== REPORTE DE VENTAS GENERAL =====")
    print("Mesa | Productos | Bruto | IVA | Total")

    total_bruto = 0
    total_iva = 0
    total_general = 0

    for mesa, datos in resumen_mesas.items():
        print(mesa, "|", datos["total_productos"], "|", datos["subtotal_bruto"], "|", datos["subtotal_iva"], "|", datos["subtotal"])

        total_bruto += datos["subtotal_bruto"]
        total_iva += datos["subtotal_iva"]
        total_general += datos["subtotal"]

    print("TOTAL BRUTO:", total_bruto)
    print("TOTAL IVA:", total_iva)
    print("TOTAL:", total_general)