from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:

        if request.form.get('folderPath') is not None:
            path = request.form.get('folderPath')
            print(f"Received folder path: {path}")
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table

        else:
            # Handle the case where 'folderPath' is not present or is None
            print("Error: 'folderPath' not present or is None")

    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")



@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        #This is when your model is called from Postman.

        # This is when your model is called from HTML wali sheet.

        if request.form.get('folderPath') is not None:
            path = request.form.get('folderPath')

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel()
            return Response("Prediction File created at %s!!!" % path)

        else:
            # Handle the case where 'folderPath' is not present or is None
            print("Error: 'folderPath' not present or is None")

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)





if __name__ == "__main__":
    app.run(debug=True)
