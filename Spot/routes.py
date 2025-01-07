from flask import render_template, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
import os
import requests
from .mydb import db
from .mydb import FoodItem
from .mydb import User


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
        return render_template("index.html", user=user)

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

      

        user = User.query.filter_by(google_id=userinfo["sub"]).first()
        if not user:
            user = User(
                google_id=userinfo["sub"],
                name=userinfo["name"],
                email=userinfo["email"],
                isAdmin=False
            )
            db.session.add(user)
            db.session.commit()

        session["user"] = {
            "name": userinfo["name"],
            "email": userinfo["email"],  
            "isAdmin": user.isAdmin 
        }
        return redirect(url_for("home"))

    def credentials_to_dict(credentials):
        credDict = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
        return credDict


    @app.route("/logout")
    def logout():
        session.pop("user", None)
        session.pop("credentials", None)
        return redirect("/")


    @app.route('/chocolate')
    def page1():
        food_item = FoodItem.query.get(1)
        return render_template('chocolate.html', food_item=food_item)

    @app.route('/caramel')
    def page2():
        food_item = FoodItem.query.get(2)
        return render_template('caramel.html', food_item=food_item)

    @app.route('/chicken')
    def page3():
        food_item = FoodItem.query.get(3)
        return render_template('chicken.html', food_item=food_item)

    @app.route('/rice')
    def page4():
        food_item = FoodItem.query.get(4)
        return render_template('rice.html', food_item=food_item)
    
    @app.route("/users")
    def adminUser():
        
        if not session["user"].get("isAdmin"):
            return render_template('accessDenied.html'),403
        else:
            users = User.query.all()
            return render_template('users.html', users=users)