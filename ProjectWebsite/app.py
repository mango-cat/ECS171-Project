from flask import Flask, render_template, request
from data_processing import runModel

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        
        result = runModel(url)

        return render_template("index.html", result=result)
    
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)