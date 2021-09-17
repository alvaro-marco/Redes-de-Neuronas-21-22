import pandas as pd
data = pd.read_csv('./concrete.dat2.csv', header=0)

#data["Cement"]=((data["Cement"]-data["Cement"].min())/(data["Cement"].max()-data["Cement"].min()))

dataf=((data-data.min())/(data.max()-data.min()))

data.sample(5)