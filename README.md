# Order Blocks e Imbalances Indicator

Indicador de **Order Blocks** e **Imbalances (Fair Value Gaps)** para análisis de Smart Money en trading de oro y otros activos financieros.

## 📊 ¿Qué es esto?

Este indicador detecta automáticamente:

### **Order Blocks**
Zonas de acumulación/distribución donde el precio podría tener dificultad para pasar. Se forman después de movimientos fuertes con volumen significativo.

- **Order Block Bullish**: Zona de soporte potencial
- **Order Block Bearish**: Zona de resistencia potencial

### **Imbalances (Fair Value Gaps)**
Espacios vacíos donde no hay precio entre velas. Indican desequilibrio entre compradores y vendedores.

- **Imbalance Bullish**: Gap hacia arriba (potencial soporte)
- **Imbalance Bearish**: Gap hacia abajo (potencial resistencia)

## 🚀 Uso Rápido

```python
from indicator import OrderBlockImbalanceIndicator
import pandas as pd

# Crear indicador
indicator = OrderBlockImbalanceIndicator(sensitivity=0.5)

# Analizar datos OHLCV
df_analyzed = indicator.analyze(df)

# Obtener niveles de soporte y resistencia
levels = indicator.get_support_resistance(df_analyzed)
print(f"Soporte: {levels['support']}")
print(f"Resistencia: {levels['resistance']}")
```

## 📋 Columnas Generadas

| Columna | Descripción |
|---------|------------|
| `ob` | 1 si hay Order Block, 0 si no |
| `ob_type` | 'bullish' o 'bearish' |
| `ob_top` | Nivel superior del Order Block |
| `ob_bottom` | Nivel inferior del Order Block |
| `ob_strength` | Fuerza del Order Block (relación volumen) |
| `imbalance` | 1 si hay imbalance, 0 si no |
| `imbalance_type` | 'bullish' o 'bearish' |
| `imbalance_top` | Nivel superior del imbalance |
| `imbalance_bottom` | Nivel inferior del imbalance |
| `signal` | 1.0 (fuerte), 0.5 (débil), 0 (sin señal) |
| `signal_type` | Tipo de señal detectada |

## 🔧 Métodos Principales

### `detect_order_blocks(df, lookback=5)`
Detecta Order Blocks basados en volumen y acumulación.

```python
df = indicator.detect_order_blocks(df, lookback=5)
```

### `detect_imbalances(df)`
Detecta Fair Value Gaps en los datos.

```python
df = indicator.detect_imbalances(df)
```

### `analyze(df)`
Análisis completo combinando Order Blocks e Imbalances.

```python
df = indicator.analyze(df)
```

### `get_support_resistance(df)`
Obtiene los 3 principales niveles de soporte y resistencia.

```python
levels = indicator.get_support_resistance(df)
# {'support': [...], 'resistance': [...]}
```

## 📈 Ejemplo Completo

Ver `example_gold.py` para un ejemplo completo con datos de oro descargados de Yahoo Finance.

```bash
python example_gold.py
```

## 📦 Requisitos

```
pandas>=1.3.0
numpy>=1.21.0
yfinance>=0.1.70
```

Instala con:
```bash
pip install -r requirements.txt
```

## 💡 Estrategia de Trading

**Señal de COMPRA:**
- Precio toca imbalance bullish + Order Block bullish
- Confirmación: Volumen aumenta

**Señal de VENTA:**
- Precio toca imbalance bearish + Order Block bearish
- Confirmación: Volumen aumenta

## ⚙️ Parámetros Ajustables

```python
indicator = OrderBlockImbalanceIndicator(sensitivity=0.5)
# sensitivity: 0.0-1.0
#   - Menor valor: más señales (menos restrictivo)
#   - Mayor valor: menos señales (más restrictivo)
```

## 📝 Notas Importantes

- El indicador requiere datos OHLCV (Open, High, Low, Close, Volume)
- Se recomienda usar timeframes de 1h en adelante para oro
- Los Order Blocks más recientes son los más relevantes
- Combina con otros indicadores para mejorar precisión

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## ⚠️ Disclaimer

Este indicador es una herramienta de análisis técnico. **No es una recomendación de inversión**. Siempre realiza tu propia investigación y consulta con un asesor financiero antes de hacer trading.

## 📧 Soporte

Para reportar bugs o sugerencias, abre un issue en el repositorio.

---

**Creado para análisis de Smart Money en mercados financieros** 📊🚀
