import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_file = 'prix_dataa.csv'
df = pd.read_csv(csv_file, parse_dates=['datetime'])

df['rendement'] = df['prix'].pct_change()

df['ma_2h'] = df['prix'].rolling(window=2).mean()
df['ma_4h'] = df['prix'].rolling(window=4).mean()

df['signal'] = np.where(df['ma_2h'] > df['ma_4h'], 1, 0)

df['achat'] = df['signal'].map({1: 'oui', 0: 'non'})
df['vente'] = df['signal'].map({0: 'oui', 1: 'non'})

df['position'] = df['signal'].shift(1)

capital_initial = 50

df['PnL'] = df['position'] * df['rendement'] * capital_initial

df['capital'] = capital_initial + df['PnL'].cumsum()

print(df)

plt.figure(figsize=(14,7))
plt.plot(df['datetime'], df['prix'], label='Prix') 
plt.plot(df['datetime'], df['capital'], label='Capital')
plt.plot(df['datetime'], df['ma_2h'], label='Moyenne Mobile 2H')
plt.plot(df['datetime'], df['ma_4h'], label='Moyenne Mobile 4H')
plt.xlabel('Date')
plt.ylabel('Valeur')
plt.title('Trading Strategy Backtesting')
plt.legend()
plt.grid(True)
plt.savefig('capital.png')
plt.show()