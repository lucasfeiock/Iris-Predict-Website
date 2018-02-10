from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
import requests

SECRET_KEY = 'development'

app = Flask(__name__)
app.config.from_object(__name__)

class SimpleForm(FlaskForm):
    sepalLength = TextField('Sepal Length')
    sepalWidth = TextField('Sepal Width')
    petalLength = TextField('Petal Length')
    petalWidth = TextField('Petal Width')
    submit = SubmitField('Predict Species')
    results = TextField('Results')

@app.route('/',methods=['post','get'])
def hello_world():
    try:
        form = SimpleForm()
        if form.validate_on_submit():
            print("TEST")
            endpoint = "http://40.79.70.90/api/v1/service/service000/score"
            headers = {"Content-Type":"application/json","Authorization":"Bearer eeff1ef1e11d49b09e240b7a11618405"}
        
            data = "{\"input_df\": [{"
            data = data + "\"petal length\":" + form.petalLength.data + ","
            data = data + "\"petal width\":" + form.petalWidth.data + ","
            data = data + "\"sepal length\":" + form.sepalLength.data + ","
            data = data + "\"sepal width\":" + form.sepalWidth.data
            data = data + "}]}"
            results = requests.post(endpoint,data=data,headers=headers).json()
            form.results.data = results.replace('"','').replace('-','_')
            form.iris = results.replace('"','').replace("-","_") + ".jpg"
        else:
            print(form.errors)
        return render_template('index.html',form=form)
        
    except:
        return 'There was an error'

if __name__ == '__main__':
    app.run(debug=True)