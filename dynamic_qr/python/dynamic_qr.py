import requests
import base64
import time
import uuid
import json
import hmac
import hashlib

USERNAME = 'MERCHANT_ID'
PASSWORD = 'MERCHANT_PASSCODE'
SIGN_SECRET = 'MERCHANT_KEY'

url = "https://khalti.com/api/qr/generate_dynamic/"

nonce = int(time.time())

prn = str(uuid.uuid4())

payment_data = {
    'prn': prn,
    'amount': 100.00,
    'vat_amount': 50.00,
    'vat': 6.50,
    'remarks1': "",
    'remarks2': "",
    'nonce': nonce
}

payment_json = json.dumps(payment_data, indent=4)
encoded_payload = base64.b64encode(payment_json.encode("ascii")).decode()

cipher_text = encoded_payload + "+" + str(SIGN_SECRET)

print("Cipher TEXT === ", cipher_text)

signature = hmac.new(SIGN_SECRET.encode('ascii'),
                     cipher_text.encode('ascii'), "sha256").hexdigest()

payload = {'payload': encoded_payload,
           'signature': signature
        }

auth_string = f"{USERNAME}:{PASSWORD}"
auth_string_encoded = base64.b64encode(auth_string.encode("ascii")).decode('ascii')
authorization = f"Basic {auth_string_encoded}"

headers = {
    'Authorization': authorization,
    'X-KhaltiNonce': str(nonce)
}

print(f"headers: {headers}, {json.dumps(payload, indent=4)}")

response = requests.post(url, headers=headers, data=payload)
response_json = response.json()

print("################################################################################")

print("Response == ", response.status_code)
print(json.dumps(response_json, indent=4))

print("################################################################################")
