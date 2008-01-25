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

Reloading this page will reload all global ZCML from all packages and products.
