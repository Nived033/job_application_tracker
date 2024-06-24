from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['job_tracker']
applications_collection = db['applications']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        job_title = request.form['job_title']
        company = request.form['company']
        application_date = request.form['application_date']
        status = request.form['status']
        
        if not job_title or not company or not application_date or not status:
            return "Please provide all the required fields"
        
        job = {
            'job_title': job_title,
            'company': company,
            'application_date': application_date,
            'status': status
        }
        applications_collection.insert_one(job)
        return redirect(url_for('view_applications'))
    
    return render_template('addition_job_info.html')

@app.route('/applications')
def view_applications():
    applications = applications_collection.find()
    return render_template('applications.html', applications=applications)

@app.route('/update_status/<job_id>', methods=['POST'])
def update_status(job_id):
    new_status = request.form['status']
    applications_collection.update_one({'_id': ObjectId(job_id)}, {'$set': {'status': new_status}})
    return redirect(url_for('view_applications'))

if __name__ == '__main__':
    app.run(debug=True)
