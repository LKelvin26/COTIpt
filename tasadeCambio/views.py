import hashlib
import hmac
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import querys
from django.http import JsonResponse
import json



@csrf_exempt
def wompi_webhook(request):
    if request.method == 'POST':
        try:
            # Validar el webhook
            if validar_webhook(request):
              webhook_data = json.loads(request.body)
              forma_pago = webhook_data["FormaPagoUtilizada"]
              identificador_enlace_comercio = webhook_data["EnlacePago"]["IdentificadorEnlaceComercio"]
              resultado_transaccion=webhook_data["ResultadoTransaccion"]

              # Imprimir los resultados
              print("Forma de pago:", forma_pago)
              print("Identificador de enlace de comercio:", identificador_enlace_comercio)
              print("resultado de la transaccion_",resultado_transaccion)
              
              if resultado_transaccion=="ExitosaAprobada":
                pago_exitoso(identificador_enlace_comercio)
              else:
                pago_denegado(identificador_enlace_comercio)
              # Procesar el webhook si la validación es exitosa
                # Aquí puedes continuar con el manejo del webhook
              return JsonResponse({'mensaje': 'Webhook válido y procesado correctamente'})
            else:
              # Si la validación falla, devolver un error 400
              return JsonResponse({'error': 'Webhook no válido'}, status=400)
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir durante la validación del webhook
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Método no permitido
        return JsonResponse({'error': 'Método no permitido'}, status=405)
  
def validar_webhook(request):
    # Leer el cuerpo completo del webhook
    body = request.body.decode('utf-8')

    # Obtener el valor del header "wompi_hash"
    wompi_hash_header = request.headers.get('wompi_hash')

    # Calcular el HMAC con SHA256 del cuerpo utilizando el API Secret de Wompi
    api_secret = 'TuApiSecretDeWompiAquí'
    hmac_calculado = hmac.new(api_secret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).hexdigest()

    # Comparar el HMAC calculado con el valor del header "wompi_hash"
    if hmac_calculado == wompi_hash_header:
        # El webhook es válido
        # Procesar el webhook según sea necesario
        datos_webhook = json.loads(body)
        # Aquí puedes realizar las acciones correspondientes con los datos del webhook
        return JsonResponse({'mensaje': 'Webhook válido'})
    else:
        # El webhook no es válido
        return JsonResponse({'error': 'Webhook no válido'}, status=400)
    

import mysql.connector
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="104.225.220.243",
            database="ventasonlinesalvador",
            user="sucursal",
            password="pdvr3P1iC@",
            autocommit=True,
            charset="utf8"
        )
        print("¡Conexión exitosa!")
        return conexion
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)
        return None
  
def pago_exitoso(id_pedido):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            # Query para actualizar los valores en la tabla hpedidos
            query = "UPDATE hpedidos SET IdStatusPedido = 1, IdStatusPedidoWompi = 1, StatusPedido = 'Asignado a sucursal' WHERE linkpedido = %s"
            # Ejecutar la consulta con el id del pedido proporcionado
            cursor.execute(query, (id_pedido,))
            print("Pedido actualizado correctamente.")
            # Cerrar cursor y conexión
            cursor.close()
            conexion.close()
        except mysql.connector.Error as error:
            print("Error al actualizar el pedido:", error)
    else:
        print("No se pudo establecer la conexión.")

def pago_denegado(id_pedido):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            # Query para actualizar los valores en la tabla hpedidos
            query = "UPDATE hpedidos SET IdStatusPedido = 6, IdStatusPedidoWompi = 2, StatusPedido = 'Validando Pago' WHERE linkpedido = %s"
            # Ejecutar la consulta con el id del pedido proporcionado
            cursor.execute(query, (id_pedido,))
            print("Pedido actualizado correctamente.")
            # Cerrar cursor y conexión
            cursor.close()
            conexion.close()
        except mysql.connector.Error as error:
            print("Error al actualizar el pedido:", error)
    else:
        print("No se pudo establecer la conexión.")