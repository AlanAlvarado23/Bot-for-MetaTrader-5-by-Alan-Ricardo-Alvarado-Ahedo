# -*- coding: utf-8 -*-
# Creado el viernes 19 de diciembre del 2021 a las 02:51:54 PM
# Autor: Alan Ricardo Alvarado Ahedo


from threading import Thread, enumerate
from time import sleep

from clases import operaciones # Archivo modular "clases.py"

def main ():
    
    while True:

        print(enumerate(), len(enumerate()))
        
        # Busca si hay menos de dos procesos, y si es así, se abre dos operaciones en paralelo
        if len(enumerate()) <= 1:

            operacion1 = operaciones()
            orden1, cierre1 = operacion1.iniciar()

            tarea1= Thread(target=operacion1.finalizar)
            tarea1.start()
            tarea1.join()

            # Cada ciclo se borra cada variable para reducir carga en memoria RAM
            del operacion1, orden1, cierre1, tarea1

        if len(enumerate()) <= 2:
            
            operacion2 = operaciones()
            orden2, cierre2 = operacion2.iniciar()
            tarea2= Thread(target=operacion2.finalizar)
            tarea2.start()
            
            # Cada ciclo se borra cada variable para reducir carga en memoria RAM
            del operacion2, orden2, cierre2, tarea2

        if len(enumerate()) > 1:
            sleep(30)
    
if __name__ == '__main__':
    main()