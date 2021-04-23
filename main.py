from api import API_KEY
from etherscan_py import etherscan_py
from etherscan import Etherscan
import  matplotlib.pyplot as plt
es = Etherscan(API_KEY)
client = etherscan_py.Client(API_KEY)
eth_price = float(es.get_eth_last_price()["ethusd"])
from datetime import datetime
import pandas as pd
import math
from collections import Counter



gas = {}
value  = {}
gas_eth = {}
timestamp = {}
prior = {}
address_prior = {}
adress = {}
h={}
for k in [0,1,2]:
    failed = client.get_all_transactions(from_address="0x480d62d0db2842d78eef6e8e9ad62bf11c20a420",status=k,from_block=12290217)
    gas[k] = []
    value[k] = []
    timestamp[k] = []
    prior[k] = []
    address_prior[k] = []
    adress[k] = []
    h=[]
    for i in failed:
        gas[k].append((i.gas_used)*i.gas_price*10**(-9))
        value[k].append((i.value)*10**(-18))
        timestamp[k].append(i.timestamp)
        if 1619099939 <= i.timestamp < 1619100000:
            prior[k].append(i.value*10**(-18))
            address_prior[k].append(i.from_address)
        if i.value *10**(-18) > 0.37:
            h.append(i.value *10**(-18))

    gas_eth[k] = [j * 10**(-9) for j in gas[k]]
print(h[0])
print(address_prior[1])
prior_address = dict(Counter(address_prior[1]))
prior_address = {k: v for k, v in sorted(prior_address.items(), key=lambda item: item[1])}
print(prior_address)

print(len(prior[1]))
print(sum(prior[1])*2550)
fig, (ax,ax1, ax2) = plt.subplots(1, 3)
print(max(value[1]))
ax.hist2d(value[0],gas_eth[0],bins=(80,50),vmin = 0,vmax = 10)
ax.set_xlabel("IDO ETH value")
ax.set_xlim([0,0.5])
ax.set_ylim([0,2])
ax.set_ylabel("Gas used (Eth)")
ax.title.set_text('Failed tx')

ax1.hist2d(value[1],gas_eth[1],bins=30,vmin = 0,vmax = 4)
ax1.set_xlabel("IDO ETH value")
ax1.set_xlim([0,0.5])
ax1.set_ylim([0,2])
ax1.set_ylabel("Gas used (Eth)")
ax1.title.set_text('Completed tx')
ax2.hist2d(value[2],gas_eth[2],bins=(80,50),vmin = 0,vmax = 10)
ax2.set_xlabel("IDO ETH value ")
ax2.set_xlim([0,0.5])
ax2.set_ylim([0,2])
ax2.set_ylabel("Gas used (Eth)")
ax2.title.set_text('Both tx')



plt.show()


df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in timestamp.items() ]))
df.columns = ["Failed","Completed","Both"]
df["Count"] = 1

def time(t):
    return datetime.utcfromtimestamp(t).strftime('%H:%M:%S')

bin_value = 10

df_failed = df[["Failed","Count"]]
df_failed = df_failed[df_failed["Failed"].notna()]
df_failed["Failed"] = pd.cut(df_failed["Failed"],bins=math.floor(len(df_failed["Failed"])/bin_value))
df_failed["Failed"] = [math.floor(a.right) for a in df_failed["Failed"]]
df_failed = df_failed.groupby([df_failed["Failed"]]).sum().reset_index()
df_failed["Failed"] = df_failed["Failed"].map(time)


df_completed = df[["Completed","Count"]]
df_completed = df_completed[df_completed["Completed"].notna()]
df_completed = df_completed.groupby([df_completed["Completed"]]).sum().reset_index()
print(len(df_completed[df_completed["Completed"]<=1619100015])/len(df_completed["Completed"]))
df_completed["Completed"] = df_completed["Completed"].apply(time)


df_both = df[["Both","Count"]]
df_both = df_both[df_both["Both"].notna()]
df_both["Both"] = pd.cut(df_both["Both"],bins= math.floor(len(df_both["Both"])/bin_value))
df_both["Both"] = [a.right for a in df_both["Both"]]
df_both = df_both.groupby([df_both["Both"]]).sum().reset_index()
df_both["Both"] = df_both["Both"].map(time)

fig2,(x1,x2) = plt.subplots(2,1)

print(len(df_completed[df_completed["Completed"]<"14"]))
x1.plot(df_failed["Failed"],df_failed["Count"],label="Failed")
x1.set_xticks([df_failed["Failed"][o] for o in range(0,len(df_failed["Failed"]),2)])
x2.plot(df_completed["Completed"],df_completed["Count"],"k+-",label="Completed")
x2.set_xticks([df_completed["Completed"][r] for r in range(0,len(df_completed["Completed"]),2)])
x1.legend()
x2.legend()

x1.tick_params(labelrotation=45)
x2.tick_params(labelrotation=45)
plt.show()