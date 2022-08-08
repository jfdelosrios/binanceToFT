# -*- coding: utf-8 -*-
""""""

from principal import generarArchivoCSV
from binance.client import BaseClient
from varios import limpiarPantalla, pausar


def ejecutarPorConsola(correJupyter:bool) -> None:
    """
    Correr el programa en consola. Donde:
    
        * correJupyter: Define si esta corriendo en entorno Jupyter (o google colab).
    """

    _entrada:dict = leerTeclado()
    
    _pathSalida:str = '.\\salida'
    _pathTMP:str = '.\\tmp'
   
    dict_s:dict = generarArchivoCSV(
            _entrada['simbolo'],
            _entrada['timeFrame'],
            _pathTMP,
            _pathSalida,
            _entrada['descargar']
        )

    if(dict_s['status'][0] == 'error'):
        print('\n{}'.format(dict_s['status'][1]))

        if(not correJupyter):
            pausar()

        return
    
    print(

        '\n{}\\{}.csv quedo generado exitosamente.'.format(
                _pathSalida, 
                _entrada['simbolo']
            )

        )

    if(not correJupyter):
        pausar()


def leerTeclado() -> dict[str, str, str]:
    """Recoge datos del usuario por medio del teclado"""

    _salida:dict = {}

    _set_1 = set([
            BaseClient.KLINE_INTERVAL_1MINUTE,
            BaseClient.KLINE_INTERVAL_3MINUTE,
            BaseClient.KLINE_INTERVAL_5MINUTE,
            BaseClient.KLINE_INTERVAL_15MINUTE,
            BaseClient.KLINE_INTERVAL_30MINUTE,
            BaseClient.KLINE_INTERVAL_1HOUR,
            BaseClient.KLINE_INTERVAL_2HOUR,
            BaseClient.KLINE_INTERVAL_4HOUR,
            BaseClient.KLINE_INTERVAL_6HOUR,
            BaseClient.KLINE_INTERVAL_8HOUR,
            BaseClient.KLINE_INTERVAL_12HOUR,
            BaseClient.KLINE_INTERVAL_1DAY,
            BaseClient.KLINE_INTERVAL_3DAY,
            BaseClient.KLINE_INTERVAL_1WEEK,
            BaseClient.KLINE_INTERVAL_1MONTH,
        ])

    while True:

        limpiarPantalla()

        print('---- Binance To Forex Tester ------\n')
    
        _salida['simbolo']:str = input("simbolo: ")
        _salida['simbolo'] = _salida['simbolo'].upper()

        while True:

            _salida['timeFrame']:str = input(
                "Seleccione un timeFrame {}: ".format(_set_1)
                )
            
            if(_salida['timeFrame']  in _set_1):
                break

        while True:

            _salida['descargar']:str = input(
                "Desea descargar el archivo de Binance? (s/n): "
                )

            _salida['descargar'] = _salida['descargar'].lower()

            if(_salida['descargar'] == 's'):
                _salida['descargar'] = True
                break
                
            if(_salida['descargar'] == 'n'):
                _salida['descargar'] = False
                break

        while True:

            _confirmacion:str = input(
                "\nLa configuración seleccionada es:\n{}\n\nEstá correcta la configuración? (s/n): ".format(
                    _salida
                    )
                )

            _confirmacion =_confirmacion.lower()

            if(_confirmacion == 's'):
                return _salida
                
            if(_confirmacion == 'n'):
                break