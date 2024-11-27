# -*- coding: utf-8 -*-
"""copper_eda.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mnKAoAiQ8i9Rq9dNLReMPkpIeD352o9z

## industrial copper modeling
"""

#importing the nessary paccages
from datetime import datetime, timedelta
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df=pd.read_csv('/content/Copper_Set.xlsx - Result 1.csv')

df.head()

df.info()

#checking for null values
df.isnull().sum()

#checking for the unique values in each column and their data types
for i in df.columns:
  print(i,':',df[i].dtype)
  print(df[i].nunique())

#manupulating the data types

df['quantity tons']=pd.to_numeric(df['quantity tons'],errors='coerce')

df.dtypes

df['material_ref']=df['material_ref'].apply(lambda x:np.nan if str(x).startswith("00000") else x)

df['material_ref'].isnull().sum()/len(df['material_ref'])*100

#more thana 50 percentage is null so removing that column

df.drop('material_ref',axis=1,inplace=True)

df.info()

df.describe().T

# selling price and quantity tons have null values

df['quantity tons']=df['quantity tons'].apply(lambda x:np.nan if x<=0 else x)
df['selling_price']=df['selling_price'].apply(lambda x:np.nan if x<=0 else x)

df.isnull().sum()

df.dtypes

#Handleing the null values using mean(),median() and mode()
# object columns and mode method

df["status"].fillna(df["status"].mode().iloc[0],inplace=True)
df["item_date"]. fillna(df["item_date"].mode().iloc[0],inplace=True)
df["delivery date"]. fillna(df["delivery date"].mode().iloc[0],inplace=True)

#numarical column and median()

df["quantity tons"].fillna(df["quantity tons"].median(),inplace=True)
df["customer"].fillna(df["customer"].median(),inplace=True)
df["country"].fillna(df["country"].median(),inplace=True)
df["application"].fillna(df["application"].median(),inplace=True)
df["thickness"].fillna(df["thickness"].median(),inplace=True)
df["selling_price"].fillna(df["selling_price"].median(),inplace=True)

df.isnull().sum()

df.drop('id',axis=1,inplace=True)

df.info()

df["item_date_1"]= pd.to_datetime(df["item_date"],format="%Y%m%d",errors="coerce").dt.date
df["delivery_date_1"]= pd.to_datetime(df["delivery date"],format="%Y%m%d",errors="coerce").dt.date

df.info()

df["item_date_1"].fillna(df["item_date_1"].mode().iloc[0],inplace=True)
df["delivery_date_1"].fillna(df["delivery_date_1"].mode().iloc[0],inplace=True)

df.info()

"""# **Encoding the catagorical columns**"""

df['status'].unique()

df['status']=df['status'].map({'Won':1, 'Draft':2, 'To be approved':3, 'Lost':0, 'Not lost for AM':4,
       'Wonderful':5, 'Revised':6, 'Offered':7, 'Offerable':8})

df['status'].unique()

df.head()

df['item type']=OrdinalEncoder().fit_transform(df[['item type']])

df['item type']

"""# **Handling the skewness using (Log Transfermation)**"""

def plot(df,column):
  #distplot
  plt.figure(figsize=(15,4))
  plt.subplot(1,3,1)
  sns.distplot(df[column])
  plt.title("distplot for"+" "+column)

  #histogram plot

  plt.subplot(1,3,2)
  sns.histplot(df, x= column, kde= True, bins=30,color="salmon")
  plt.title("histogram plot for"+" "+column)

  #boxplot

  plt.subplot(1,3,3)
  sns.boxplot(df, x=column)
  plt.title("Box plot for"+" "+column)

skewed_columns=['quantity tons', 'customer', 'country', 'status',
                'item type', 'application', 'thickness', 'width', 'product_ref',
                'selling_price']

for i in skewed_columns:
  plot(df,i)

#Skewed columns:
# 1.quantity tons
# 2.customer
# 3.thickness
# 4.selling_price

df1= df.copy()

df1.columns

df1['quantity_tons_log']=np.log(df1['quantity tons'])
df1['customer_log']=np.log(df1['customer'])
df1['thickness_log']=np.log(df1['thickness'])
df1['selling_price_log']=np.log(df1['selling_price'])

skwed_columns_2=["quantity_tons_log","customer_log","thickness_log","selling_price_log"]
for i in skwed_columns_2:
  plot(df1,i)

"""# **checking for outliers**"""

#numerical columns
#'quantity_tons_log', 'customer_log', 'thickness_log','selling_price_log','width','application'

column=df1.columns

def out(df,column):
  plt.figure(figsize=(15,4))
  plt.subplot(1,3,1)
  sns.boxplot(df, x=column)
  plt.title("Box plot for"+" "+column)

for i in column:
  out(df1,i)

"""# **handling outliers using iqr**"""

def outlier(df,column):
  Q1=df[column].quantile(0.25)
  Q3=df[column].quantile(0.75)

  IQR=Q3-Q1

  lower_threshold=Q1-1.5*IQR
  upper_threshold=Q3+1.5*IQR

  df[column]= df[column].clip(lower_threshold, upper_threshold)

outlier_columns= ['quantity_tons_log', 'customer_log', 'thickness_log','selling_price_log','width','application']
for i in outlier_columns:
  outlier(df1,i)

df1.describe().T

for i in outlier_columns:
  plot(df1,i)

df1.columns

df1.drop(columns=["quantity tons","customer","thickness","selling_price"],axis=1,inplace=True)

df1.columns

df1.dtypes

#date handelling
df2=df1.copy()

#date correction

df2['item_date_1']=pd.to_datetime(df2['item_date_1'])
df2['delivery_date_1']=pd.to_datetime(df2['delivery_date_1'])

df2.dtypes

df2["date_dif"]=(df2['delivery_date_1']-df2['item_date_1']).dt.days

df2['item_date_day']=df2['item_date_1'].dt.day
df2['item_date_month']=df2['item_date_1'].dt.month
df2['item_date_year']=df2['item_date_1'].dt.year

df2.columns

# now we want to create the model for delivery date prediction
# importing the model
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor

df2_positive=df2[df2['date_dif']>=0]
df2_positive.reset_index(inplace=True,drop=True)

df2_negative=df2[df2['date_dif']<0]
df2_negative.reset_index(inplace=True,drop=True)

df2_positive.head()

df2_negative.head()

df2_positive['date_dif'].unique()

df2_negative['date_dif'].unique()

"""# **regresson model for date correction**

# **training with the positive values**
"""

def date(df,algorithm):

  x=df.drop(columns=['item_date_1', 'delivery_date_1','date_dif'])
  y=df['date_dif']

  x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

  model=algorithm().fit(x_train,y_train)

  y_pred=model.predict(x_test)

  #checking the accuracy score
  mse= mean_squared_error(y_test, y_pred)
  rmse= np.sqrt(mse)
  mae= mean_absolute_error(y_test,y_pred)
  r2= r2_score(y_test, y_pred)

  metrics={"algorithm":algorithm,
          "R2_score":r2,
          "Mean_squared_error":mse,
          "Root_mean_squared_error":rmse,
          "Mean_absolute_error":mae,
          }
  return metrics

print(date(df2_positive,DecisionTreeRegressor))
print(date(df2_positive,RandomForestRegressor))
print(date(df2_positive,AdaBoostRegressor))
print(date(df2_positive,ExtraTreesRegressor))
print(date(df2_positive,GradientBoostingRegressor))
print(date(df2_positive,XGBRegressor))

"""# **randomforest regressior is best**"""

def randomforest(train_df,test_df):

  X=train_df.drop(columns=['item_date_1','delivery_date_1','date_dif'])
  y=train_df['date_dif']

  x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

  model=RandomForestRegressor().fit(x_train,y_train)

  data=test_df.drop(columns=['item_date_1','delivery_date_1','date_dif'])

  y_pred=model.predict(data)

  return y_pred

date_diffrence = randomforest(df2_positive,df2_negative)

date_diffrence

len(date_diffrence)

#converting the datatype from flot to int

date_diffrence_1=[]
for i in date_diffrence:
  date_diffrence_1.append(int(round(i,0)))

len(date_diffrence_1)

df2.columns

df2_negative.columns

len(df2_negative)

df2_negative['date_diffrence']=pd.DataFrame(date_diffrence_1)

df2_negative['delivery_date_1']

df2_negative.columns

df2_negative.dtypes

df2_negative['delivery_date_1']=df2['item_date_1']+pd.to_timedelta(df2_negative['date_diffrence'],unit='D')

df2_negative['delivery_date_1']

# Concadinating the two dataframes(df4_pv,df4_nv) based on the rows
df_final=pd.concat([df2_positive,df2_negative],axis=0,ignore_index=True)

df_final.head()

df_final.tail()

df_final.info()

df_final['delivery_date_day']=df_final['delivery_date_1'].dt.day
df_final['delivery_date_month']=df_final['delivery_date_1'].dt.month
df_final['delivery_date_year']=df_final['delivery_date_1'].dt.year

df_final.drop(columns=['item_date_1','delivery_date_1','date_dif','item_date','delivery date','date_diffrence'],axis=1,inplace=True)

df_final.info()

# Saving the dataframe
df_final.to_csv("Industrial_Copper_Colab_final.csv",index= False)

"""# **classification for won/lose predection**"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#packages
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score,auc,roc_curve,confusion_matrix,classification_report

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from imblearn.combine import SMOTETomek
import pickle

df=pd.read_csv('/content/Industrial_Copper_Colab_final (1).csv')

df_class=df.copy()

df_class.info()

df_c=df_class[(df_class['status']==1)  | (df_class['status']==0)]

df_c.head()

df_c.info()

df_c['status'].unique()

df_c["status"].value_counts()

116012/150450*100

34438/150450*100

"""# **handeling the imbalenced data**"""

# s Oversampling is a technique that can help address this issue by increasing the number of samples from the underrepresented class.

x=df_c.drop(columns=['status'])
y=df_c['status']

X_new,Y_new=SMOTETomek().fit_resample(x,y)

x.shape,y.shape

X_new.shape,Y_new.shape

Y_new.value_counts()

"""# **finding the best algorithm for ml predection(classification)**"""

def classification(x_data,y_data,algorithm):

 x_train,x_test,y_train,y_test=train_test_split(x_data,y_data,test_size=0.2,random_state=42)

 model=algorithm().fit(x_train,y_train)

 y_pred_train=model.predict(x_train)

 y_pred_test=model.predict(x_test)

 #checking the accuracy score
 accuracy_train=accuracy_score(y_train,y_pred_train)
 accuracy_test=accuracy_score(y_test,y_pred_test)

 metrics={"algorithm":algorithm,
          "accuracy_train":accuracy_train,
          "accuracy_test":accuracy_test}

 return metrics

print(classification(X_new,Y_new,DecisionTreeClassifier))
print(classification(X_new,Y_new,RandomForestClassifier))
print(classification(X_new,Y_new,ExtraTreesClassifier))
print(classification(X_new,Y_new,AdaBoostClassifier))
print(classification(X_new,Y_new,GradientBoostingClassifier))
print(classification(X_new,Y_new,XGBClassifier))

"""# **Hyperparameter Tuning method with using of GridsearchCV**"""

# Get the high accuracy using Hyperparameter Tuning method with using of the GridsearchCV

x_train, x_test, y_train, y_test= train_test_split(X_new,Y_new, test_size= 0.2, random_state=42)

parameters= {"max_depth": [2,5],
              "min_samples_split": [2,5],
              "min_samples_leaf": [1,2],
              "max_features": ['sqrt', 'log2', None],

           }

gridsearch= GridSearchCV(estimator= RandomForestClassifier(), param_grid= parameters, cv= 5, n_jobs= -1)
gridsearch.fit(x_train,y_train)

gridsearch.best_score_

gridsearch.best_params_

"""
Passing the best Hypertuning paramers in the ,
RandomForest algorithm and check the accuracy for training and testing
"""

x_train, x_test, y_train, y_test= train_test_split(X_new, Y_new, test_size= 0.2, random_state= 42)

model= RandomForestClassifier(max_depth=20, max_features= None, min_samples_leaf=1, min_samples_split=2).fit(x_train,y_train)

y_pred_train= model.predict(x_train)
y_pred_test= model.predict(x_test)

#checking the accuracy_score for train and test

accuracy_train= accuracy_score(y_train, y_pred_train)
accuracy_test= accuracy_score(y_test, y_pred_test)

print("Accuracy score for Train and Test")
print("----------------------------------")
print("Accuracy_Train: ",accuracy_train)
print("Accuracy_Test: ",accuracy_test)
print("  ")
#confution matrics and the classification report for test

print("Confution_matrix for Test")
print("--------------------------")
print(confusion_matrix(y_true= y_test, y_pred= y_pred_test))
print(" ")
print("Classification_report for Test")
print("-------------------------------")
print(classification_report(y_true= y_test, y_pred= y_pred_test))

""" Receiver Operating Characteristic (ROC) Curve and Area Under the Curve (AUC)

"""

FP,TP,threshold= roc_curve(y_true=y_test, y_score=y_pred_test)

print(FP)
print(TP)

print(threshold)
print(" ")
auc_curve= auc(x=FP,y=TP)
print("auc_curve:",auc_curve)

""" create a plot for roc and auc curve"""

# create a plot for roc and auc curve
roc_point= {"ROC Curve (area)":round(auc_curve,2)}
plt.plot(FP,TP,label= roc_point)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.1])
plt.xlabel("False Positive")
plt.ylabel("True Positive")
plt.plot([0,1],[0,1],"k--")
plt.legend(loc= "lower right")
plt.show()

user_data1 = np.array([[77.0,3.0,10.0,1500.0,164141591,3.677655,17.222226,0.000000,7.110696,1,4,2021,1,8,2021]])

user_data = np.array([[30153963, 30, 6, 28, 952, 628377, 5.9, -0.96, 6.46, 1,4,2021,1,1,2021]])
y_pred_user= model.predict(user_data1)
if y_pred_user == 1:
    print("Won")
else:
    print("Lose")

with open("classification_model.pkl","wb") as f:
  pickle.dump(model,f)

with open("classification_model.pkl","rb") as f:
  model=pickle.load(f)

user_data = np.array([[77.0,3.0,10.0,1500.0,164141591,3.677655,17.222226,0.000000,7.110696,1,4,2021,1,8,2021]])
y_pred_user= model.predict(user_data)

if y_pred_user == 1:
    print("Won")
else:
    print("Lose")

"""# **regression model for price predection**"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor

df_price=df.copy()

df_price.info()

x=df_price.drop(columns=['selling_price_log'])
y=df_price['selling_price_log']

def accuracy_regressor(df,algorithm):
  x=df.drop(columns=['selling_price_log'])
  y=df['selling_price_log']

  x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

  model=algorithm().fit(x_train,y_train)

  y_pred_train=model.predict(x_train)
  y_pred_test=model.predict(x_test)

  r2_train=r2_score(y_train,y_pred_train)
  r2_test=r2_score(y_test,y_pred_test)

  metrics={"algorithm":algorithm,
           "r2_train":r2_train,
           "r2_test":r2_test}
  return metrics

print(accuracy_regressor(df, DecisionTreeRegressor))
print(accuracy_regressor(df, RandomForestRegressor))
print(accuracy_regressor(df, ExtraTreesRegressor))
print(accuracy_regressor(df, AdaBoostRegressor))
print(accuracy_regressor(df, GradientBoostingRegressor))
print(accuracy_regressor(df, XGBRegressor))

"""# **hypertuning for ramdomForest regressor model**"""

x= df.drop(columns=["selling_price_log"], axis=1)
y= df["selling_price_log"]

x_train, x_test, y_train, y_test= train_test_split(x,y, test_size= 0.2, random_state= 42)

parameters_r= {"max_depth": [2,4,10,20],
               "min_samples_split": [2,5,10],
               "min_samples_leaf": [1,2,4],
               "max_features": ["sqrt","log2",None]}

gridsearch_r= GridSearchCV(estimator= RandomForestRegressor(), param_grid= parameters_r, cv= 5,n_jobs=-1)
gridsearch_r.fit(x_train, y_train)

gridsearch_r.cv_results_

gridsearch_r.best_score_

gridsearch_r.best_params_

r_model= RandomForestRegressor(max_depth=20, max_features=None, min_samples_leaf=1, min_samples_split=2).fit(x_train,y_train)

y_pred_train= model.predict(x_train)
y_pred_test= model.predict(x_test)

#checking the accuracy_score for train and test

accuracy_train= accuracy_score(y_train, y_pred_train)
accuracy_test= accuracy_score(y_test, y_pred_test)

print("Accuracy score for Train and Test")
print("----------------------------------")
print("Accuracy_Train: ",accuracy_train)
print("Accuracy_Test: ",accuracy_test)

#predict the selling price with hypertuning parameters and calculate the accuracy using metrics

x = df.drop(columns=['selling_price_log'], axis=1)
y = df['selling_price_log']
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=42)

model_r = RandomForestRegressor(max_depth=20, max_features=None, min_samples_leaf=1, min_samples_split=2).fit(x_train, y_train)
y_pred = model_r.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

metrics_r = {'R2': r2,
           'Mean Absolute Error': mae,
           'Mean Squared Error': mse,
           'Root Mean Squared Error': rmse}

metrics_r

user_data = np.array([[30202938,25,1,5,41,1210,1668701718,6.6,-0.2,1,4,2021,1,4,2021]])
y_pred = model_r.predict(user_data)
print("Predicted selling price with Log: ",y_pred[0])
print("Predicted selling price without Log: ",np.exp(y_pred[0]))

import pickle

with open("regression_model.pkl","wb") as f:
  pickle.dump(model_r,f)

with open("regression_model.pkl","rb") as f:
  model_r=pickle.load(f)

user_data = np.array([[28.0,1,5.0,10.0,1500.0,1670798778,3.991779,17.221905,0.693147,1,4,2021,1,7,2021]])
y_pred = model_r.predict(user_data)
print("Predicted selling price with Log: ",y_pred[0])
print("Predicted selling price without Log: ",np.exp(y_pred[0]))

"""# ***streamlit part***"""

!pip install streamlit

!pip install streamlit_option_menu

!pip install streamlit-calendar

# Commented out IPython magic to ensure Python compatibility.
# 
# %%writefile copper_app_test.py
# import streamlit as st
# import pandas as pd
# import numpy as np
# from streamlit_option_menu import option_menu
# from operator import index
# import pickle
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
# import streamlit_calendar as calendar
# 
# def price_predection(coun,stat,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,itm_dt_d,itm_dt_m,itm_dt_y,del_dt_d,del_dt_m,del_dt_y):
# 
#   item_date_d=int(itm_dt_d)
#   item_date_m=int(itm_dt_m)
#   item_date_y=int(itm_dt_y)
# 
#   delivery_date_d=int(del_dt_d)
#   delivery_date_m=int(del_dt_m)
#   delivery_date_y=int(del_dt_y)
# 
#   user_data_r=np.array([[coun,stat,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,item_date_d,item_date_m,item_date_y,delivery_date_d,delivery_date_m,delivery_date_y]])
# 
#   model_r=pickle.load(open('/content/regression_model.pkl','rb'))
# 
#   y_pred=model_r.predict(user_data_r)
# 
#   price=np.exp(y_pred[0])
# 
#   return price
# 
# 
# def status_predection(coun,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,slp_log,itm_dt_d,itm_dt_m,itm_dt_y,del_dt_d,del_dt_m,del_dt_y):
# 
#   item_date_d=int(itm_dt_d)
#   item_date_m=int(itm_dt_m)
#   item_date_y=int(itm_dt_y)
# 
#   delivery_date_d=int(del_dt_d)
#   delivery_date_m=int(del_dt_m)
#   delivery_date_y=int(del_dt_y)
# 
#   user_data=np.array([[coun,item_typ,appl,wid,prod_ref,qnt_tns,cus,thck_log,slp_log,item_date_d,item_date_m,item_date_y,delivery_date_d,delivery_date_m,delivery_date_y]])
# 
#   model_c=pickle.load(open('/content/classification_model.pkl','rb'))
# 
#   y_pred=model_c.predict(user_data)
# 
#   if y_pred==1:
#     return "Won"
#   else:
#     return "Lose"
# 
# 
# 
# 
# 
# st.set_page_config(layout="wide")
# st.title(":blue[**INDUSTRIAL COPPER MODELING**]")
# st.image("/content/a-beginners-guide-to-trading-gold-online.png")
# 
# 
# 
# tab1,tab2=st.tabs(["PRICE PREDECTION","STATUS PREDECTION"])
# with tab1:
#   st.subheader(":green[**PRICE PREDECTION**]")
#   but=st.button("calender")
#   if but:
#     cal=calendar.calendar()
# 
#   col1,col2=st.columns(2)
#   with col1:
# 
#     country_r= st.number_input(label="**COUNTRY**", min_value=25, max_value=113)
#     status_r=st.number_input(label="**STATUS**",min_value=0,max_value=8)
#     item_type_r= st.number_input(label="**ITEM TYPE**",min_value=0, max_value=6)
#     application_r= st.number_input(label="**APPLICATION**",min_value=2.0, max_value=87.5)
#     width_r= st.number_input(label="**WIDTH**",min_value=700.0, max_value=1980.0)
#     product_ref_r= st.number_input(label="**PRODUCT_REF**",min_value=611728, max_value=1722207579)
#     quantity_tons_log_r= st.number_input(label="**QUANTITY_TONS (Log Value)**",min_value=-0.3223343801166147, max_value=6.924734324081348,format="%0.15f")
#     customer_log_r= st.number_input(label="**CUSTOMER (Log Value)**",min_value=17.21910565821408, max_value=17.230155364880137,format="%0.15f")
# 
# 
#   with col2:
# 
# 
# 
#     thickness_log_r= st.number_input(label="**THICKNESS (Log Value)**",min_value= -1.7147984280919266, max_value=3.281543137578373,format="%0.15f")
#     st.write("**ITEM DATE**")
#     item_date_day_r= st.selectbox("**DAY**",("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"))
#     item_date_month_r= st.selectbox("**MONTH**",("1","2","3","4","5","6","7","8","9","10","11","12"))
#     item_date_year_r= st.selectbox("**YEAR**",("2020","2021"))
#     st.write("**DELIVERY DATE**")
#     delivery_date_day_r= st.selectbox("**DAY.**",("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"))
#     delivery_date_month_r= st.selectbox("**MONTH.**",("1","2","3","4","5","6","7","8","9","10","11","12"))
#     delivery_date_year_r= st.selectbox("**YEAR.**",("2020","2021","2022"))
# 
# 
# 
#   button= st.button(":violet[**PREDICT THE SELLING PRICE**]",use_container_width=True)
#   if button:
#     pre_price=price_predection(country_r,status_r,item_type_r,application_r,width_r,product_ref_r,quantity_tons_log_r,customer_log_r,thickness_log_r,item_date_day_r,item_date_month_r,item_date_year_r,delivery_date_day_r,
#                      delivery_date_month_r,delivery_date_year_r)
# 
# 
#     st.write("## :green[**The Selling Price is :**]",round(pre_price,2))
# 
# 
# with tab2:
#   st.subheader(":green[**STATUS PREDECTION**]")
# 
# 
#   col1,col2=st.columns(2)
#   with col1:
# 
#     country= st.number_input(label="**COUNTRY_**", min_value=25, max_value=113)
#     item_type= st.number_input(label="**ITEM TYPE_**",min_value=0, max_value=6)
#     application= st.number_input(label="**APPLICATION_**",min_value=2.0, max_value=87.5)
#     width= st.number_input(label="**WIDTH_**",min_value=700.0, max_value=1980.0)
#     product_ref= st.number_input(label="**PRODUCT_REF_**",min_value=611728, max_value=1722207579)
#     quantity_tons_log= st.number_input(label="**QUANTITY_TONS_ (Log Value)_**",min_value=-0.3223343801166147, max_value=6.924734324081348,format="%0.15f")
#     customer_log= st.number_input(label="**CUSTOMER (Log Value)_**",min_value=17.21910565821408, max_value=17.230155364880137,format="%0.15f")
#     thickness_log= st.number_input(label="**THICKNESS (Log Value)_**",min_value= -1.7147984280919266, max_value=3.281543137578373,format="%0.15f")
# 
#   with col2:
# 
# 
# 
#     selling_price_log=st.number_input("**SELLING PRICE_**")
#     st.write("**ITEM DATE_**")
#     item_date_day= st.selectbox("**DAY_**",options=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"),key="delivery_date_day_c")
#     item_date_month= st.selectbox("**MONTH_**",options=("1","2","3","4","5","6","7","8","9","10","11","12"),key="item_date_month_c")
#     item_date_year= st.selectbox("**YEAR_**",options=("2020","2021"),key="item_date_year_c")
#     st.write("**DELIVERY DATE_**")
#     delivery_date_day= st.selectbox("**DAY_**",options=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"),key="delivery_date_day_classification")
#     delivery_date_month= st.selectbox("**MONTH_**",options=("1","2","3","4","5","6","7","8","9","10","11","12"),key="delivery_date_month_c")
#     delivery_date_year= st.selectbox("**YEAR_**",options=("2020","2021","2022"),key="delivery_date_year_c")
# 
# 
# 
#   button= st.button(":violet[**PREDICT THE STATUS(WON/LOSE)**]",use_container_width=True)
#   if button:
#     stat_pred=status_predection(country,item_type,application,width,product_ref,quantity_tons_log,customer_log,thickness_log,selling_price_log,item_date_day,item_date_month,item_date_year,delivery_date_day,
#                      delivery_date_month,delivery_date_year)
# 
# 
#     st.write("## :green[**The status is :**]",stat_pred)
#

!wget -q -O - ipv4.icanhazip.com

!streamlit run copper_app_test.py & npx localtunnel --port 8501