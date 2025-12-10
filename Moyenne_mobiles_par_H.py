import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

def run_backtest():
    
    csv_file = Path(__file__).parent / "prix_dataa.csv"

    graph_folder = Path(__file__).parent /'Graph Backtest'
    

    df = pd.read_csv(csv_file, parse_dates=['datetime'])
    
    
    df['rendement'] = df['prix'].pct_change()
    
    
    df['ma_2h'] = df['prix'].rolling(window=2).mean()  
    df['ma_4h'] = df['prix'].rolling(window=4).mean()  
    
    
    df['signal'] = np.where(df['ma_2h'] > df['ma_4h'], 1, 0)
    df['position'] = df['signal'].shift(1)
    
    
    capital_initial = 50
    df['PnL'] = df['position'] * df['rendement'] * capital_initial
    df['capital'] = capital_initial + df['PnL'].cumsum()
    
    
    print(df)
    
    
    plt.figure(figsize=(14,7))
    plt.plot(df['datetime'], df['prix'], label='Prix', color='blue')
    plt.plot(df['datetime'], df['capital'], label='Capital', color='green')
    plt.plot(df['datetime'], df['ma_2h'], label='MA 2H', color='red', linestyle='--')
    plt.plot(df['datetime'], df['ma_4h'], label='MA 4H', color='orange', linestyle='--')
    plt.xlabel('Datetime')
    plt.ylabel('Valeur')
    plt.title('Backtest Moyennes Mobiles')
    plt.legend()
    plt.grid(True)
    
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    plot_file = graph_folder / f"backtest_plot_{timestamp}.png"
    plt.savefig(plot_file)
    plt.close()
    
    print(f"Graphique sauvegardé : {plot_file}")
