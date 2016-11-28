import os
import sys
import site

# Virtualenv location (default: None)
#virtualenv = '/home/chris/code/pythonenv'
virtualenv = None

# App's root ../
app_root = (os.path.abspath(os.path.join(
                            os.path.dirname(__file__),
                            '..')))

# Change current working directory to App's root
os.chdir(app_root)

# Add the app's directory to the PYTHONPATH
sys.path.append(app_root)

# Virtualenv
if virtualenv is not None:
    # Add the site-packages of the chosen virtualenv to work with
    virtualenv = virtualenv.rstrip('/')
    site.addsitedir("%s/lib/python2.7/site-packages" % (virtualenv,))
	# Activate your virtualenv
    activate_env="%s/bin/activate_this.py" % (virtualenv,)
    execfile(activate_env, dict(__file__=activate_env))

# Configuration File
config = (os.path.abspath(os.path.join(
                          os.path.dirname(__file__),
                          '../settings.yaml')))
os.environ['NEUTRINO_CONFIG'] = str(config)

os.environ['PYTHON_EGG_CACHE'] = "%s/tmp/.cache/Python-Eggs" % (app_root)

# Initialize WSGI Object
import nfw
nfw_wsgi = nfw.Wsgi()

# LETS GET THIS PARTY STARTED...
application = nfw_wsgi.application()

