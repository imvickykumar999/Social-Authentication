
from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'myauthentication'

# app.config['SERVER_NAME'] = 'localhost:5000'
oauth = OAuth(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/facebook/')
def facebook():
    instaConfig = {
	'client_id':'***********************',
	'client_secret':'**************************',
	'redirect_uri' : 'http://localhost:8081/instagram_callback/'
    }

    FACEBOOK_CLIENT_ID = instaConfig['client_id']
    FACEBOOK_CLIENT_SECRET = instaConfig['client_secret']

    oauth.register(
		name='facebook',
		client_id=FACEBOOK_CLIENT_ID,
		client_secret=FACEBOOK_CLIENT_SECRET,
		access_token_url='https://graph.facebook.com/oauth/access_token',
		access_token_params=None,
		authorize_url='https://www.facebook.com/dialog/oauth',
		authorize_params=None,
		api_base_url='https://graph.facebook.com/',
		client_kwargs={'scope': 'email'},
	)
    print('Authenticating..............................................')
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/facebook/auth/')
def facebook_auth():
    print('Welcome..............................................')
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
    'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)
    return render_template('welcome.html')

if __name__ == "__main__":
	app.run(debug=True)
