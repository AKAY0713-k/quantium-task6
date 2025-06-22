import pandas as pd

df0=pd.read_csv("data/daily_sales_data_0.csv")
df1=pd.read_csv("data/daily_sales_data_1.csv")
df2=pd.read_csv("data/daily_sales_data_2.csv")

df=pd.concat([df0,df1,df2],ignore_index=True)

df = df[df['product'] == 'pink morsel']

df['price'] = df['price'].replace('[\$,]', '', regex=True)
df['price']=pd.to_numeric(df['price'])

df['sales'] = df.apply(lambda row: row['price'] * row['quantity'], axis=1)

df = df[['sales', 'date', 'region']]
df=df.sort_values(by='sales')

df.to_csv("format_sales1.csv",index=False)


