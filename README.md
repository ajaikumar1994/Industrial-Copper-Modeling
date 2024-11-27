# Industrial-Copper-Modeling
Problem Statement:
  
  The copper industry, while dealing with relatively less complex data, faces challenges due to data quality issues like skewness and noise. These issues can significantly impact the accuracy of manual predictions, leading to suboptimal pricing decisions and inefficient lead generation.
  
  Objective:
  
  To develop a robust machine learning solution that addresses these challenges:
  
  Predictive Modeling:
  
  Task:
  
  Predict the Selling_Price of copper products based on historical data.
  
  Approach:
  
  Employ advanced regression techniques to handle data irregularities and accurately forecast prices.
  Lead Classification:
  
  Task: 
  
  Classify leads as either "WON" (successful) or "LOST" (unsuccessful) to prioritize sales efforts.
  
  Approach:
  
  Utilize effective classification algorithms to identify high-potential leads.
  
  Solution Approach:
  
  Data Exploration and Preprocessing:
  
  Conduct in-depth data analysis to identify and address issues like missing values, outliers, and data skewness.
  Implement data cleaning and preprocessing techniques to prepare the data for modeling.
  Model Development and Training:
  
  Regression Model:
  
  Select appropriate regression algorithms (e.g., Linear Regression, Decision Tree Regression, Random Forest Regression, XGBoost Regression) based on data characteristics.
  Train and fine-tune the model to minimize prediction errors.
  
  Classification Model:
  
  Choose suitable classification algorithms (e.g., Logistic Regression, Decision Tree Classification, Random Forest Classification, XGBoost Classification, Support Vector Machine) to accurately classify leads.
  Train and optimize the model to maximize predictive accuracy.
  
  Model Deployment and User Interface:
  
  Deploy the trained models to a production environment.
  Develop a user-friendly Streamlit interface that allows users to input relevant data and receive real-time predictions for Selling_Price and Status.
  
  Expected Outcomes:
  
  Improved Pricing Accuracy:
  
  The regression model will provide more accurate Selling_Price predictions, enabling optimal pricing strategies.
  
  Enhanced Lead Prioritization:
  
  The classification model will help identify high-potential leads, allowing sales teams to focus on the most promising opportunities.
  Efficient Decision-Making: The Streamlit app will provide timely insights and predictions, empowering decision-makers to make informed choices.
  By addressing these challenges and leveraging the power of machine learning, the copper industry can achieve significant improvements in efficiency, profitability, and overall business performance.


Industrial Copper Modeling - Streamlit App

This Streamlit app provides a user interface for predicting the selling price and status (WON/LOST) of copper products based on historical data and machine learning models.

Features:

Price Prediction: Input various features related to a copper product and receive the predicted selling price.
Status Prediction: Enter details about a potential sale and get a prediction on whether it will be successful (WON) or unsuccessful (LOST).
User-friendly Interface: The app utilizes Streamlit to offer a clear and interactive interface for easy data input and prediction results.

Requirements:

Python 3.x
streamlit
pandas
numpy
scikit-learn (specifically RandomForestRegressor for regression and a classification model like RandomForestClassifier)
streamlit_option_menu (optional, for tabbed navigation)
streamlit_calendar (optional, for calendar input)
pickle (for loading pre-trained models)
Instructions:

Install Dependencies:

pip install streamlit 
pip install pandas 
pip install numpy 
pip install scikit-learn 
pip install streamlit_option_menu 
pip install streamlit_calendar 
pip install pickle


Replace Model Paths:

Edit the paths in price_predection and status_prediction functions to point to the locations of your saved regression model (regression_model.pkl) and classification model (classification_model.pkl).

Run the App:

streamlit run copper_app_test.py

Description of Functionality:

The app is divided into two tabs: "PRICE PREDICTION" and "STATUS PREDICTION".
Users can input various features relevant to a copper product or potential sale.
Features include country, status, item type, application, width, product reference, quantity (log value), customer (log value), thickness (log value), item date (day, month, year), and delivery date (day, month, year).
The app leverages pre-trained machine learning models (loaded using pickle) to make predictions.
Clicking the prediction buttons displays the predicted selling price (rounded to two decimal places) or the predicted status (WON/LOST).

Future Enhancements:

Implement error handling for invalid user input.
Expand prediction features to include more data points.
Integrate data visualization elements for insights into model performance.
Deploy the app to a cloud platform for wider accessibility.

Disclaimer:

This is a basic example. The effectiveness of the predictions depends heavily on the quality of your trained machine learning models.

























