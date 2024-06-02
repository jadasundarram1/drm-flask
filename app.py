from flask import Flask, request, render_template, session
from google.cloud import bigquery
from google.oauth2 import service_account
from ai import cluster_emails
import os

credentials = service_account.Credentials.from_service_account_file(
'/Users/jadasundarram/Desktop/drm-code/directresponsemarketing-8a2f34248a42.json')
project_id = 'directresponsemarketing'
client = bigquery.Client(credentials=credentials, project=project_id)

secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        email = request.form['search']
        session['email'] = email
        query_results = get_cases_data(email)
        result_list = list(query_results)
        return render_template('results.html', results = result_list)
    
@app.route('/cluster_emails', methods=['POST'])
def cluster_emails_and_display():
    if request.method == 'POST':
        # Get the category from the form
        category = request.form['category']

        # Hardcoded list of email descriptions
        email = session.get('email', None)
        email_descriptions = organize_descriptions(email)
        print(email_descriptions)

        # Cluster the email descriptions
        predicted_categories = cluster_emails(email_descriptions)
        print(predicted_categories)

        formatted_categories = {}
        for email, category in predicted_categories.items():
            if category not in formatted_categories:
                formatted_categories[category] = []
            formatted_categories[category].append(email)
        print(formatted_categories)

        # Display the clustered results
        return render_template('cluster_results.html', category=category, results= list(formatted_categories))

# Define your other routes and functions as needed.   

def get_cases_data(input_email):
    query = f"SELECT isescalated, origin, contactphone, suppliedemail, casenumber, type, description FROM LLM_Sample.Case WHERE contactemail = '{input_email}'"
    query_job = client.query(query)
    results = query_job.result()
    return results

def organize_descriptions(input_email):
    query = f"SELECT description FROM LLM_Sample.Case WHERE contactemail = '{input_email}'"
    query_job = client.query(query)
    results = query_job.result()
    email_descriptions = [row[0] for row in list(results)]
    return email_descriptions

if __name__ == '__main__':
    app.run()

