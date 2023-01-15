# OS
import os
import base64
import urllib.parse
import secrets
# External
from flask import Flask, request, redirect, session, render_template, url_for
import requests
# Internal
import utils
import forms

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("APP_SECRET_KEY")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# This should be the URL of your callback handler on your App Engine instance
redirect_uri = os.environ.get("CALLBACK_URL")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/publish", methods=["GET","POST"])
def publish():

    form = forms.LinkedInPost()

    if form.validate_on_submit():

        content = form.content.data

        result = utils.post(session["access_token"],content)
        return result

    return render_template("publish.html", form=form)

@app.route("/auth/linkedin")
def auth_linkedin():
    # Step 1: Direct the user to LinkedIn's authorization endpoint
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"

    # Generate a random state to protect against CSRF
    state = secrets.token_hex(16)
    session["state"] = state

    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": "w_organization_social"
    }

    auth_url = f"{auth_url}?{urllib.parse.urlencode(auth_params)}"

    return redirect(auth_url)

@app.route("/auth/linkedin/callback")
def auth_linkedin_callback():
    # Step 2: LinkedIn will redirect the user to the URL specified in the redirect_uri parameter, with a code parameter appended to the URL
    # Extract the code parameter from the URL
    code = request.args.get("code")
    state = request.args.get("state")

    # Verify that the state parameter matches the state stored in the session
    if state != session.get("state"):
        return "Invalid state"

    # Step 3: Send a POST request to LinkedIn's token endpoint to obtain an access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    # Construct the authorization header
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8"))

    token_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header.decode('utf-8')}",
    }

    response = requests.post(token_url, data=token_params, headers=headers)

    # Step 4: If the request is successful, LinkedIn will return a JSON object containing an access_token field
    if response.status_code == 200:
        token_response = response.json()
        access_token = token_response["access_token"]

        # Store the access token in the session
        session["access_token"] = access_token

        # Redirect the user to the home page
        return render_template("index.html")

if __name__=="__main__":
    app.run(port=5000, debug=True)