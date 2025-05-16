import os
import requests
from flask import Flask, redirect, request
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

load_dotenv()

app = Flask(__name__)

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

from firebase_admin import credentials

cred = credentials.Certificate({
  "type": "service_account",
    "project_id": "form-e74ab",
    "private_key_id": "764f0a6cad71edf7d4f7dd4f0c7be3ef91cf13df",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDKImLKTL/6DYz+
Z/IDtsGNqiNfVwQiI1/b/GultWFFfLfOMLX9echpBjllvtTaO1mChJhsbwnAKnBv
XoRR75sq7w3TkxL35RKlC7qS/NNizVMPp1WjkSHp3EDpDqt1sNdaQctOCPWIXn0G
3qXFeWCUSOD4lnBQ9WS4++s56KtM4dRkCcEIKustYVSFAXCCvuMBSOKPK8jtcTWs
mEjoExIPYuD8u135FAxDTveyFRJVPKn5+CNNThY8kBV6Ga/RzzOHFFAiabkD91+J
K6vNzvC0AnG4LnINugjyW/g1hjSt2URV8K3Uvf2OQWmeNDPd6PaXMZ9Qt7HnC3Pd
Kq6dCetxAgMBAAECggEAIAIDbkDqinRgXf3EQUnMivwE12lOToCXAp0NR8N5yHjY
G0az3tRMw7K4Xo/yIS+SPDx2bX9ExkECJmSLY/Ui91C8+gKZV5dW1TtO+00dRRE5
5KntAfZurhtSTQVlacDLzS9LfAsnpEVAG5kgm21duYVz2HFsDinZngBITpZ1H7p/
sfmHXeISr4azQhtSecfmkyKCivPWaR5QWBMPrGjOJpL/8wIyXXKeQ2jL3oHWOg80
DZttfFKpI3j0I2KnaIYAlyG95dgEpvV8VsV7CHRIqxJXs14eygbSTZJN93c93beZ
St0EON0qpkoI+1iXc7oQw1ee/qstxHasYdA49d98ZQKBgQDR1l9yj3DluM+8vqoi
6EL+PgTcnw7jLfPrLY694ETWcmdhMFc70AnlOVcvRUQ+S6sM7XIff7D1M50yMLlb
/r6dQdC01ZjWea0V1dI7FpfZbDCLDg/+PWIQJ/PoQBni5DrxDlXsiqZkEjF/ndFz
tFbHnBev8JnRFqMVgZlAMj6PPQKBgQD2mjDv2lV44aK5W+ushiRWaHjzVTl13Eix
eFYG2mE0S8Cr1keL0Q+izfk08GDXZRImetvFfDezYCLYnyJUQHU8h9j75G206SxA
03cx5lq6LJRwlDr6LXzl6n2u267UOLM2fJpEBwdDQhZh/YjmFPKxGGjx7XkroqGX
Fq+TQbeQRQKBgFOGmJG6ZT8b9Jz17DVe7KPVPgwvyDZH6Wr4xHPyXJRcD6iRHHgz
lGzJCVpIoSSG7DyGG8JMCr1f4TfES1RCL8/bDd+dkmv1HR+u8DMTCDjEpwIDA/y4
pFs3/A+7zFITdR7VDQDOI/N7hnZ89I2xAEYObSNci22+LAZ4gu8Z0OslAoGBAOVA
hwoUEa2lJd/oInpq4lEqInck3ZxCQ5oo4uDQF9nEKsQVGsJSgpS5o1mhtoXHwk3f
nXxEdIvfbcWwevuUSOkS6ZeSzqKGussxS/gpzGKTmxPl2cZGj3w2uMzcEfXdGE4p
HEjtt8TBJYnHZ4NuKgiVRsrSF/mG4W5SersNNxd5AoGALJ6OQAjSO9yKmvZDQjRX
BE3PVxXeA5uXg7660kn8dLOrpeHnXV33auMoDSXez9hSj/2adXDUGA1cvgK13b61
IHmCasoXmNL2iqz5ER18WSFCvAc5Pp1Q1Vhcm2lNRQFgTCKZ3bNbotNLtio2gy/5
vW6/Y4pl9COtGDYzsld4yWg=
-----END PRIVATE KEY-----\n""",
    "client_email": "firebase-adminsdk-dvvfl@form-e74ab.iam.gserviceaccount.com",
    "client_id": "101921514795688112776",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dvvfl%40form-e74ab.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred, {
    "databaseURL": os.getenv("FIREBASE_URL")
})
@app.route("/")
def index():
    # Updated to include additional OAuth scopes
    scope = "identify email guilds guilds.join connections"
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}")


@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify email guilds guilds.join connections'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Get access token from Discord OAuth2
    r = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    r.raise_for_status()
    access_token = r.json()['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Fetch user information
    user_info = requests.get('https://discord.com/api/users/@me', headers=headers).json()

    # Fetch the user's guilds
    guilds_info = requests.get('https://discord.com/api/users/@me/guilds', headers=headers).json()

    # Fetch the user's connections
    connections_info = requests.get('https://discord.com/api/users/@me/connections', headers=headers).json()

    discord_id = user_info['id']
    username = user_info['username']
    email = user_info['email']

    # Push verified user data to Firebase
    ref = db.reference("verified_users")
    ref.push({
        "discord_id": discord_id,
        "username": username,
        "email": email,
        "guilds": guilds_info,  # Save guilds info
        "connections": connections_info  # Save connections info
    })

    return f"✅ Verified You may now return to Discord."


if __name__ == "__main__":
    app.run(debug=True)