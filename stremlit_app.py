# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Corrected indentation: this must align with the 'for' loop or the string initialization
    my_insert_stmt = """insert into smoothies.public.orders (ingredients, name_on_order)
                        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        # Corrected indentation: this must be inside the 'if time_to_insert' block
        st.success('Your Smoothie is ordered!', icon="✅")

