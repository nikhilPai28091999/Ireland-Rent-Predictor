import pandas as pd
import re

df = pd.read_csv('data/rentals-data-withAmenities.csv')
df.columns = ['Sno', 'Title', 'Bed', 'Bath', 'Price',
              'Parking', 'Central Heating', 'Washing Machine',
              'Dryer', 'Dishwasher', 'Internet', 'Garden / Patio / Balcony',
              'Microwave', 'Gym', 'Pets Allowed']


###### Remove Bed and Bath from the row values ##########
df['Bed'] = df['Bed'].astype(str).str.extract(r'(\d+)').astype(float)
df['Bath'] = df['Bath'].astype(str).str.extract(r'(\d+)').astype(float)
###### Remove Bed and Bath from the row values ##########


########### Convert per month price to weekly #############
def extract_price(price_str):
    """Extract numeric price from string like '€2,000 per month'"""
    if pd.isna(price_str):
        return None
    # Remove currency symbols and commas, extract numbers
    price_match = re.search(r'[€$]?([\d,]+)', str(price_str))
    if price_match:
        return float(price_match.group(1).replace(',', ''))
    return None

def convert_to_weekly(price_str):
    """Convert monthly prices to weekly, leave weekly prices as is"""
    if pd.isna(price_str):
        return price_str
    
    price_str = str(price_str)
    price_value = extract_price(price_str)
    
    if price_value is None:
        return price_str
    
    # Check if it's per month and convert to per week
    if 'per month' in price_str.lower():
        weekly_price = price_value / 4  # Average weeks per month
        # Format back to string with currency
        currency = '€'
        return f"{currency}{weekly_price:,.0f}"
    
    # If it's already per week, return as is
    elif 'per week' in price_str.lower():
        return price_str.replace(" per week","")
    
    # If no time period specified, assume it's monthly and convert
    else:
        weekly_price = price_value / 4
        return f"€{weekly_price:,.0f}"


df['Price'] = df['Price'].apply(convert_to_weekly)
########### Convert per month price to weekly #############


############## Extract location and create Location column ###########
df['Location'] = df['Title'].str.split(',').str[-1].str.strip()

# Remove location from Title column (everything up to and including the last comma)
df['Title'] = df['Title'].str.rsplit(',', n=1).str[0]
############## Extract location and create Location column ###########

# ############ Convert Price to numeric(remove € sign) #############
df['Price'] = df['Price'].str.replace('€', '', regex=False)  # Remove euro symbol
df['Price'] = df['Price'].str.replace(',', '')               # Remove commas if present
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0).astype(int)
# ############ Convert Price to numeric(remove € sign) #############

############## Assume places where bed and bath are NA to be 1 #################
df['Bath'] = df['Bath'].fillna(1).astype(int)
df['Bed'] = df['Bed'].fillna(1).astype(int)
############## Assume places where bed and bath are NA to be 1 #################

###### Convert Categorical variables into numerical ones ##############
df["Location"] = df["Location"].astype(str)
df = pd.get_dummies(df, columns=["Location"], drop_first=True)
###### Convert Categorical variables into numerical ones ##############


df.to_csv('data/cleaned-data.csv')
# print(df['Parking'])




