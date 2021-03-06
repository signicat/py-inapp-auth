# py-inapp-auth
### Functional examples of inapp authentication

---

These are **functional examples** of inapp authentication. It does not illustrate how to implement the methods in a mobile app, it merely illustrates the API calls required to make the flow work as expected. It can be viewed as a jumping-off point for your app implementation.

This example follows the documentation at [Swedish BankID: How to integrate authentication with Swedish BankID from a native app](https://developer.signicat.com/id-methods/swedish-bankid/#how-to-integrate-authentication-with-swedish-bankid-from-a-native-app).

PS: Documentation for the Norwegian implementation will be made available as soon as it's ready.

**Dependencies**:

* Python 3
* Built in: sys, random, time, urllib.parse
* [Requests](http://docs.python-requests.org/en/master/): HTTP for Humans.

### Supported eIDs.

* [nbid-inapp.py](./nbid-inapp.py): Norwegian BankID on mobile (BankID på Mobil)
* [sbid-inapp.py](./sbid-inapp.py): Swedish BankID on mobile (BankID på Mobil)

To be able to use our "inapp" flow, the eID must fullfil several technical requirements related to mobile integration. So far Signicat has created inapp methods for only Norwegian and Swedish BankID.

### Flow

1. Call /authorize.
2. Poll collect method until success.
3. Call complete method - the last redirect will contain CODE and STATE.
4. Call /token end-point as normal (using CODE we got in STEP 3).
5. Call /userinfo with access token. (optional)

Note: Step 1-3 should be performed in your mobile app. Step 4 & 5 should be performed at the web service hosted at your redirect URI.

### Application Usage

**Norwegian BankID** ([nbid-inapp.py](./nbid-inapp.py))

Both the variable ```cfg['BD']``` and ```cfg['PN']``` needs to be changed to a valid Norwegian BankID test-user. This test-user has to be enabled for BankID on a mobile device!
* BD: Needs to be the birth of date of a Norwegian BankID test-user setup with "BankID på Mobil"! Format: ddmmyy
* PN: Needs to be the phone number for the test-user. Format: nnnnnnnn

Once you have changed these variable, you can run it with ```python3 nbid-inapp.py```.

**Swedish BankID** ([sbid-inapp.py](./sbid-inapp.py))

You need to change the variable ```cfg['NID']``` to a valid Swedish BankID test-user. This test-user has to be setup in the mobile app on a mobile device! 

Once you have changed this variable, you can run it with ```python3 sbid-inapp.py```.

**Security Concerns**

There are certain key concepts to keep in mind to be able to achive a good level of security when implementing OIDC authentication in-app.
* [Proof Key for Code Exchange](https://tools.ietf.org/html/rfc7636): Signicat feels that a code interception attack is more likely with an in-app flow. As such it is **strongly recommended** that you implement this extension for OAuth/OIDC (supported by default on Signicat's OIDC clients). *The code examples in this repo already has PKCE implemented!*
* Unless you have specifically hardened security of your mobile application, you have to consider it somewhat unsafe. *OIDC tokens and client secrets provided by Signicat should not be stored in your app.*
* As mentioned earlier step 4 & 5 **should not** be performed in-app. 
* General hardening of mobile applications should also be considered. See for instance AppSamurai blog post: [12 Various Ways To Ensure Mobile Application Security](https://appsamurai.com/12-various-ways-to-ensure-mobile-application-security/)

### References

[Norwegian BankID: Test Information](https://developer.signicat.com/id-methods/norwegian-bankid-on-mobile/#test-information).

[Swedish BankID: Test Information](https://developer.signicat.com/id-methods/swedish-bankid/#test-information).

For general information about the Authentication service, please refer to [Get Started With Authentication](https://developer.signicat.com/documentation/authentication/get-started-with-authentication/).
