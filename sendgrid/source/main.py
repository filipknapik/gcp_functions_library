import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import jsonify

def execute(request):
    request_json = request.get_json()
    key = request_json['key']
    email_from = request_json['email_from']
    email_to = request_json['email_to']
    subject_txt = request_json['subject']
    content_txt = request_json['content']
    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject=subject_txt,
        html_content=content_txt)
    try:
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
        return jsonify({"Result":e}), 500
    return jsonify({"Result":"OK"}), 200
