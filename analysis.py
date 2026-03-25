## first open folder which has csv file and then impor libraries
## to get ineractive mode use shift+enter
#3 to change between terminals and python shells... use exit() and python as as commands
import pandas as pd
#3 read that csv file
df=pd.read_csv("customer_shopping_behavior.csv")
## get first 5 rows
df.head()
df.info()
df.describe()
## check any null values
df.isnull().sum()
# check column names and change them into snake casing(lowercase and _)
df.columns
## we are changing the column names into snake casing
df.columns=df.columns.str.lower().str.replace(" ","_")
df.columns
df=df.rename(columns={"purchase_amount_(usd)":"purchase_amount"})
df.columns
## creating new columns(feature engineering)
#3 chaging age columns into 4 categories
labels =["young adult","adult","middle-age","senior"]
df["age_group"]=pd.qcut(df["age"],q=4,labels=labels)
df[["age","age_group"]].head(10)
## creating a column named purchase frequency days
frequency_mapping ={
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Annually':365,
    'Bi-Weekly':14,
    'Every 3 Months':90
}
df["purchase_frequency_days"]=df['frequency_of_purchases'].map(frequency_mapping)
df[["frequency_of_purchases","purchase_frequency_days"]]
## remove the columns that are no longer needed
df[['discount_applied','promo_code_used']].head(10)
(df['discount_applied']==df['promo_code_used']).all()
## so drop promo code used column
df.drop("promo_code_used",axis=1,inplace=True)
df.head()
## now we need to connect python file to sql
## here some codes we wrote in terminal
from sqlalchemy import create_engine

# Step 1: Connect to PostgreSQL
## here my password coontains @ so it creates an error soo we are replacing with encode value %40 to get betetr results
# Replace placeholders with your actual details
username = "postgres"
password = "17Nf1@0221"
host = "localhost"
port = "5432"
database = "Customer_Behaviour"

engine = create_engine(f"postgresql+psycopg2://{username}:{password.replace('@', '%40')}@{host}:{port}/{database}")
# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine,if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")