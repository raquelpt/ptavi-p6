#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os

if len(sys.argv) != 4:
	print "Usage: python server.py IP port audio_file"
	raise SystemExit
	

IP = sys.argv[1]

FICHERO_AUDIO = sys.argv[3]	

# Puerto en el que escuchamos

PORT = int(sys.argv[2])

try: 
	audio = open (FICHERO_AUDIO, 'r')
except IOError:
	print "Audio file doesn't exist"
	raise SystemExit



# Damos permiso de ejecución a RTP
os.system("chmod +x mp32rtp")

class EchoHandler(SocketServer.DatagramRequestHandler):
	"""
   	Echo server class
  	"""

	def handle(self):
		
		self.wfile.write("Hemos recibido tu peticion")
		while 1:
		    # Leyendo línea a línea lo que nos envía el cliente
		    line = self.rfile.read()
		    print "El cliente nos manda " + line

		    # Si no hay más líneas salimos del bucle infinito
		    if not line:
		        break
			
			# Seleccionamos la respuesta correcta

			Metodo = line.split(" ")[0]
			if Metodo == "INVITE" or Metodo == "ACK" or Metodo == "BYE":
				if Metodo == "INVITE" and line.split(" ")[2] =='SIP/2.0\r\n\r\n':
					Answer = "SIP/2.0 100 Trying\r\n\r\n"
					Answer += "SIP/2.0 180 Ring\r\n\r\n"
					Answer += "SIP/2.0 200 OK\r\n\r\n"
			
				elif Metodo == "ACK":
					# Tratamiento ACK
					aEjecutar = "./mp32rtp -i 127.0.0.1 -p 23032 < " + FICHERO_AUDIO
					print "Vamos a ejecutar", aEjecutar
					os.system (aEjecutar)
				elif Metodo == "BYE":
					# Tratamiento BYE
					Answer = "SIP/2.0 200 OK\r\n\r\n"
				else:	
					Answer = "SIP/2.0 400 Bad Request"
			else:
				Answer = "SIP/2.0 405 Method Not Allowed"
		

			# Imprimimos la respuesta y la enviamos

			if  Metodo != "ACK":
				print "Enviamos:" + Answer
				self.wfile.write(Answer)

if __name__ == "__main__":


    # Creamos servidor de eco y escuchamos

    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Listening..."
    serv.serve_forever()
