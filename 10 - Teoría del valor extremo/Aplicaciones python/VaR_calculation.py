
# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm 

abspath = 'C:/Users/tao24/OneDrive - University of Reading/PhD/'  
                   'QMF Book/book Ran/data files new/Book4e_data/'
data = pd.read_excel(abspath + 'sp500_daily.xlsx',index_col=[0])

def LogDiff(x):
    x_diff = np.log(x/x.shift(1))
    x_diff = x_diff.dropna()
    return x_diff

data['ret'] = LogDiff(data['Close'])
data = data.rename(columns={'Close':'sp500'})
data = data.dropna()

mean = np.mean(data['ret'])
std_dev = np.std(data['ret'])



# In[2]:


fig = plt.figure(1, dpi=600)
ax1 = fig.add_subplot(111)
ax1.hist(data['ret'],100,edgecolor='black',linewidth=1.2)
ax1.set_ylabel('density')

x = np.linspace(mean - 5*std_dev, mean + 5*std_dev, 100)
ax2 = ax1.twinx() 
ax2.plot(x,mlab.normpdf(x,mean,std_dev),"r")
ax2.set_ylabel('pdf of the normal distribution')
plt.legend()
plt.show()



# In[3]:


# normal distribution
VaR_90 = norm.ppf(1-0.9, mean, std_dev)
VaR_95 = norm.ppf(1-0.95, mean, std_dev)
VaR_99 = norm.ppf(1-0.99, mean, std_dev)

print('90%:{}'.format(VaR_90) )
print('95%:{}'.format(VaR_95) )
print('99%:{}'.format(VaR_99) )



# In[4]:


# historical distribution
VaR_90 = data['ret'].quantile(0.1)
VaR_95 = data['ret'].quantile(0.05)
VaR_99 = data['ret'].quantile(0.01)

print('90%:{}'.format(VaR_90) )
print('95%:{}'.format(VaR_95) )
print('99%:{}'.format(VaR_99) )



# In[5]:


threshold = -0.025
alpha = 0.01

data1 = data[data['ret']<=threshold]
data1 = data1.sort_values(['ret'])
data1['k'] = data1.iloc[0]['ret']

xi = (np.log(-data1['k']) - np.log(-data1['ret']) ).sum()*(1/(data1.shape[0]-1))
VaR_hill = data1['ret']*(data.shape[0]/data1.shape[0]*alpha)**(-xi)
VaR_hill = VaR_hill[1:]



# In[6]:


plt.figure(2, dpi=600)
x = [i for i in range(1,VaR_hill.shape[0]+1)]
plt.scatter(x,VaR_hill)
plt.xlabel('n')
plt.ylabel('VaR')
plt.show()



# In[7]:


import numpy as np
from scipy.optimize import minimize

alpha = 0.01
threshold = -0.025
y = threshold - data[data['ret']<=threshold]
y = y.sort_values(['ret'])
rets = y['ret'].values

shape = 0.2
scale = 1
x0 = (shape, scale)



# In[8]:


def fun(params,rets):
    F = lambda x: 1/params[1]*(1 + params[0] * x/params[1])**(-1 - 1/params[0])
    result = -sum([np.log(d) for d in [F(x) for x in rets] ])
    return result

result = minimize(fun, x0, args=rets, method='Nelder-Mead')
print (result) 



# In[9]:


shape = result.x[0]
scale = result.x[1]

VaR_mle = threshold + scale/shape*((data.shape[0]/y.shape[0]*alpha)**(shape)-1)
print('VaR_mle:{}'.format(VaR_mle) )

