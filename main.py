from http import client
import os
import time
import psycopg2
import requests
import boto3
from flask import Flask, request
from apscheduler.schedulers.blocking import BlockingScheduler
from psycopg2 import Error

app = Flask(__name__)
print("Script started")
# Use environment variables for sensitive data
PAGE_ACCESS_TOKEN = os.getenv('removed for security reasons')
AWS_ACCESS_KEY = os.getenv('removed for security reasons')
AWS_SECRET_KEY = os.getenv('removed for security reasons')
print("Script started")

# Function to retrieve data from Athena
def get_athena_data():
    athena = boto3.client('athena', 
                      region_name='us-east-1', 
                      aws_access_key_id=AWS_ACCESS_KEY, 
                      aws_secret_access_key=AWS_SECRET_KEY)
    # Code to retrieve data from Athena goes here.
    # This function should return the data you want to send to the user.

# Function to send a message to the user
def send_message(recipient_id, message):
    data = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message
        }
    }
    response = requests.post('https://graph.facebook.com/v13.0/me/messages?access_token=' + PAGE_ACCESS_TOKEN, json=data)

# Function to get a connection to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="removed for security reasons",
            user="removed for security reasons",
            password="removed for security reasons",
            host="removed for security reasons",
            port="removed for security reasons"
        )
        return conn
    except Error as e:
        print("Unable to connect to the database", e)


@app.route("/", methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.getenv("VERIFY_TOKEN"):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route("/", methods=['POST'])
def receive_message():
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                message_text = message['message'].get('text')

                if message_text.lower() == 'subscribe':
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""
                    INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING
                    """, (recipient_id,))
                    conn.commit()
                    cur.close()
                    conn.close()

                    # Send a confirmation message back to the user
                    send_message(recipient_id, "Thanks for using TotallyAir, we will update you from now on.")

                elif message_text.lower() == 'update me':
                    # Check if the user is in the database
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""
                    SELECT * FROM users WHERE user_id = %s
                    """, (recipient_id,))
                    user = cur.fetchone()
                    cur.close()
                    conn.close()

                    # If the user is in the database, send them an update
                    if user:
                        message = create_message()
                        send_message(recipient_id, message)

    return "Message Processed"



def create_message():
    # Connect to AWS Athena and retrieve your data
    # This is a placeholder. Replace this with your actual data retrieval
    query_result = client.start_query_execution(
        QueryString="SELECT * FROM removed for security reasons ORDER BY date_de_fin DESC LIMIT 1",
        QueryExecutionContext={
            'Database': 'removed for security reasons'
        },
        ResultConfiguration={
            'OutputLocation': 's3://removed for security reasons',
        }
    )
    query_id = query_result['QueryExecutionId']
    query_detail = client.get_query_execution(QueryExecutionId=query_id)
    while query_detail['QueryExecution']['Status']['State'] not in ['SUCCEEDED', 'FAILED']:
        time.sleep(3)
        query_detail = client.get_query_execution(QueryExecutionId=query_id)
    result = client.get_query_results(QueryExecutionId=query_id)
    
    # Extract the data from the result
    data = result['ResultSet']['Rows'][1]['Data']
    date_de_fin = data[1]['VarCharValue']
    nom_site = data[6]['VarCharValue']
    polluant = data[8]['VarCharValue']
    valeur = data[14]['VarCharValue']
    unite_de_mesure = data[16]['VarCharValue']

    # Format the data into a message
    message = f"On {date_de_fin}, the concentration of {polluant} at {nom_site} was {valeur} {unite_de_mesure}. Stay safe and breathe easy!"

    return message

def send_daily_updates():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    user_ids = cur.fetchall()
    cur.close()
    conn.close()

    message = create_message()

    for user_id_tuple in user_ids:
        user_id = user_id_tuple[0]  # extract the user_id from the tuple
        send_message(user_id, message)

scheduler = BlockingScheduler()
scheduler.add_job(send_daily_updates, 'cron', hour=8)
scheduler.start()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    print("Script started")