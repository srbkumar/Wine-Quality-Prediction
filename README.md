# Wine-Quality-Prediction
Wine certification includes physiochemical tests like determination of density, pH, alcohol quantity, fixed and volatile acidity etc. We have a large datasets having the physiochemical tests results and quality on the scale of 1 to 10 of wines of the Vinho Verde variety.Such a model can be used not only by the certification bodies but also by the wine producers to improve quality based on the physicochemical properties and by the consumers to predict the quality of wines.

## Prerequisites
1. Python
2. Pandas
3. matplotlib
4. numpy
5. scikit-learn
6. Dataset
The dataset used here is Wine Quality Data set from UCI Machine Learning Repository. The csv file needed "winequality-red.csv" is attached in the repository. The same can also be found here https://archive.ics.uci.edu/ml/datasets/Wine+Quality

Input variables (based on physicochemical tests):

fixed acidity
volatile acidity
citric acid
residual sugar
chlorides
free sulfur dioxide
total sulfur dioxide
density
pH
sulphates
alcohol
Output variable (based on sensory data): quality (score between 0 and 10)
