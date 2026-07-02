import pandas as pd
import numpy as np
from indicator import OrderBlockImbalanceIndicator
import yfinance as yf

# Descargar datos de oro (XAUUSD)
print("Descargando datos de oro...")
gold = yf.download('GC=F', start='2024-01-01', end='2024-12-31', interval='1h')
gold = gold.reset_index()
gold.columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume']

# Inicializar el indicador
indicator = OrderBlockImbalanceIndicator(sensitivity=0.5)

# Analizar los datos
print("Analizando Order Blocks e Imbalances...")
df_analyzed = indicator.analyze(gold)

# Mostrar últimas 10 velas con señales
print("\n=== ÚLTIMAS 10 VELAS ===")
cols_display = ['datetime', 'close', 'volume', 'ob_type', 'imbalance_type', 'signal', 'signal_type']
print(df_analyzed[cols_display].tail(10).to_string())

# Obtener niveles de soporte y resistencia
levels = indicator.get_support_resistance(df_analyzed)
print(f"\n=== NIVELES CLAVE ===")
print(f"Soporte: {levels['support']}")
print(f"Resistencia: {levels['resistance']}")

# Contar señales
bullish_signals = len(df_analyzed[df_analyzed['signal_type'].str.contains('BULLISH', na=False)])
bearish_signals = len(df_analyzed[df_analyzed['signal_type'].str.contains('BEARISH', na=False)])

print(f"\n=== ESTADÍSTICAS ===")
print(f"Señales Alcistas: {bullish_signals}")
print(f"Señales Bajistas: {bearish_signals}")
print(f"Order Blocks Detectados: {len(df_analyzed[df_analyzed['ob'] == 1])}")
print(f"Imbalances Detectados: {len(df_analyzed[df_analyzed['imbalance'] == 1])}")

# Guardar resultados
df_analyzed.to_csv('gold_analysis.csv', index=False)
print("\n✅ Análisis guardado en 'gold_analysis.csv'")
