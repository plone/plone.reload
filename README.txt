plone.reload Package Readme
===========================

Overview
--------

ZCML configuration reload without server restarts.

This code is heavily based on the Products.RefreshNG product found at
http://launchpad.net/refreshng.

Usage
-----

While being logged into the ZMI as a Manager user goto /@@zcml_reload on your
Zope application root via a browser. If your Zope is configured to listen on
port 8080 on localhost this is::

  http://localhost:8080/@@zcml_reload

You should see a message::

  Global ZCML reloaded.

Subsequent reloads of this page will reload all global ZCML from all packages
and products each time.

If you get a `Resource not found` error, make sure you have loaded this
packages configure.zcml file and you really use the ZODB application root and
not a Plone site as the base url.
