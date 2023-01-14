import sys
from dateutil.parser import parse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_rows', 20)

# zad 1
p1 = pd.read_csv('Plant_1_Generation_Data.csv', parse_dates=["DATE_TIME"], dayfirst=False)
p2 = pd.read_csv('Plant_2_Generation_Data.csv', parse_dates=["DATE_TIME"], dayfirst=False)
df = pd.concat([p1, p2], ignore_index=True)

# zad 2
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True) # ??

# zad 3
generator1 = df.loc[
    (df['DATE_TIME'] >= '2020-05-17') & (df['DATE_TIME'] <= '2020-05-23') & (df['SOURCE_KEY'] == '1BY6WEcLGh8j5v7')]
generator1.set_index("DATE_TIME", inplace=True)
generator1.plot(y='AC_POWER', figsize=(15, 6))
plt.show()

# zad 4
generators = df.loc[
    (df['DATE_TIME'] >= '2020-05-17') & (df['DATE_TIME'] <= '2020-05-23')]  # DRY
generators.insert(0, 'mean', generators.groupby(['DATE_TIME'])['AC_POWER'].transform(np.mean))
generator1_merge = generator1.merge(generators, how='outer', on='DATE_TIME', sort=True)

generator1_merge.set_index("DATE_TIME", inplace=True)
generator1_merge[['AC_POWER_x', 'mean']].plot(figsize=(15, 6))
plt.show()

# zad 5
generators_lower = generators.loc[generators['AC_POWER'] < 0.8 * generators['mean']]
generators_lower = generators_lower.groupby('SOURCE_KEY')['SOURCE_KEY'].aggregate(np.count_nonzero).sort_values(
    ascending=False)
print(generators_lower)
print(generators_lower.index[:3])
