plone.reload
============

Overview
--------

Configuration and code reload without server restarts.

This code is heavily based on the Products.RefreshNG product found at
http://launchpad.net/refreshng.

The original xreload.py written by Guido van Rossum can be found at
http://svn.python.org/projects/sandbox/trunk/xreload/xreload.py

It has some enhancements, but those seem to break more code than do any good
in a Zope environment with patched in meta classes and monkey patches all over
the place.

Usage
-----

While being logged into the ZMI as a Manager user goto /@@reload on your
Zope application root via a browser. If your Zope is configured to listen on
port 8080 on localhost this is::

  http://localhost:8080/@@reload

If you get a `Resource not found` error, make sure you have loaded this
packages configure.zcml file and you really use the ZODB application root and
not a Plone site as the base url.

When you press the `Reload Code` button, all modules that have been changed
since the last time they were loaded are reloaded. You'll get a status message
telling you which modules have been reloaded.

To reload all ZCML without a restart, press the 'Reload Code and ZCML' button.

The action to perform is determined via a simple query string, so once you
did a 'Reload Code' once, you can simply reload the browser page to execute
the action once again.
