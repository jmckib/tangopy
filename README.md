# tangopy
A simple python wrapper of TangoCard's RaaS API.

See https://github.com/tangocarddev/RaaS

Make sure you set up a virtualenv and install requirements.

```
cd tangopy
virtualenv venv
pip install -r requirements.txt
```

I wrote this in about an hour, and it doesn't include every single API call, but hopefully it will save you some time.

Note this doesn't do anything with the `system_message` field mentioned here:
https://github.com/tangocarddev/RaaS#system-wide-notes
