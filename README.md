# zzzz

zzzz.io was a website providing free dynamic DNS subdomains.

It existed from 2014 - 2019. I threw it together in a weekend, hacking to get something up and running, not to create something beautiful, so the resulting code smells pretty bad and important engineering practices (e.g. testing) were ignored.

The only reason I'm making this code available here is that there've been multiple requests from old users of the service to open-source it. So, here you go. 

## Warning

This is provided as-is. I'm responsible for no harm that comes from using it. For more details, see the license in `LICENSE.md`. 

(e.g. before going anywhere near this, you should probably upgrade the dependencies in `requirements.txt` .....)

## Running

* Clone the repo
* Create a virtualenv and enter it, then:

```
cd zzzz
pip install -e .
DJANGO_SETTINGS_MODULE=zzzz.settings.dev python manage.py runserver
```

* This will run the django webserver using the settings in `zzzz/settings/dev.py` (not to be used for production)

If you're sticking it behind a webserver, you can use the `wsgi.py` module.

## Getting help

Sorry, I don't support this code. Please don't contact me about it asking for help. You'll most likely find the answer to any question you may have by Googling.
