#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Comprobamos si es correcto el numero de argumentos pasados

if len(sys.argv) != 3:
	print "Usage: python client.py method receiver@IP:SIPport"
	raise SystemExit

# Cliente UDP simple.

lista = sys.argv
METODO = lista[1].upper()
Direccion = lista[2]

# Dirección IP del servidor.

SERVER = Direccion[1].split("@").split(":")[0]
PORT = int(Direccion.split("@")[1].split(":")[1])

# Contenido que vamos a enviar

LINE =  METODO + " sip:" + Direccion.split(":")[0] + " SIP/2.0\r\n\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))


print "Enviando: " + LINE
my_socket.send(LINE)
try:
	data = my_socket.recv(1024)
	except socket.error:
	print 'Error: No server listening at ' + SERVER + ' port ' + PORT
	raise SystemExit

print 'Recibido --', data
line = data.split('\r\n\r\n')[:-1]

if line == ["SIP/2.0 100 Trying", "SIP/2.0 180 Ring", "SIP/2.0 200 OK"]:
	LINE = "ACK sip:" + Direccion.split(":")[0] + " SIP/2.0\r\n\r\n"
	my_socket.send(LINE)
elif line == ["SIP/2.0 400 Bad Request"]:
	print "El servidor no entiende la petición"

elif line == ["SIP/2.0 405 Method Not Allowed"]:
	print "Enviado metodo incorrecto"

print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
