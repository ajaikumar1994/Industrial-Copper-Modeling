import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from operator import index
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
import streamlit_calendar as calendar

def price_predection(coun,stat,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,itm_dt_d,itm_dt_m,itm_dt_y,del_dt_d,del_dt_m,del_dt_y):

  item_date_d=int(itm_dt_d)
  item_date_m=int(itm_dt_m)
  item_date_y=int(itm_dt_y)

  delivery_date_d=int(del_dt_d)
  delivery_date_m=int(del_dt_m)
  delivery_date_y=int(del_dt_y)

  user_data_r=np.array([[coun,stat,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,item_date_d,item_date_m,item_date_y,delivery_date_d,delivery_date_m,delivery_date_y]])

  model_r=pickle.load(open('/content/regression_model.pkl','rb'))

  y_pred=model_r.predict(user_data_r)

  price=np.exp(y_pred[0])

  return price


def status_predection(coun,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,slp_log,itm_dt_d,itm_dt_m,itm_dt_y,del_dt_d,del_dt_m,del_dt_y):

  item_date_d=int(itm_dt_d)
  item_date_m=int(itm_dt_m)
  item_date_y=int(itm_dt_y)

  delivery_date_d=int(del_dt_d)
  delivery_date_m=int(del_dt_m)
  delivery_date_y=int(del_dt_y)

  user_data=np.array([[coun,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,slp_log,item_date_d,item_date_m,item_date_y,delivery_date_d,delivery_date_m,delivery_date_y]])

  model_c=pickle.load(open('/content/classification_model.pkl','rb'))

  y_pred=model_c.predict(user_data)

  if y_pred==1:
    return "Won"
  else:
    return "Lose"





st.set_page_config(layout="wide")
st.title(":blue[**INDUSTRIAL COPPER MODELING**]")
st.image("/content/a-beginners-guide-to-trading-gold-online.png")



tab1,tab2=st.tabs(["PRICE PREDECTION","STATUS PREDECTION"])
with tab1:
  st.subheader(":green[**PRICE PREDECTION**]")
  but=st.button("calender")
  if but:
    cal=calendar.calendar()

  col1,col2=st.columns(2)
  with col1:

    country_r= st.number_input(label="**COUNTRY**", min_value=25, max_value=113)
    status_r=st.number_input(label="**STATUS**",min_value=0,max_value=8)
    item_type_r= st.number_input(label="**ITEM TYPE**",min_value=0, max_value=6)
    application_r= st.number_input(label="**APPLICATION**",min_value=2.0, max_value=87.5)
    width_r= st.number_input(label="**WIDTH**",min_value=700.0, max_value=1980.0)
    product_ref_r= st.number_input(label="**PRODUCT_REF**",min_value=611728, max_value=1722207579)
    quantity_tons_log_r= st.number_input(label="**QUANTITY_TONS (Log Value)**",min_value=-0.3223343801166147, max_value=6.924734324081348,format="%0.15f")
    customer_log_r= st.number_input(label="**CUSTOMER (Log Value)**",min_value=17.21910565821408, max_value=17.230155364880137,format="%0.15f")


  with col2:



    thickness_log_r= st.number_input(label="**THICKNESS (Log Value)**",min_value= -1.7147984280919266, max_value=3.281543137578373,format="%0.15f")
    st.write("**ITEM DATE**")
    item_date_day_r= st.selectbox("**DAY**",("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"))
    item_date_month_r= st.selectbox("**MONTH**",("1","2","3","4","5","6","7","8","9","10","11","12"))
    item_date_year_r= st.selectbox("**YEAR**",("2020","2021"))
    st.write("**DELIVERY DATE**")
    delivery_date_day_r= st.selectbox("**DAY.**",("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"))
    delivery_date_month_r= st.selectbox("**MONTH.**",("1","2","3","4","5","6","7","8","9","10","11","12"))
    delivery_date_year_r= st.selectbox("**YEAR.**",("2020","2021","2022"))



  button= st.button(":violet[**PREDICT THE SELLING PRICE**]",use_container_width=True)
  if button:
    pre_price=price_predection(country_r,status_r,item_type_r,application_r,width_r,product_ref_r,quantity_tons_log_r,customer_log_r,thickness_log_r,item_date_day_r,item_date_month_r,item_date_year_r,delivery_date_day_r,
                     delivery_date_month_r,delivery_date_year_r)


    st.write("## :green[**The Selling Price is :**]",round(pre_price,2))


with tab2:
  st.subheader(":green[**STATUS PREDECTION**]")


  col1,col2=st.columns(2)
  with col1:

    country= st.number_input(label="**COUNTRY_**", min_value=25, max_value=113)
    item_type= st.number_input(label="**ITEM TYPE_**",min_value=0, max_value=6)
    application= st.number_input(label="**APPLICATION_**",min_value=2.0, max_value=87.5)
    width= st.number_input(label="**WIDTH_**",min_value=700.0, max_value=1980.0)
    product_ref= st.number_input(label="**PRODUCT_REF_**",min_value=611728, max_value=1722207579)
    quantity_tons_log= st.number_input(label="**QUANTITY_TONS_ (Log Value)_**",min_value=-0.3223343801166147, max_value=6.924734324081348,format="%0.15f")
    customer_log= st.number_input(label="**CUSTOMER (Log Value)_**",min_value=17.21910565821408, max_value=17.230155364880137,format="%0.15f")
    thickness_log= st.number_input(label="**THICKNESS (Log Value)_**",min_value= -1.7147984280919266, max_value=3.281543137578373,format="%0.15f")

  with col2:



    selling_price_log=st.number_input("**SELLING PRICE_**")
    st.write("**ITEM DATE_**")
    item_date_day= st.selectbox("**DAY_**",options=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"),key="delivery_date_day_c")
    item_date_month= st.selectbox("**MONTH_**",options=("1","2","3","4","5","6","7","8","9","10","11","12"),key="item_date_month_c")
    item_date_year= st.selectbox("**YEAR_**",options=("2020","2021"),key="item_date_year_c")
    st.write("**DELIVERY DATE_**")
    delivery_date_day= st.selectbox("**DAY_**",options=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"),key="delivery_date_day_classification")
    delivery_date_month= st.selectbox("**MONTH_**",options=("1","2","3","4","5","6","7","8","9","10","11","12"),key="delivery_date_month_c")
    delivery_date_year= st.selectbox("**YEAR_**",options=("2020","2021","2022"),key="delivery_date_year_c")



  button= st.button(":violet[**PREDICT THE STATUS(WON/LOSE)**]",use_container_width=True)
  if button:
    stat_pred=status_predection(country,item_type,application,width,product_ref,quantity_tons_log,customer_log,thickness_log,selling_price_log,item_date_day,item_date_month,item_date_year,delivery_date_day,
                     delivery_date_month,delivery_date_year)


    st.write("## :green[**The status is :**]",stat_pred)
