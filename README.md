# class-scheduler
Built with guide: https://stackabuse.com/deploying-a-flask-application-to-heroku/

## Running web server locally
```
source venv/bin/activate
pip install -r requirements
python app.py
```
Then go to localhost:5000

## Add new packages
```
source venv/bin/activate
pip install <package_name>
pip freeze > requirements.txt
```
Make sure you commit the requirements file

App located on Heroku: https://dashboard.heroku.com/apps/class-scheduler-erel/