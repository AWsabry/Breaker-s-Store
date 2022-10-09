# importing the requests library
import json
import random
import requests
# importing Hash Library
import hashlib
URL = "https://atfawry.fawrystaging.com/ECommerceWeb/Fawry/payments/charge"

# Payment Data
merchantCode    = '1tSa6uxz2nTwlaAmt38enA=='
merchantRefNum  = '23124654641'
merchant_cust_prof_id  = '777777'
payment_method = 'PAYATFAWRY'
amount = '580.55'
merchant_sec_key =  '259af31fc2f74453b3a55739b21ae9ef' 
signature = hashlib.sha256(
        str(random.getrandbits(256)).encode('utf-8')).hexdigest()

# defining a params dict for the parameters to be sent to the API
PaymentData = {
    'merchantCode' : merchantCode,
    'merchantRefNum' : merchantRefNum,
    'customerName' : 'Ahmed Ali',
    'customerMobile' : '01234567891',
    'customerEmail' : 'example@gmail.com',
    'customerProfileId' : '777777',
    'amount' : '580.55',
    'paymentExpiry' : '1631138400000',
    'currencyCode' : 'EGP',
    'language' : 'en-gb',
    'chargeItems' : {
                          'itemId' : '897fa8e81be26df25db592e81c31c',
                          'description' : 'Item Description',
                          'price' : '580.55',
                          'quantity' : '1'
                      },
    'signature' : signature,
    'paymentMethod' : payment_method,
    'description': 'example description'
}

# sending post request and saving the response as response object
status_request = requests.post(url = URL, params = json.dumps(PaymentData))

# extracting data in json format
status_response = status_request.json()