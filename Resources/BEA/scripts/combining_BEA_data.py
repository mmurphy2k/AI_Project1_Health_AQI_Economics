# %%
import pandas as pd
import io
personal_income_df = pd.read_csv('./source/personal_income.csv')
gdp_df = pd.read_csv('./source/gdp.csv')
employment_df = pd.read_csv('./source/employment.csv')


# %%
def clean_and_melt_state_data(df):
    # Drop the 'GeoFips' column
    df = df.drop(columns=['GeoFips'])
    # Rename 'cols'
    df = df.rename(columns={'GeoName': 'State', 'year': 'Year'})
    # Remove the 'United States' row
    df = df[df['State'] != 'United States']
    # Melt the dataframe to create 'year' column
    df_melted = df.melt(id_vars=['State'], var_name='Year', value_name='value') 
    df_melted = df_melted[(df_melted['State'] == 'New York') | (df_melted['State'] == 'New Mexico') | (df_melted['State'] == 'Washington')]
    df_melted.set_index(['State', 'Year'], inplace=True)
    return df_melted


# %%
personal_income_long = clean_and_melt_state_data(personal_income_df).rename(columns={'value': 'personal_income'})
gdp_long = clean_and_melt_state_data(gdp_df).rename(columns={'value': 'GDP (in $)'})
employment_long = clean_and_melt_state_data(employment_df).rename(columns={'value': 'people_employed'})
print(personal_income_long.head())
print(gdp_long.head())
print(employment_long.head())


# %%
combined_economic_df = pd.concat([personal_income_long, gdp_long, employment_long], axis=1)
# Reset the index to make State and year regular columns
combined_economic_df = combined_economic_df.reset_index()
# Sort the DataFrame by State and year
combined_economic_df = combined_economic_df.sort_values(['State', 'Year'])

# Display the first few rows of the combined DataFrame
print(combined_economic_df.head())
# Save the combined economic data to a CSV file
combined_economic_df.to_csv('./resources/BEA/bea_annual.csv', index=False)