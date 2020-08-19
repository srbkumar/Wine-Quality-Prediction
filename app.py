# importing all the important libraries
from flask import Flask,render_template, request, send_file, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
sns.set()
import pickle

app = Flask(__name__) #initializing the Flask app

@app.route('/',methods=['GET']) # Route to display the HomePage
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # Route to show all the prediction values
@cross_origin()
def index():
    print('1.Here')
    #reading the inputs given by user
    fixed_acidity = float(request.form['fixed_acidity'])
    volatile_acidity = float(request.form['volatile_acidity'])
    citric_acid = float(request.form['citric_acid'])
    residual_sugar = float(request.form['residual_sugar'])
    chlorides = float(request.form['chlorides'])
    free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])
    total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])
    density = float(request.form['density'])
    pH = float(request.form['pH'])
    sulphates = float(request.form['sulphates'])
    alcohol = float(request.form['alcohol'])
    print('2.Here')

    filename ='modelForPrediction.sav'
    loaded_model = pickle.load(open(filename,'rb')) #loading themodel filesfrom storage
    scalar = pickle.load(open('StandardScalar.sav','rb'))
    prediction = loaded_model.predict(scalar.transform([[fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol]]))
    print('Predicion is: ',prediction)
    #if ()
    return render_template("result.html",output=prediction,)

@app.route('/uploadfile',methods=['POST','GET'])  #
@cross_origin()
def uploadfile():
    return render_template('upload.html')

@app.route('/csv',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def csv():
    if request.method == 'POST':
        try:
            #reading csv file
            uploaded_file = request.files['upload_file']
            filename = uploaded_file.filename

            #procede only if file is available
            if uploaded_file.filename != '':
                uploaded_file.save(filename)
                data = pd.read_csv(filename)


                # procede only if file is in correct format
                if len(data.columns) == 11:

                    #filling NaN values if present in dataset
                    data['fixed acidity'].fillna(value=round(data['fixed acidity'].mean()), inplace=True)
                    data['volatile acidity'].fillna(value=round(data['volatile acidity'].mean()), inplace=True)
                    data['citric acid'].fillna(value=round(data['citric acid'].mean()), inplace=True)
                    data['residual sugar'].fillna(value=round(data['residual sugar'].mean()), inplace=True)
                    data['chlorides'].fillna(value=round(data['chlorides'].mean()), inplace=True)
                    data['free sulfur dioxide'].fillna(value=data['free sulfur dioxide'].mean(), inplace=True)
                    data['total sulfur dioxide'].fillna(value=data['total sulfur dioxide'].mean(), inplace=True)
                    data['density'].fillna(value=round(data['density'].mean()), inplace=True)
                    data['pH'].fillna(value=round(data['pH'].mean()), inplace=True)
                    data['sulphates'].fillna(value=round(data['sulphates'].mean()), inplace=True)
                    data['alcohol'].fillna(value=round(data['alcohol'].mean()), inplace=True)

                    # loading the model file from the storage
                    model_filename = 'modelForPrediction.sav'
                    loaded_model = pickle.load(open(model_filename, 'rb'))

                    # loading Scaler pickle file
                    scaler = pickle.load(open('StandardScalar.sav', 'rb'))


                    #deleting previous files present in csv_file folder
                    csv_files = './csv_file'
                    list_of_files = os.listdir(csv_files)
                    for csfile in list_of_files:
                        try:
                            os.remove("./csv_file/" + csfile)
                        except Exception as e:
                            print('error in deleting:  ', e)

                    # making prediction
                    prediction = loaded_model.predict(scaler.transform(data))
                    data['Prediction Of Wine Quality'] = prediction

                    #saving pandas dataframe as a csv file in csv_file folder
                    result_file = './csv_file/result_output_data.csv'
                    data.to_csv(result_file)

                    #plot for prediction analysis
                    sns.set_style(style='darkgrid')
                    total_pridiction = sns.catplot(x='Prediction Of Wine Quality', kind='count', data=data)
                    #sns.set_style(style='darkgrid')
                    #total_pridiction= sns.countplot(x='Prediction Of Wine Quality', data=data)
                    print('Till Here')

                    # deleting previous graph images present in statistics folder
                    image_files = './static/stats'
                    list_of_files = os.listdir(image_files)
                    for imgfile in list_of_files:
                        try:
                            os.remove("./static/stats/" + imgfile)
                        except Exception as e:
                            print('error in deleting:  ', e)

                    #save graph in statictics folder inside static
                    print('2.Till Here')
                    output_path_total = './static/stats/output_prediction.png'
                    print('3.Till Here')
                    total_pridiction.savefig(output_path_total)
                    print('4.Till Here')


                    return render_template('csv.html')

                else:
                    return 'Error: Please Make Sure that csv file is in standard acceptable format. Please go through the given sample csv file format'


            else:
                return 'File Not Found'


        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')

@app.route('/download')  #
@cross_origin()
def download_file():
    p = './csv_file/result_output_data.csv'
    return send_file(p, as_attachment=True)

@app.route('/stats',methods=['POST','GET'])  #
@cross_origin()
def stats():
    return render_template('stats.html')

if __name__ == "__main__":
    app.run(debug= True) #running the app
