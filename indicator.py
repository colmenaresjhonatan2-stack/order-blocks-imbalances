import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

class OrderBlockImbalanceIndicator:
    """
    Indicador de Order Blocks e Imbalances (Fair Value Gaps)
    para análisis de Smart Money en trading de oro y otros activos.
    """
    
    def __init__(self, sensitivity: float = 0.5):
        """
        Inicializa el indicador.
        
        Args:
            sensitivity: Sensibilidad para detectar imbalances (0.0-1.0)
                        Mayor valor = más restrictivo (menos señales)
        """
        self.sensitivity = sensitivity
        self.order_blocks = []
        self.imbalances = []
    
    def detect_imbalances(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detecta Fair Value Gaps (Imbalances) en los datos OHLC.
        
        Un imbalance se forma cuando hay un gap entre velas (sin precio en medio).
        
        Args:
            df: DataFrame con columnas ['open', 'high', 'low', 'close']
        
        Returns:
            DataFrame con columnas adicionales de imbalances
        """
        df = df.copy()
        df['imbalance'] = 0
        df['imbalance_top'] = np.nan
        df['imbalance_bottom'] = np.nan
        df['imbalance_type'] = ''  # 'bullish' o 'bearish'
        
        for i in range(2, len(df)):
            prev_high = df['high'].iloc[i-2]
            prev_low = df['low'].iloc[i-2]
            curr_low = df['low'].iloc[i-1]
            curr_high = df['high'].iloc[i-1]
            next_low = df['low'].iloc[i]
            next_high = df['high'].iloc[i]
            
            # Imbalance BEARISH: gap hacia abajo
            # Vela 1 cierra, Vela 2 abre por debajo (sin tocar)
            if prev_low > curr_high and next_low < curr_high:
                df.loc[i, 'imbalance'] = 1
                df.loc[i, 'imbalance_top'] = prev_low
                df.loc[i, 'imbalance_bottom'] = curr_high
                df.loc[i, 'imbalance_type'] = 'bearish'
            
            # Imbalance BULLISH: gap hacia arriba
            # Vela 1 cierra, Vela 2 abre por arriba (sin tocar)
            if prev_high < curr_low and next_high > curr_low:
                df.loc[i, 'imbalance'] = 1
                df.loc[i, 'imbalance_top'] = curr_low
                df.loc[i, 'imbalance_bottom'] = prev_high
                df.loc[i, 'imbalance_type'] = 'bullish'
        
        return df
    
    def detect_order_blocks(self, df: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
        """
        Detecta Order Blocks basados en zonas de acumulación/distribución.
        
        Un Order Block se forma después de un movimiento fuerte con volumen,
        típicamente antes de un cambio de dirección.
        
        Args:
            df: DataFrame con columnas ['open', 'high', 'low', 'close', 'volume']
            lookback: Período para calcular la acumulación
        
        Returns:
            DataFrame con columnas adicionales de Order Blocks
        """
        df = df.copy()
        
        if 'volume' not in df.columns:
            df['volume'] = 1  # Si no hay volumen, usar 1 por defecto
        
        df['ob'] = 0
        df['ob_top'] = np.nan
        df['ob_bottom'] = np.nan
        df['ob_type'] = ''  # 'bullish' o 'bearish'
        df['ob_strength'] = 0
        
        for i in range(lookback + 1, len(df)):
            # Obtener el rango de velas anteriores
            recent_closes = df['close'].iloc[i-lookback:i].values
            recent_highs = df['high'].iloc[i-lookback:i].values
            recent_lows = df['low'].iloc[i-lookback:i].values
            recent_volumes = df['volume'].iloc[i-lookback:i].values
            
            # Calcular acumulación (promedio ponderado por volumen)
            volume_weighted_price = np.average(recent_closes, weights=recent_volumes)
            avg_volume = np.mean(recent_volumes)
            
            current_price = df['close'].iloc[i]
            prev_price = df['close'].iloc[i-1]
            current_volume = df['volume'].iloc[i]
            
            # ORDER BLOCK BEARISH: Fuerte movimiento bajista
            if prev_price > volume_weighted_price and current_price < volume_weighted_price:
                if current_volume > avg_volume * 0.8:  # Volumen significativo
                    df.loc[i, 'ob'] = 1
                    df.loc[i, 'ob_type'] = 'bearish'
                    df.loc[i, 'ob_top'] = np.max(recent_highs)
                    df.loc[i, 'ob_bottom'] = np.min(recent_lows)
                    df.loc[i, 'ob_strength'] = (current_volume / avg_volume)
            
            # ORDER BLOCK BULLISH: Fuerte movimiento alcista
            if prev_price < volume_weighted_price and current_price > volume_weighted_price:
                if current_volume > avg_volume * 0.8:  # Volumen significativo
                    df.loc[i, 'ob'] = 1
                    df.loc[i, 'ob_type'] = 'bullish'
                    df.loc[i, 'ob_bottom'] = np.min(recent_lows)
                    df.loc[i, 'ob_top'] = np.max(recent_highs)
                    df.loc[i, 'ob_strength'] = (current_volume / avg_volume)
        
        return df
    
    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Análisis completo: detecta tanto Order Blocks como Imbalances.
        
        Args:
            df: DataFrame con columnas ['open', 'high', 'low', 'close', 'volume']
        
        Returns:
            DataFrame enriquecido con señales de trading
        """
        df = self.detect_imbalances(df)
        df = self.detect_order_blocks(df)
        
        # Crear señal de trading
        df['signal'] = 0
        df['signal_type'] = ''
        
        for i in range(1, len(df)):
            imbalance = df['imbalance'].iloc[i]
            ob = df['ob'].iloc[i]
            
            if imbalance == 1 and ob == 1:
                if df['imbalance_type'].iloc[i] == df['ob_type'].iloc[i]:
                    df.loc[i, 'signal'] = 1
                    df.loc[i, 'signal_type'] = f"STRONG_{df['imbalance_type'].iloc[i].upper()}"
            elif imbalance == 1:
                df.loc[i, 'signal'] = 0.5
                df.loc[i, 'signal_type'] = f"IMBALANCE_{df['imbalance_type'].iloc[i].upper()}"
            elif ob == 1:
                df.loc[i, 'signal'] = 0.5
                df.loc[i, 'signal_type'] = f"OB_{df['ob_type'].iloc[i].upper()}"
        
        return df
    
    def get_support_resistance(self, df: pd.DataFrame) -> Dict:
        """
        Obtiene los niveles de soporte y resistencia basados en
        Order Blocks e Imbalances activos.
        
        Returns:
            Dict con 'resistance' y 'support'
        """
        ob_bullish = df[df['ob_type'] == 'bullish'].copy()
        ob_bearish = df[df['ob_type'] == 'bearish'].copy()
        
        support_levels = []
        resistance_levels = []
        
        if len(ob_bullish) > 0:
            support_levels.append(ob_bullish['ob_bottom'].iloc[-1])
        
        if len(ob_bearish) > 0:
            resistance_levels.append(ob_bearish['ob_top'].iloc[-1])
        
        imbalance_bullish = df[df['imbalance_type'] == 'bullish'].copy()
        imbalance_bearish = df[df['imbalance_type'] == 'bearish'].copy()
        
        if len(imbalance_bullish) > 0:
            support_levels.append(imbalance_bullish['imbalance_bottom'].iloc[-1])
        
        if len(imbalance_bearish) > 0:
            resistance_levels.append(imbalance_bearish['imbalance_top'].iloc[-1])
        
        return {
            'support': sorted(support_levels, reverse=True)[:3] if support_levels else [],
            'resistance': sorted(resistance_levels)[:3] if resistance_levels else []
        }
