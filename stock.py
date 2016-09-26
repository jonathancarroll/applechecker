#!/usr/bin/env python
import time
import sys
import smtplib
from socket import gaierror
import requests
from twilio.rest import TwilioRestClient


#Replace the account, token and smsFrom number with those associated with your twilio account
account = "ACCOUNTIDGOESHERE"
token = "TOKENGOESHERE"
smsFrom = "+15554443333"
client = TwilioRestClient(account, token)

# only tested for US stores and US text message
URL = "http://www.apple.com/shop/retail/pickup-message"
BUY = "http://store.apple.com/xc/product/"

DATEFMT = "%m/%d/%Y %H:%M:%S"
LOADING = ['-', '\\', '|', '/']

def main(model, zipcode, dest, sec=5, login=None, pwd=None):
    good_stores = []
    my_alert = Alert(dest, login, pwd)
    initmsg = ("[{0}]start tracking {1} in {2}. "
               "Alert will be sent to {3}").format(time.strftime(DATEFMT),
                                                   model, zipcode, dest)
    print initmsg
    my_alert.send(initmsg)
    params = {'parts.0': model,
              'location': zipcode}
    sec = int(sec)
    i, cnt = 0, sec

    while True:
        if cnt < sec:
            # loading sign refreashes every second
            sys.stdout.write('\rChecking...{}'.format(LOADING[i]))
            sys.stdout.flush()
            i = i + 1 if i < 3 else 0
            cnt += 1
            time.sleep(1)
            continue
        cnt = 0

        try:
            stores = requests.get(URL, params=params) \
                    .json()['body']['stores'][:8]
        except (ValueError, KeyError, gaierror):
            print "Failed to query Apple Store"
            time.sleep(int(sec))
            continue

        for store in stores:
            sname = store['storeName']
            item = store['partsAvailability'][model]['storePickupProductTitle']
            if store['partsAvailability'][model]['pickupDisplay'] \
                        == "available":
                if sname not in good_stores:
                    good_stores.append(sname)
                    msg = u"Found it! {store} has {item}! {buy}{model}".format(
                        store=sname, item=item, buy=BUY, model=model)
                    print u"{0} {1}".format(time.strftime(DATEFMT), msg)
                    my_alert.send(msg)
            else:
                if sname in good_stores:
                    good_stores.remove(sname)
                    msg = u"Oops all {item} in {store} are gone :( ".format(
                        item=item, store=sname)
                    print u"{0} {1}".format(time.strftime(DATEFMT), msg)
                    my_alert.send(msg)

        if good_stores:
            print "[{current}] Avaiable: {stores}".format(
                current=time.strftime(DATEFMT),
                stores=', '.join([s.encode('utf-8') for s in good_stores])
                        if good_stores else "None")

class Alert(object):
    def __init__(self, dest, login=None, password=None):
        self.dest = dest
        if login and password:
            self.login = login
            self.password = password
            self.send = self.send_email
        else:
            self.send = self.send_sms

    def send_email(self, msgbody):
        message = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}".format(
            self.login, self.dest, "Apple Stock Alert", msgbody)
        try:
            mailer = smtplib.SMTP('smtp.gmail.com:587')
        except gaierror:
            print "Couldn't reach Gmail server"
            return
        mailer.ehlo()
        mailer.starttls()
        mailer.ehlo()
        mailer.login(self.login, self.password)
        mailer.sendmail(self.login, self.dest, message)
        mailer.close()

    def send_sms(self, message):
        message = client.messages.create(to=self.dest, from_=smsFrom, body=message)
        

if __name__ == '__main__':
    main(*sys.argv[1:])
