# Covid-19 Forecaster ©

**App description**

This is an interactive web application which offers tools for visualising and forecasting data related to Covid-19 in Germany, starting from early beginnings of the virus evolution.

The whole development process was based on OSEMN methodology: **O**btain, **S**crub and **E**xplore data, **M**odel and i**N**terpret the data, **D**eploy the model. 

Dataset used: 
https://www.kaggle.com/headsortails/covid19-tracking-germany

The project includes the following modules:

- ```expl_analysis.ipynb``` the file that contains all the details about data processing and exploratory analysis
- ```forecasting_choice.ipynb``` the file which contains all information regarding the forecaster choise for prediction model 
- ```app.py``` the main script which is responsible for model deployment

To run this project, you first should install the following dependencies by running the following command:

```
$ pip install -r requirements.txt
```

Make sure that you have changed the file paths ```cases_file_path```, ```deaths_file_path``` and ```recovered_file_path``` in ```app.py``` to the actual path of the following files:
in your local machine.

Then start it in the folder ```code```, by running this command in your terminal:
```
python app.py
```

