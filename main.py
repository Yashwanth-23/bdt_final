# This is a sample Python script.
import pandas as pd
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pymongo

import pymongo

from ML import ML
from gold import goldClass
from silver import MyClass

def dataset():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["HealthStatistics"]
    print(myclient.list_database_names())
    mydb = myclient["HealthStatistics"]
    collection_name = "HealthData"
    if collection_name in mydb.list_collection_names():
        mydb.drop_collection(collection_name)
    collection = mydb["HealthData"]
    df = pd.read_csv(r"/Users/BigData/GlobalHealthStatistics.csv")
    df2=df.head(200000)
    data_dict = df2.to_dict(orient="records")
    collection.insert_many(data_dict)
    cursor = collection.find()
    data = list(cursor)
    df3 = pd.DataFrame(data)
    print(df3.head(5))
    print(df3.shape)
    return df3






# Press the green button in the gutter to run the script.
class Bronzedata:
    def __init__(self, df):
        self.df=df;

    def bronze_data(self):

        # Establish connection to MongoDB
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["HealthStatistics"]

        # Collection name
        collection_name = "bronzedata"

        # Drop collection if it exists
        if collection_name in mydb.list_collection_names():
            mydb.drop_collection(collection_name)

        # Create or access the collection
        collection = mydb[collection_name]
        print(f"Collection '{collection_name}' is ready.")
        data_dict = self.df.to_dict(orient="records")
        collection.insert_many(data_dict)
        cursor = collection.find()
        data = list(cursor)
        df_b = pd.DataFrame(data)
        print("Silver rows:")
        return df_b



if __name__ == '__main__':
    df3=dataset()
    bronze=Bronzedata(df3)
    df_bronze=bronze.bronze_data()
    obj = MyClass(df_bronze)
    df_sil=obj.cleaning()
    gc=goldClass(df_sil)
    df_gold=gc.dropcolumns()
    ml=ML(df_gold)
    ml.Regression_Model()






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
