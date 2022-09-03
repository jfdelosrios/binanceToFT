# -*- coding: utf-8 -*-
"""Genera archivo csv legible para Forex Tester usando data de Binance."""

from pandas import DataFrame, to_datetime
from C_Simbolo import C_Simbolo
from os import makedirs
from datetime import datetime
from pytz import timezone
from requests.exceptions import ReadTimeout, ConnectTimeout
from binance.exceptions import BinanceAPIException


def parsearDataFrame(_simbolo:str, _df: DataFrame) -> DataFrame:
    """vuelve legible el dataFrame _df para para Forex Tester."""
    
    _df = _df.sort_values(by = 'Open time', ascending = True)
    
    _df['Open time'] = to_datetime(_df['Open time'], unit = 'ms', utc = True)
    
    _df['<DTYYYYMMDD>'] = _df['Open time'].dt.strftime('%Y%m%d')
    _df['<TIME>'] = _df['Open time'].dt.strftime('%H%M')
    _df['<TICKER>'] = _simbolo
    
    _df.rename(

            columns = {
                    'Open': '<OPEN>',
                    'High': '<HIGH>',
                    'Low': '<LOW>',
                    'Close': '<CLOSE>',
                    'Number of trades': '<VOL>'
                },

            inplace = True

        )

    _df = _df[[
            '<TICKER>', 
            '<DTYYYYMMDD>', 
            '<TIME>', 
            '<OPEN>', 
            '<HIGH>', 
            '<LOW>', 
            '<CLOSE>', 
            '<VOL>'
        ]]

    return _df


def generarArchivoCSV(
    _simbolo:str,
    _timeFrame:str,
    _pathTMP:str,
    _pathSalida:str,
    _cantVelas:int
) -> dict[list[str,str]]:
    """
        Genera archivo csv desde data de Binance. Donde:
        
            * _simbolo: Simbolo.

            * _timeFrame: TimeFrame del simbolo. ver constantes KLINE_INTERVAL

                https://python-binance.readthedocs.io/en/latest/constants.html

            * _pathTMP: ruta donde se guarda el archivo resultante.

            * _descargar: Descarga el dataFrame de binance en el directorio _pathTMP.
    """
    
    fecha_barraActual =  datetime.timestamp(datetime.now(tz = timezone('UTC'))) * 1000

    try:
        simbolo = C_Simbolo(simbolo = _simbolo)
    except (ReadTimeout, ConnectTimeout, BinanceAPIException) as error:
        return {'status': ['error', str(error)], 'out': DataFrame}

    dict_s = simbolo.leer_velas(
                _interval =_timeFrame,
                ini = int(fecha_barraActual),
                cantBarras = _cantVelas,
                espera = 0.1
            )

    if(dict_s['status'][0] == 'error'):
        return {'status': dict_s['status']}

    try:
        df = parsearDataFrame(_simbolo, dict_s['out'])
    except (KeyError, ValueError) as error:

        _salida = {
            'status': [
                    'error', 
                    '{}\\{}-{}.csv esta dañado. {}'.format(
                        _pathTMP, 
                        _simbolo, 
                        _timeFrame,  
                        str(error)
                        )
                ]
            }

        return _salida
    
    makedirs(_pathSalida, exist_ok = True)
    
    df.to_csv('{}\\{}.csv'.format(_pathSalida, _simbolo), index = False)
    
    return {'status': ['ok', '']}