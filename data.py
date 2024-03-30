import pandas as pd

conditions = ["confirmed", "deaths", "recovered"]

daily_df = pd.read_csv("data/daily_report.csv")

totals_df = (daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count"))
totals_df = totals_df.rename(columns={'index': "condition"})

countries_df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = countries_df.groupby("Country_Region").sum().sort_values(by="Confirmed", ascending=False).reset_index()

dropdown_options = df = countries_df.sort_values("Country_Region").reset_index()
dropdown_options = dropdown_options["Country_Region"]

print(daily_df.columns)


def make_country_df(country):
    def make_df(df, condition):
        print("Columns before dropping:", df.columns)  # Add this line to print columns before dropping
        # Drop unnecessary columns and rename the remaining columns
        df = df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1, errors='ignore')
        df_sum = df.sum().reset_index(name=condition)
        df_sum = df_sum.rename(columns={'index': 'date'})
        return df_sum

    final_df = None
    
    for condition in conditions:
        df = pd.read_csv(f"data/time_{condition}.csv")
        # Rename the columns to match the column names in daily_df
        df = df.rename(columns={'Country/Region': 'Country_Region', 'Lat': 'Lat', 'Long': 'Long_'})
        df = df.loc[df["Country_Region"] == country]
        condition_df = make_df(df, condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    
    return final_df

 

def make_global_df():
    def make_df(df, condition):
        print("Columns before dropping:", df.columns)  # Add this line to print columns before dropping
        # Drop unnecessary columns and rename the remaining columns
        df = df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1, errors='ignore')
        df_sum = df.sum().reset_index(name=condition)
        df_sum = df_sum.rename(columns={'index': 'date'})
        return df_sum

    final_df = None
    
    for condition in conditions:
        df = pd.read_csv(f"data/time_{condition}.csv")
        # Rename the columns to match the column names in daily_df
        df = df.rename(columns={'Country/Region': 'Country_Region', 'Lat': 'Lat', 'Long': 'Long_'})
        condition_df = make_df(df, condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    
    return final_df





