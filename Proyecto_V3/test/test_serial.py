import serial
import time

puerto = 'COM6'  # Cambia al puerto correcto si no es COM6
baudrate = 115200

try:
    with serial.Serial(puerto, baudrate, timeout=1) as ser:
        print("Conectado a", puerto)
        time.sleep(2)  # Esperar a que el ESP32 reinicie
        while ser.in_waiting:
            print(ser.readline().decode().strip())  # Leer mensaje de inicio

        ser.write(b'Prueba desde Python\n')  # Enviar mensaje
        time.sleep(1)

        while ser.in_waiting:
            print("ESP32:", ser.readline().decode().strip())

except Exception as e:
    print("Error:", e)
