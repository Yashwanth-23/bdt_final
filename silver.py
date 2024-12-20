# File: my_class.py
import pymongo
import pandas as pd

class MyClass:
    def __init__(self, df):
        self.df = df

    def cleaning(self):
        print(self.df.columns)
        print(self.df.dtypes)
        null_counts = self.df.isnull().sum()
        print("Null Values in Each Column:")
        print(null_counts)
        columns_with_nulls = null_counts[null_counts > 0]
        print("\nColumns with Null Values:")
        print(columns_with_nulls)
        expected_dtypes = {
            '_id': 'object',
            'Country': 'object',
            'Year': 'int64',
            'Disease Name': 'object',
            'Disease Category': 'object',
            'Prevalence Rate (%)': 'float64',
            'Incidence Rate (%)': 'float64',
            'Mortality Rate (%)': 'float64',
            'Age Group': 'object',
            'Gender': 'object',
            'Population Affected': 'int64',
            'Healthcare Access (%)': 'float64',
            'Doctors per 1000': 'float64',
            'Hospital Beds per 1000': 'float64',
            'Treatment Type': 'object',
            'Average Treatment Cost (USD)': 'int64',
            'Availability of Vaccines/Treatment': 'object',
            'Recovery Rate (%)': 'float64',
            'DALYs': 'int64',
            'Improvement in 5 Years (%)': 'float64',
            'Per Capita Income (USD)': 'int64',
            'Education Index': 'float64',
            'Urbanization Rate (%)': 'float64',
        }
        mismatched_columns = {
            column: (self.df[column].dtype, expected)
            for column, expected in expected_dtypes.items()
            if self.df[column].dtype != expected
        }

        if mismatched_columns:
            print("\nColumns with Data Type Mismatches:")
            for col, (actual, expected) in mismatched_columns.items():
                print(f"{col}: Expected {expected}, Found {actual}")
        else:
            print("\nNo Data Type Mismatches Found.")
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["HealthStatistics"]

        # Collection name
        collection_name = "silverdata"

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
        df_s= pd.DataFrame(data)
        print(df_s)
        return df_s

