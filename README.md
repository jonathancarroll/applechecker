# applechecker

> Check Apple Store Inventory +With Twilio Support

Keep checking Apple Store inventory and send you alert when nearby stores have your desired device in stock.
Also let you know if inventory becomes zero again so you don't jump out of bed when it is already too late.

* [Prerequisites](#prerequisites)
* [Usage](#usage)

## Prerequisites

* `pip install requests`
* `pip install twilio`

* A gmail account if want email alert. (Got refused by Gmail because the app is insecure? [Enable 2-Step Verification](https://support.google.com/accounts/answer/185839?hl=en) and [generate an App password]() for it. Or follow [this instruction](https://support.google.com/accounts/answer/6010255?hl=en) to allow insecure login)

* For SMS alert, the script uses the service provided by [Twilio](http://twilio.com/), you will need to create an account and set the appropriate variables in the python script.  Be sure to include +1 in front of your phone numbers (for USA numbers) with Twilio.

Make sure and set these variables in stock.py

* `account = "ACCOUNTIDGOESHERE"`
* `token = "TOKENGOESHERE"`
* `smsFrom = "+15554443333"`

## Usage

```
python stock.py <model> <zipcode> <emails or phone numbers delimited by comma> <check interval in seconds> <your gmail account if you want email alerts> <your gmail password if you want email alerts>
```

### Example:

Every 5 seconds, check availability of `Apple Watch Stainless Steel Case with White Sport Band` near zipcode 12345 and send email alert to `recipient@example.com` using gmail account `sender@gmail.com`.

```
python /path/to/stock.py "MNPR2LL/A" "12345" "recipient@example.com" 5 sender@gmail.com sender_password
```

Every 10 seconds, check availability of `iPhone 7 Plus T-Mobile Jet Black 128GB` near zipcode 12345 and send sms alert to `1234567890`.

```
python /path/to/stock.py "MN5L2LL/A" "12345" "+11234567890" 10
```

Model number is a unique identifier, U.S. models end with "LL/*". (https://www.theiphonewiki.com/wiki/Model_Regions)

* For Apple Watch: model number hides in query string in URL of the item page.

    Example:
    `http://www.apple.com/shop/buy-watch/apple-watch/silver-stainless-steel-stainless-steel-sport-band?preSelect=true&product=`**`MNPR2LL/A`**`&step=detail#`

* iPhone: inspect the item page and look for a request to `http://www.apple.com/shop/delivery-message?`

    Example:
    `http://www.apple.com/shop/delivery-message?parts.0=`**`MN5L2LL%2FA`**`&cppart=TMOBILE%2FUS&_=1474171709609`

    or just check your model number here: http://www.everyi.com/

To verify, visit `http://store.apple.com/xc/product/<model numer>` and see if it shows the product you want.

### Docker Example:

```
docker run --name my-checker-email -e MODEL="MN5L2LL/A" -e ZIP=12345 -e DEST=recipient@example.com -e SEC=1 -e LOGIN=sender@gmail.com -e PASS=sender_password yuha0/applechecker
```

```
docker run --name my-checker-sms -e MODEL="MNPR2LL/A" -e ZIP="12345" -e DEST="+11234567890" -e SEC=5 yuha0/applechecker
```
