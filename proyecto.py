import funciones

while True:
    print("1.Crear productos \n2.Crear mesas \n3.Crear clientes \n4.Facturacion \n5.Reporte de ventas \n0.Salir")
    opcio = input("elija opcion: ")

    if opcio == "1":
        funciones.crear_producto()

    elif opcio == "2":
        funciones.crear_mesa()

    elif opcio == "3":
        funciones.crear_cliente()

    elif opcio == "4":
        funciones.facturacion()

    elif opcio == "5":
        funciones.reporte_ventas()

    elif opcio == "0":
        break

    else:
        print("Opcion invalida")