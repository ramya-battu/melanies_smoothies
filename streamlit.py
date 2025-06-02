# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f"Cup With Straw : Customise your smoothie")
st.write(
  "choose the fruits you want"
)
import streamlit as st

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your smoothie will be ", name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_ID'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: '
    ,my_dataframe
)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string=ingredients_string+fruit_chosen+' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    st.write(my_insert_stmt)
   # st.stop()

    

    time_to_insert=st.button('Submit Order')

    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df=st.dataframe(data=smoothiefroot_response.json(), user_container_width=True)
