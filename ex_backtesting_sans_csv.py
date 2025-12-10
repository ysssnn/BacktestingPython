import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = {
    'date' : ['2025-02-01','2025-02-02','2025-02-03','2025-02-04','2025-02-05','2025-02-06','2025-02-07','2025-02-08','2025-02-09','2025-02-10'],
    'prix' : [50 ,52, 49,51,53,54,52,55,56,54]
}
df = pd.DataFrame(data)

df['rendement_j'] = df['prix'].pct_change()

df['rendement_3j'] = (1 + df['rendement_j']).rolling(window=3).apply(np.prod, raw=True) - 1

df['signal'] = np.where(df['prix'] < df['prix'].shift(1),0,1)

df['MA_3J'] = df['prix'].rolling(window=3).mean()
df['MA_3J_plot'] = df['MA_3J'].fillna(method='backfill')

df['achat'] = df['signal'].map({ 1:'oui' , 0:'non'})

df['vente'] = df['signal'].map({0:'oui' , 1:'non'})

df["Position"]= 0
df.loc [df["signal"] == 1 , "Position"] = 1
df.loc [df["signal"] == 0 , "Position"] = 0

capital_initial = 45

df ["PnL"] = df["Position"].shift(1) * (df["prix"].diff())

df['capital'] = capital_initial + df['PnL'].cumsum()

print (df)

plt.figure(figsize=(12,5))
plt.plot(df['date'], df['prix'], label='Prix')
plt.plot(df['date'], df['capital'], label='Capital')
plt.plot(df['date'], df['MA_3J_plot'], label='Moyenne Mobile')
plt.title("Graphique du Prix et du Capital")
plt.xlabel("date")
plt.ylabel("valeur")
plt.legend()
plt.grid(True)
plt.show()
