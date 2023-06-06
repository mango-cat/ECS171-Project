## Running the Webpage
All the source code for our webpage can be found in the ProjectWebsite folder.
Our website is a Flask application, and it can be run by typing:

```terminal
akhilarunachalam@Akhils-MacBook-Air-6 Project_FrontEnd % python3 app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
 ```

Then you can paste the url provided by Flask as output (http://127.0.0.1:5000) 
into a web browser such as Chrome. All you have to do is type a url into the 
textbox, and click the submit button in order to classify the url.

For some people, they may get a KeyError warning displayed on the webpage when 
they submit an url. This is because pickle may have trouble loading the decision 
tree model from the model.joblib located in ECS 171-Project/Project-Website/Models. 
when the model is dumped to the file and loaded from the file using different 
versions of Scikit-Learn. In case this happens, we have provided a screen recording 
of our code and our website where we test a couple of Urls in the Screen_Recording 
folder in our repository. 
