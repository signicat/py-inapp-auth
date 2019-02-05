import sys
import requests
import random
from time import sleep
import urllib.parse as urlparse
from pkce import code_verifier, code_challenge


""" BD: Needs to be the birth of date of a Norwegian BankID test-user setup with "BankID på Mobil"!
    Format: ddmmyy
    PN: Needs to be the phone number for the test-user.
    See https://developer.signicat.com/id-methods/norwegian-bankid-on-mobile/#test-information
"""
cfg = {'BD': '', 'PN': ''}
if str.isdigit(cfg['BD']) is False or len(cfg['BD']) is not 6 :
    print("The variable cfg['BD'] needs to be date-of-birth in format 'DDMMYY'.")
    sys.exit()
if str.isdigit(cfg['PN']) is False or len(cfg['PN']) is not 8:
    print("The variable cfg['PN'] needs to be an 8-digit Norwegian phone number without country code.")
    sys.exit()

# STEP 0: Prepare PKCE (https://tools.ietf.org/html/rfc7636)
verifier = code_verifier(40)
challenge = code_challenge(verifier)
print("PKCE: verifier='{}', challenge='{}'".format(verifier, challenge))

# STEP 1: Call authorize using method "nbid-inapp"
headers1 = {'Accept': 'application/json'}
url1 = ('https://preprod.signicat.com/oidc/authorize?response_type=code&scope=openid+profile&client_id=demo-inapp&redirect_uri=https://example.com/redirect&acr_values=urn:signicat:oidc:method:nbid-inapp&state={}&login_hint=birthdate-{}&login_hint=phone-{}&code_challenge_method=S256&code_challenge={}'
        .format(''.join(random.choice('ABCDEF0123456789') for _ in range(8)), cfg['BD'], cfg['PN'], challenge.decode()))
r1 = requests.get(url1, headers=headers1)
jar = r1.cookies # !IMPORTANT! Saves all cookies - to be used in future requests.
res1 = r1.json()
print("Authorize Response: {}".format(res1))

# STEP 2: Poll collectUrl until status=finished
url2 = res1['statusUri']
PS = {'status': None}
print("\nPolling...")
while 'finished' not in PS: # Check if finished, if not sleep 5s and check again.
    sleep(5)
    res2 = requests.get(url2, headers=headers1, cookies=jar).json()
    PS = res2['status']
    print("  -- Status: {}".format(PS))
print("collectUrl Response: {}".format(res2))

# STEP 3: Call completeUrl - the last redirect will contain CODE and STATE.
url3 = res2['completeUri']
r3 = requests.get(url3, cookies=jar) # requests.get() method automatically follows redirects.
res3 = r3.history[-1].headers['Location'] # Get the LAST of the redirects. This contains code and state.
res3_params = urlparse.parse_qs(urlparse.urlparse(res3).query)
print("\nFinal redirect from completeURL: {}".format(res3))
print("  -- CODE: '{}'".format(res3_params['code'][0]))
print("  -- STATE: '{}'".format(res3_params['state'][0]))

# STEP 4: Call /token end-point as normal (using CODE we got in STEP 3)
headers2 = {'Authorization': 'Basic ZGVtby1pbmFwcDptcVotXzc1LWYyd05zaVFUT05iN09uNGFBWjd6YzIxOG1yUlZrMW91ZmE4'}
payload = {
    'client_id': 'demo-inapp',
    'redirect_uri': 'https://example.com/redirect',
    'grant_type': 'authorization_code',
    'code_verifier': verifier.decode(),
    'code': res3_params['code'][0]
}
res4 = requests.post('https://preprod.signicat.com/oidc/token', data=payload, headers=headers2).json()
token = res4['access_token'] # Access token!
print("\nAccess Token: {} ... (Truncated {} Bytes)".format(token[:33], len(token)-33))

# STEP 5 (optional): Call /userinfo with access token.
headers3 = {'Authorization': 'Bearer ' + token}
res5 = requests.get('https://preprod.signicat.com/oidc/userinfo', headers=headers3).json()
print("UserInfo Response: {}".format(res5))
