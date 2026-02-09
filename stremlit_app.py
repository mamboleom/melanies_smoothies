import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    cnx = st.connection("snowflake")
    session = cnx.session()
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
    pd_df = my_dataframe.to_pandas()

    ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

    if ingredients_list:
        ingredients_string = ''

        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
            
            # Lookup the search value
            try:
                search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            except:
                search_on = fruit_chosen

            st.subheader(fruit_chosen + ' Nutrition Information')
            # Dynamic API call
            smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
            if smoothiefroot_response.status_code == 200:
                st.json(smoothiefroot_response.json())
            else:
                st.warning(f"No nutrition info found for {fruit_chosen}")

        my_insert_stmt = """insert into smoothies.public.orders (ingredients, name_on_order)
                    values ('""" + ingredients_string.strip() + """', '""" + name_on_order + """')"""

        time_to_insert = st.button('Submit Order')
        
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")



