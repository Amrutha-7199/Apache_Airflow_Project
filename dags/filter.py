import pandas as pd

# country data starts with I letter
def filter_function():

    print("Applying filter condition to take counties which start with I letter")

    df=pd.read_csv("~/ip_file/countries_cleaned.csv")

    df = df[df['Country'].str.startswith("I")].reset_index(drop=True)

    df.to_csv("~/op_file/countries_filtered.csv")