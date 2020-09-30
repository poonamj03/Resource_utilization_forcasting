# Import libraries
import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

# Defaults
plt.rcParams['figure.figsize'] = (20.0, 10.0)
plt.rcParams.update({'font.size': 12})
plt.style.use('ggplot')

data_cpu5 = pd.read_csv('/home/poonam/Downloads/future_predictions_on_grocessary store/group1_ID5_CPU_index.csv')#group1_ID2_time_combined_index.csv')#, engine='python', skipfooter=3)
data_cpu5.columns = ['timestamp','CPU_Used']

print('Ok')
data_cpu5['Month']=pd.to_datetime(data_cpu5['timestamp'], format='%Y-%m-%d')
#data_cpu5.set_index(['timestamp'], inplace=True)

data_cpu5_1 = data_cpu5.iloc[26000:]
data_cpu5_1.plot()

plt.hist(data_cpu5['CPU_Used'], bins = 100)#[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4] )

from statsmodels.tsa.stattools import adfuller
adfuller(data_cpu5_1['CPU_Used'])

def adfuller_test(CPU_Used):
    result=adfuller(CPU_Used)
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
    for value,label in zip(result,labels):
        print(label+' : '+str(value) )
    if result[1] <= 0.05:
        print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
    else:
        print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")


adfuller_test(data_cpu5_1['CPU_Used'])

data_cpu5_1['CPU_Used_dif'] = data_cpu5_1['CPU_Used']- data_cpu5_1['CPU_Used'].shift(6)
print(data_cpu5_1['CPU_Used_dif'].head(10))
print(data_cpu5_1['CPU_Used'].head(10))

adfuller_test(data_cpu5_1['CPU_Used_dif'].dropna())
data_cpu5_1['CPU_Used_dif'].plot()
#from pandas.tools.plotting import autocorrelation_plot
from pandas.plotting import autocorrelation_plot
autocorrelation_plot(data_cpu5_1['CPU_Used'])
plt.ylim([-0.1,0.1])
plt.show()


from statsmodels.tsa.arima_model import ARIMA
model=ARIMA(data_cpu5['CPU_Used'],order=(1,1,1))
model_fit=model.fit()
model_fit.summary()

data_cpu5_1['forecast']=model_fit.predict(dynamic=True)
data_cpu5_1[['CPU_Used','forecast']].plot(figsize=(12,8))


import statsmodels.api as sm

model=sm.tsa.statespace.SARIMAX(data_cpu5_1['CPU_Used'],order=(1, 1, 1),seasonal_order=(1,1,1,12))
results=model.fit()
data_cpu5_1['forecast']=results.predict(dynamic=True)
data_cpu5_1[['CPU_Used','forecast']].plot(figsize=(12,8))


### For future casting
from pandas.tseries.offsets import DateOffset
print(data_cpu5_1.index[-1])
print( DateOffset(months=x)for x in range(0,24))

future_dates=[data_cpu5_1.index[-1] + str(DateOffset(months=x)) for x in range(0,30)]
future_datest_df=pd.DataFrame(index=future_dates[1:],columns=data_cpu5_1.columns)
future_datest_df.tail()
future_df=pd.concat([data_cpu5_1,future_datest_df])
future_df['forecast'] = results.predict(dynamic= True)
future_df[['CPU_Used', 'forecast']].plot(figsize=(12, 8))
