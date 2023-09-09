

from dbapp import Database
from gupy import Gupy
import pandas as pd

gupy=Gupy()


df_jobs=gupy.gupy_jobs()

df_app=pd.DataFrame()
df_steps=pd.DataFrame()

for _id in df_jobs.id:
    app=gupy.gupy_applications(_id)
    steps=gupy.gupy_steps(_id)
    df_app=pd.concat([df_app,app],ignore_index=True)
    df_steps=pd.concat([df_steps,steps],ignore_index=True)


database=Database()
database.connect()

database.dataframe_to_table(df_jobs,'Jobs')
database.dataframe_to_table(df_app,'Applications')
database.dataframe_to_table(df_steps,'Steps')



