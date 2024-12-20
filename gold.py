import pandas as pd
import pymongo


class goldClass:
    def __init__(self, df):
        self.df = df
    def dropcolumns(self):
        columns_to_drop = ['DALYs', 'Prevalence Rate (%)', 'Incidence Rate (%)',
                           'Improvement in 5 Years (%)', 'Urbanization Rate (%)', 'Education Index']

        # Drop the columns
        df_cleaned = self.df.drop(columns=columns_to_drop)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["HealthStatistics"]

        # Collection name
        collection_name = "golddata"

        # Drop collection if it exists
        if collection_name in mydb.list_collection_names():
            mydb.drop_collection(collection_name)

        # Create or access the collection
        collection = mydb[collection_name]
        print(f"Collection '{collection_name}' is ready.")
        data_dict = df_cleaned.to_dict(orient="records")
        collection.insert_many(data_dict)
        cursor = collection.find()
        data = list(cursor)
        df_g= pd.DataFrame(data)
        print(df_g.shape)
        return df_g


