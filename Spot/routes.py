from flask import render_template, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
import os
import requests
from .mydb import db


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_SECRETS_FILE = "/Users/mac/Documents/GitHub/ICA-Mariela_Machuca/Spot/client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/userinfo.profile", 
          "https://www.googleapis.com/auth/userinfo.email", 
          "openid"]
REDIRECT_URI = "http://127.0.0.1:5000/callback"


def register_routes(app):
    @app.route("/")
    def login_page():
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login.html")

    @app.route("/home")
    def home():
        if "user" not in session:
            return redirect(url_for("login_page"))
        user = session["user"]
        return render_template("index.html")

    @app.route("/login")
    def login():
        flow = Flow.from_client_secrets_file(
            GOOGLE_CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    @app.route("/callback")
    def callback():
        state = session["state"]
        flow = Flow.from_client_secrets_file(
            GOOGLE_CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            state=state,
            redirect_uri=REDIRECT_URI,
        )
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        session["credentials"] = credentials_to_dict(credentials)

        # Fetch user info from Google API
        import requests
        userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"
        userinfo_response = requests.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {credentials.token}"},
        )
        userinfo = userinfo_response.json()

        session["user"] = {
            "name": userinfo["name"],
            "email": userinfo["email"],
            "picture": userinfo["picture"],
        }
        return redirect(url_for("home"))

    def credentials_to_dict(credentials):
        return {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }


    @app.route("/logout")
    def logout():
        session.pop("user", None)
        session.pop("credentials", None)
        return redirect("/")


    @app.route('/chocolate')
    def page1():
        return render_template('chocolate.html')

    @app.route('/caramel')
    def page2():
        return render_template('caramel.html')

    @app.route('/chicken')
    def page3():
        return render_template('chicken.html')

    @app.route('/rice')
    def page4():
        return render_template('rice.html')
