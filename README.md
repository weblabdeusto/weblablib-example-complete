# complete

This is a complete example of how to use **weblablib**. It is based on the `advanced` example, but it includes:
 * Flask-SocketIO
 * Flask-Babel (to manage internationalization)
 * Flask-Assets (to manage static files in a single file)

## What does this lab do?

This lab is just a simple laboratory showing ten light bulbs (on which you can click to turn them on and off) and a fake "microcontroller" that you can either send a file that works or one which doesn't.

You can find more documentation in the `advanced` example

## Internationalization

This lab supports multiple languages (only English and Spanish right now). In your Python code, you can put things like:

```python

from flask_babel import gettext, lazy_gettext

# ...

# Outside request
ERROR_MESSAGE = lazy_gettext("This is my error message")

# ...

# Inside request
@app.route('/lab')
@requires_login
def lab():
    # ...
    if error:
       return render_template("error.html", message=gettext("There was an error in the server"))
```

or in your templates:

```jinja
<h1>{{ gettext("Complete laboratory") }}</h1>
```

By default, it will work as if you didn't put ``gettext``/``lazy_gettext`` (returning that string). Then, check the ``babel.cfg`` file (to see that the folder matches your project). Then you can run the following commands:

```shell
# Extract all the messages (this reads all the files and finds any message doing gettext() or similar and stores it in messages.pot)
$ pybabel extract -F babel.cfg -k lazy_gettext -k ng_gettext -o messages.pot --project complete --version 0.1 .

# ONLY FOR NEW LANGUAGES: If you wanted to create a new set of translations for French for example, you would need to run this:
$ pybabel init -i messages.pot -d mylab/translations -l fr

# Once you have run the 'pybabel extract' command, messages.pot will be updated, but not each language. Whenever you
# run this other command, you'll find a folder in mylab/translations/es/LC_MESSAGES/messages.po, which is a text file
# you can edit (or you can use existing tools such as Google Translator Toolkit to edit)
$ pybabel update -i messages.pot -d mylab/translations -l es

# Once you have edited the '.po' file, you can run this command to create a '.mo' file, which is used by Flask automatically
# whenever you restart the Flask application/gunicorn.
$ pybabel compile -f -d mylab/translations
```

And then, depending on the language, it will use one text or another. So as to know which language it should be using, ``weblab_user`` provides a ``locale`` variable which is what the final system stated. Also, you can simply append a ``?locale=`` to the URL or similar. How this is decided is in the ``mylab/__init__.py`` file (search for ``localeselector``).

Check [Flask-Babel](https://pythonhosted.org/Flask-Babel/) for more information on internationalization.

## Assets

[Flask-Assets](https://flask-assets.readthedocs.io/) is a powerful library for managing static files such as CSS or JavaScript.

In all the examples, we use public CDNs (Content Delivery Network), which are external servers that provides contents; in our case, providing popular open source libraries such as [Bootstrap](http://getbootstrap.com/), [jQuery](https://jquery.com/) or [socket.io](https://socket.io/).

However, in your case, you might want to download the libraries and share them in your static folder. Once you do it, you may want to use Flask-Assets to put all of them together in a single static file, and do the same with your code in a separate file, by putting this in your Jinja templates:

```jinja
{% assets filters="cssmin", output='gen/vendor.min.css',
                           'css/bootstrap.css' %}
<link rel="stylesheet" href="{{ ASSET_URL }}">
{% endassets %}
{% assets filters="cssmin", output='gen/app.min.css',
                           'css/app.css' %}
<link rel="stylesheet" href="{{ ASSET_URL }}">
{% endassets %}

<!-- later on -->

{% assets filters="jsmin", output='gen/vendor.min.js',
                           'vendor/jquery.js',
                           'vendor/bootstrap.js',
                           'vendor/socketio.js' %}
<script src="{{ ASSET_URL }}"></script>
{% endassets %}
{% assets filters="jsmin", output='gen/app.min.js',
                           'js/lab.js' %}
<script src="{{ ASSET_URL }}"></script>
{% endassets %}
```

If you run this code, it will generate in the ``static/gen`` folder a set of files (``vendor.min.css``, ``app.min.css``, ``vendor.min.js`` and ``app.min.js``), and when displaying your template on the web browser, you will see something like the following:

```html
<link rel="stylesheet" href="/static/gen/vendor.min.css?0bddf6cd">
<link rel="stylesheet" href="/static/gen/app.min.css?cd0bddf6">

<!-- later on -->

<script src="/static/gen/vendor.min.js?f6cd0bdd"></script>
<script src="/static/gen/app.min.js?ddf6cd0b"></script>
```

This has several advantages:
 1. It generates files that the web browser can safely cache. You can put in the web server a strict policy on the ``static`` directory. Whenever there is any change, Flask will generate a different file, and the URL will be different (since the ``?ddf6cd0b`` is a hash of the contents), so the web browser will load the new version. The separation of ``vendor`` (external libraries) and ``app`` (your code) is also relevant for this: typically you change your code more often that your libraries; and your code is typically smaller than the libraries. So recurring users' web browsers will have cached both the ``vendor`` and ``app`` files, and if you make an update, they will only have to re-download the ``app`` one.
 1. You reduce substantially the number of files that the web browser has to download and the overhead per connection, as well as the size of the files and the loading time by the web browser.

However, in the example code you will only find it used once, since as we mentioned, we use CDNs:
```jinja
{% assets filters="jsmin", output='gen/app.min.js',
                           'js/lab.js' %}
<script src="{{ ASSET_URL }}"></script>
{% endassets %}
```

The main disadvantage of using this mechanism is that when you're developing and there is an error, it's difficult to find out why or where (since the code was minified). For this reason, there is a configuration variable called ``ASSETS_DEBUG``. In our example, in Development, by default is ``False``; but you can activate it by putting:

```shell
 $ export ASSETS_DEBUG=1
 $ python run_debug.py
```

Or by changing the ``config.py`` file to be always ``True`` on Development.

Check more information on [Flask-Assets](https://flask-assets.readthedocs.io/).

## Deployment

### Install the dependencies

You will need to create a virtual environment, and then install all the requirements:

```shell

 $ pip install -r requirements.txt
```

If you are running ``Python 2``, install also:

```shell
 $ pip install gevent-websocket
```

### Running it for development

So as to run it, in Linux / Mac OS X:

```shell

 $ python run_debug.py

```

Alternatively, you can do also:
```shell
 $ python run_debug.py
```

Since ``localrc`` already contains those variables.

In Microsoft Windows:
```shell
 C:\...\> python run_debug.py
```

Additionally, you must run in other terminal:
```shell
 $ export FLASK_DEBUG=1
 $ export FLASK_APP=autoapp.py
 $ flask weblab loop
```

or in Windows:

```shell
 C:\...\> set FLASK_DEBUG=1
 C:\...\> set FLASK_APP=autoapp.py
 C:\...\> flask weblab loop
```


And you can test it using [WebLab-Deusto](https://weblabdeusto.readthedocs.org) or using the weblablib command line interface in other terminal:

```shell

 $ export FLASK_APP=autoapp.py # (or . localrc)
 $ flask weblab fake new --locale es
```

### Running it for production environments

In a production environment, you must use a proper server such as `gunicorn`. To do this:

```shell

pip install gunicorn

```

Then, you have to have a file such as `wsgi_app.py`. Important: change all the values there (e.g., `WEBLAB_PASSWORD`, `SECRET_KEY`, etc.).

Once you change it, you can run a script like `gunicorn_start.sh`. Furthermore, this script is prepared to be launched from [supervisor](http://supervisord.org/).

Finally, you have further information on WebLab-Deusto for unmanaged servers [in the official documentation](http://weblabdeusto.readthedocs.io/en/latest/#remote-laboratory-development-and-management).



# Developing with Docker

Docker can be used to start developing in a particularly fast way, without needing to set a development environment in your own machine.

## Setting up the environment

- Install git.
- Install the community version of docker.
- Clone this repository somewhere.

## Run the lab server

The laboratory server for development can be run from Docker. Docker will run all the dependencies (Python, the virtual env, etc.).
The source code, however, will be located in a local folder in your machine, so that you can change it easily. Just go to the folder
where you have cloned this repository, and run:

```docker-compose up```

This will build the docker images, and run the containers that are needed. The laboratory server will be listening in your local port 5000, so you could simply go to http://localhost:5000 with your browser. Note, however, that you will get redirected out, because
a fake session will not be ready.

## Try the lab server

To try the lab server you need to start a fake session. A fake session simply involves simulating that a student has
entered your laboratory, so that you can test that everything works as expected. To do so, run:

```docker-compose exec lab flask weblab fake new --assigned-time 3600```

That command will connect to the docker container and run the command to simulate a user, assigning a maximumt ime of 3600 seconds.
The output should be an URL similar to: http://localhost:5000/callback/5HRFqybZe_Is4cXeNMBtsG0i1HOv34jFBUuvgMKmbRw

You should be able to open it in your browser, and test your lab.

## Developing your lab

Simply modify your local source code, and the changes should take place automatically. Run the previous command to simulate
new users to test it.

## Turning the lab off

To turn the docker containers off after you're done developing, just run:

```docker-compose down```

## Running other commands

To run 'weblab' management commands as in other sections of the doc, you can simply do:

```docker-compose exec lab flask weblab``

(and add parameters as needed).

Likewise, if you want to enter the docker container itself in case you need to check what is going on, you can:

```docker-compose exec lab bash```

