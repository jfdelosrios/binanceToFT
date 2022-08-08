# -*- coding: utf-8 -*-
"""Genera archivo csv legible para Forex Tester usando data de Binance."""

from pandas import DataFrame
from C_Simbolo import C_Simbolo, leerDataFrameBinance
from requests.exceptions import ConnectionError
from binance.exceptions import BinanceAPIException
from os import makedirs


def parsearDataFrame(_simbolo:str, _df: DataFrame) -> DataFrame:
    """vuelve legible el dataFrame _df para para Forex Tester."""
    
    _df = _df.sort_values(by = 'Open time', ascending = True)
    
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
    _descargar:bool
) -> dict[list[str,str]]:
    """
        Genera archivo csv desde data de Binance. Donde:
        
            * _simbolo: Simbolo.

            * _timeFrame: TimeFrame del simbolo. ver constantes KLINE_INTERVAL

                https://python-binance.readthedocs.io/en/latest/constants.html

            * _pathTMP: ruta donde se guarda el archivo resultante.

            * _descargar: Descarga el dataFrame de binance en el directorio _pathTMP.
    """
    
    if(_descargar):

        try:

            simbolo = C_Simbolo(simbolo = _simbolo)

        except (ConnectionError, BinanceAPIException) as error:

            return {'status': ['error', str(error)]}

        dict_s = simbolo.descargarDataFrameBinance(
            _timeFrame, 
            _pathTMP
            )

        if(dict_s['status'][0] == 'error'):
            return {'status': dict_s['status']}

    dict_s = leerDataFrameBinance(
        '{}\\{}-{}.csv'.format(_pathTMP, _simbolo, _timeFrame)
        )

    if(dict_s['status'][0] == 'error'):
        return {'status': dict_s['status']}

    df = parsearDataFrame(
        _simbolo,

        dict_s['out'][[
            'Open time', 
            'Open', 
            'High', 
            'Low', 
            'Close', 
            'Number of trades'
            ]]

        )
    
    makedirs(_pathSalida, exist_ok = True)
    
    df.to_csv('{}\\{}.csv'.format(_pathSalida, _simbolo), index = False)
    
    return {'status': ['ok', '']}