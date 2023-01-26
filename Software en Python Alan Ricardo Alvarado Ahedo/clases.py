# -*- coding: utf-8 -*-
# Creado el viernes 12 de noviembre del 2021 a las 11:28:11 PM
# Autor: Alan Ricardo Alvarado Ahedo

import sqlite3 as sql
import datetime as dt
import pytz
from time import sleep, time
import MetaTrader5 as mt5
import pandas as pd
import sqlite3 as sql

class operaciones:

    def __init__(self):

        # Se declaran las variables necesarias para iniciar sesión
        self.servidor = ""
        self.usuario = int("")
        self.contrasena = ""
        # El usuario, contraseña y servidor se eliminaron por privacidad

        for i in range(3):
            print("Iniciando sesion")
            if not mt5.initialize(server= self.servidor, login= self.usuario, password= self.contrasena):
                print("initialize() fallo: ", mt5.last_error())
                mt5.shutdown()
                print("Intentando de nuevo")
                
                if i == 3:
                    print("No fue posible conectar")
                    quit()
            else:
                break

        # Variable que indica si hay una operación abierta o cerrada
        self.estado_operacion = False

        # Se abre el archivo de "config.txt" de la carpeta resourses para aplicar los parámetros correspondientes
        datos_finales=[]
        datos = open("resourses/config.txt", 'r')
        lista = datos.readlines()
        for a in lista:
            datos_finales.append(int(a.replace("\n", "")))
        datos.close()

        # Se declaran las variables sobre el mercado para obtener datos y poder operar
        self.moneda = "Volatility 25 Index"
        self.lote = 0.5
        self.desviacion = 10
        self.puntos = mt5.symbol_info(self.moneda).point
        self.precio = mt5.symbol_info_tick(self.moneda).ask

        self.distanciaMinima = datos_finales[0]
        self.takeProfit = datos_finales[1]
        self.stopLoss = datos_finales[2]
        self.sl = 20000
        self.tp = 20000

    # Esta función retorna la fecha respecto a la zona horaria especificada
    def fecha (self):
    
        dia = (dt.datetime.now(pytz.timezone('Etc/GMT+0')).day)
        mes = dt.datetime.now(pytz.timezone('Etc/GMT+0')).month
        ano = dt.datetime.now(pytz.timezone('Etc/GMT+0')).year
        
        hora= (dt.datetime.now(pytz.timezone('Etc/GMT+0')).hour)
        
        minutos= dt.datetime.now(pytz.timezone('Etc/GMT+0')).minute
        
        return dt.datetime(ano, mes, dia, hora, minutos)

    """
    Escribe resultados de cada operación realizada con el bot en una base de datos de SQLite3
    Los datos almacenados son: 
    -  Fecha local de inicio y final de operación
    -  fecha del broker de inicio y final de operación
    -  el máximo y mínimo de las ganancias del resultado como el resultado final"""
    def escribirResultado (self, localFechaInicio, localFechaFinal, brokerFechaInicio, brokerFechaFinal, profitMinimo, profitMaximo, profit):
        format = "%Y-%m-%d %H:%M"
        
        base = sql.connect("Resourses/Activos/Volatility_25_index.db")

        base.execute("Insert into Operaciones(Fecha_Local_Inicio, Fecha_Local_Final, Fecha_Broker_Inicio, Fecha_Broker_Final, Profit_Minimo, Profit_Maximo, Profit_Final) values (?,?,?,?,?,?,?)", (localFechaInicio.strftime(format), localFechaFinal.strftime(format), brokerFechaInicio.strftime(format), brokerFechaFinal.strftime(format), profitMinimo, profitMaximo, profit))
        base.commit()
        base.close()

        print("\nGuardado correctamente")

    """
    Descompone los datos extraídos del mercado en 3 variables (todos convertidos a listas):
      -  Posiciones de los cierres de cada vela
      -  Crea un indicador de Media Movil Simple (Simple Moving Average)
      -  Crea un segundo indicador de Media Movil Exponencial (Exponential Moving Average"""
    def descomponer_mercado (self, mercado):
        return mercado['close'].tolist(), mercado['close'].rolling(window=20).mean().tolist(), mercado['close'].ewm(span = 5, adjust=False).mean().tolist()

    # Busca si la EMA cruzó la SMA de abajo hacia arriba o de arriba hacia abajo
    def buscar_cruce (self):

        # Se obitene la información del mercado elegido y a la fecha elegida
        mercado = pd.DataFrame(mt5.copy_rates_from(self.moneda, mt5.TIMEFRAME_M5, self.fecha(), 70))
        closeM5, SMA_M5_20, EMA_M5_5 = self.descomponer_mercado(mercado)
        
        # Se invierte para buscar lo más reciente que sucedió en el mercado
        SMA_M5_20_invertida = list(reversed(SMA_M5_20[-16:-2]))
        
        for i in SMA_M5_20_invertida:
            # Dirección hacia la baja (cruza de arriba a abajo)
            if i < EMA_M5_5[SMA_M5_20.index(i)] and SMA_M5_20[SMA_M5_20.index(i)+2] > EMA_M5_5[SMA_M5_20.index(i)+2]:
                return ["baja", SMA_M5_20[SMA_M5_20.index(i)+1], pd.to_datetime(mercado['time'][SMA_M5_20.index(i)+1], unit='s')]

            # Dirección hacia la alza (cruza de abajo a arriba)
            elif i > EMA_M5_5[SMA_M5_20.index(i)] and SMA_M5_20[SMA_M5_20.index(i)+2] < EMA_M5_5[SMA_M5_20.index(i)+2]:
                return ["alza", SMA_M5_20[SMA_M5_20.index(i)+1], pd.to_datetime(mercado['time'][SMA_M5_20.index(i)+1], unit='s')]

            # No hubo ningun curce
            else:
                return [False, None, None]

    def buscador (self):

        while not self.estado_operacion:
            self.cruce = [False]
            
            # Se busca si hubo un cruce
            print("Buscando cruce, estrategia: ", self.distanciaMinima, " - ", self.takeProfit, " - ", self.stopLoss)
            while self.cruce[0] == False:
                
                self.cruce = self.buscar_cruce()
                if self.cruce[0] == "baja" or self.cruce[0] == "alza":
                    break

                if self.cruce[0] == False:
                    sleep(10)
            
            tiempo1 = time()

            # Durante este while, se busca la separación de la distancia deseada, pero si vuelve a cruar en dirección contraria, se reinicia y cambia de dirección
            while (self.cruce[0] == "baja" and self.buscar_cruce()[0] != "alza") or (self.cruce[0] == "alza" and self.buscar_cruce()[0] != "baja"):

                mercado = pd.DataFrame(mt5.copy_rates_from(self.moneda, mt5.TIMEFRAME_M5, self.fecha(), 70))
                closeM5, SMA_M5_20, EMA_M5_5 = self.descomponer_mercado(mercado)

                # Esta variable es para poder hacer ciclos por minutos
                tiempo2= int(time()- tiempo1)

                if tiempo2 == 55:
                    print("\nNinguna desicion tomada, estrategia: ", self.distanciaMinima, " - ", self.takeProfit, " - ", self.stopLoss)
                    print(self.buscar_cruce()[0], self.cruce[0], self.cruce[1], " Distancia EMA: ", EMA_M5_5[-1] - self.cruce[1])
                    print(self.cruce[0], " == alza: ", self.cruce[0] == "alza", "  and  ", self.cruce[1]+self.distanciaMinima, " <= ", EMA_M5_5[-1], ": ", self.cruce[1]+self.distanciaMinima <= EMA_M5_5[-1])
                    print(self.cruce[0], " == baja: ", self.cruce[0] == "baja", "  and  ", self.cruce[1]-self.distanciaMinima, " >= ", EMA_M5_5[-1], ": ", self.cruce[1]-self.distanciaMinima >= EMA_M5_5[-1])

                
                # Meter operación al alza
                if self.cruce[0] == "alza" and (self.cruce[1]+self.distanciaMinima <= EMA_M5_5[-1]):
                    print("Operacion alza")
                    request = {"action": mt5.TRADE_ACTION_DEAL,
                        "symbol": self.moneda,
                        "volume": self.lote,
                        "type": mt5.ORDER_TYPE_BUY,
                        "price": self.precio,
                        "sl": self.precio - self.sl * self.puntos,
                        "tp": self.precio + self.tp * self.puntos,
                        "deviation": self.desviacion,
                        "comment": "Bot autonomo con POO",
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_FOK}
                    
                    self.cierre = mt5.ORDER_TYPE_SELL
                    
                    print("\aMeter operacion a la alza")
                    self.estado_operacion = True

                    self.orden = mt5.order_send(request)

                    print(mt5.last_error())
                    return self.orden, self.cierre, dt.datetime.now(), self.fecha()
                
                # Meter operación a la baja
                elif self.cruce[0] == "baja" and (self.cruce[1]-self.distanciaMinima >= EMA_M5_5[-1]):
                    print("Operacion baja")
                    self.precio=mt5.symbol_info_tick(self.moneda).bid
                    request = {"action": mt5.TRADE_ACTION_DEAL,
                        "symbol": self.moneda,
                        "volume": self.lote,
                        "type": mt5.ORDER_TYPE_SELL,
                        "price": self.precio,
                        "sl": self.precio + self.sl * self.puntos,
                        "tp": self.precio - self.tp * self.puntos,
                        "deviation": self.desviacion,
                        "comment": "Bot autonomo con POO",
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_FOK}
                    self.cierre = mt5.ORDER_TYPE_BUY
                    
                    print("\aMeter operacion a la baja")
                    self.estado_operacion = True

                    self.orden = mt5.order_send(request)

                    print(mt5.last_error())
                    return self.orden, self.cierre, dt.datetime.now(), self.fecha()
                
                else:
                    sleep(5)

                if tiempo2 == 60:
                    tiempo1 = time()

            print("\n\nReinicio de busqueda de cruce")

    # En este método se maneja y vigila la operación para cerrarla en caso de ganancia o pérdida deseada, guardando datos como:
    # Ganancia o pérdida máxima, resultado final, fecha de cierre de operación en hora bróker y local
    def manipulador_operacion (self, orden, cierre):
    
        self.estado_operacion = True

        # Esta variable sirve para hacer ciclos cada cierto tiempo deseado
        tiempo1 = time()
        
        # Aquí se guardan las variables de ganancia y pérdida máxima
        profitMinimo = 0
        profitMaximo = 0
        
        # Mientras el estado de la operación siga siendo cierto
        while self.estado_operacion:
            # Se obtiene la información de la operación abierta
            a=mt5.positions_get(ticket=self.orden.order)

            print("Profit:", a[0])
            print("Profit:", a)
            profit = a[0].profit
            print("Profit:", a[0])
            
            tiempo2= int(time()- tiempo1)
                
            if tiempo2 == 60:
                tiempo1= time()
            
            # En estas condicionales se guarda la ganancia y pérdida máxima
            if profit < profitMinimo: 
                profitMinimo = profit
            
            if profit > profitMaximo:
                profitMaximo = profit
            
            # Si se llegó a la pérdida o ganancia proporcionada por la estrategiam se cierra la operación
            if profit >= self.takeProfit or profit <= self.stopLoss:
                
                posicion_id= self.orden.order
                self.desviacion = 5
                self.puntos = mt5.symbol_info(self.moneda).point
                self.precio = mt5.symbol_info_tick(self.moneda).ask
                requestCerrar={"action": mt5.TRADE_ACTION_DEAL,
                    "symbol": self.moneda,
                    "volume": self.lote,
                    "type": self.cierre,
                    "position": posicion_id,
                    "price": self.precio,
                    "deviation": self.desviacion,
                    "comment": "Cierre Charles 5",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_FOK}
                
                self.orden = mt5.order_send(requestCerrar)
                self.estado_operacion= False
                
                # Operación cerrada

                break
            
            sleep(0.5)
            
        return profit, dt.datetime.now(), self.fecha(), profitMinimo, profitMaximo

    # En este método de la clase se inicia la búsqueda y análisis para obtener la dirección a la que se meterá la operación
    def iniciar (self):

        # Aquí se sincronizan los minutos y segundos para evitar delays o retrazos de la información obtenida del mercado y así que sea en tiempo real
        print("Sincronizando segundos: ", str(60-(dt.datetime.now().second)), "segundos. Segundo actual: ", str(dt.datetime.now().second))
        sleep(60-(dt.datetime.now().second))
        print("Sincronizando minutos")
        while True:
            if (dt.datetime.now().minute)%5 != 0:
                sleep(60)
            elif (dt.datetime.now().minute)%5 == 0 or dt.datetime.now().minute == 0:
                break
        print("Sincronizado")
        
        # Se manda a buscar la direccón de la operación y se ejecuta, recibiendo así la fecha de inicio local y en bróker para guardar en la base de datos
        self.orden, self.cierre, self.localFechaInicio, self.brokerFechaInicio = self.buscador()

        return self.orden, self.cierre

    # En este método se maneja la operación y la cierra automáticamente, y todos los datos obtenidos de la operación se guardan en la base de datos de dicho activo
    def finalizar (self):

        self.profit, self.localFechaFinal, self.brokerFechaFinal , self.profitMinimo, self.profitMaximo= self.manipulador_operacion(self.orden, self.cierre)
        print(self.localFechaInicio, self.localFechaFinal, self.brokerFechaInicio, self.brokerFechaFinal, self.profitMinimo, self.profitMaximo, self.profit)

        self.escribirResultado(self.localFechaInicio, self.localFechaFinal, self.brokerFechaInicio, self.brokerFechaFinal, self.profitMinimo, self.profitMaximo, self.profit)

        return self.localFechaInicio, self.localFechaFinal, self.brokerFechaInicio, self.brokerFechaFinal, self.profitMinimo, self.profitMaximo, self.profit

# Esta función crea un archivo "db" para SQLite3
def crearBaseActivo (nombreArchivo):

    conexion=sql.connect(str(nombreArchivo + ".db"))

    try:
        conexion.execute("""
            Create table Operaciones(
            Id integer primary key autoincrement,
            Fecha_Local_Inicio text,
            Fecha_Local_Final text,
            Fecha_Broker_Inicio text,
            Fecha_Broker_Final text,
            Profit_Minimo real,
            Profit_Maximo real,
            Profit_Final real)""")
        print("Se creo la tabla")

    except sql.OperationalError:
        print("La tabla ya fue creada anteriormente")
    conexion.close()