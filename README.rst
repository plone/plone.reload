Overview
--------

Configuration and code reload for Zope 2 and Plone without server restarts.

Usage
-----

While being logged into the ZMI as an user with the Manager role visit
``/@@reload`` on your Zope application root via a browser. If your Zope is
configured to listen on port 8080 on localhost this is::

  http://localhost:8080/@@reload

If you get a `Resource not found` error, make sure you have loaded the
`configure.zcml` file from this library and you really use the ZODB application
root and not a Plone site as the base url.

When you press the `Reload Code` button, all modules that have been changed
since the last time they were loaded are reloaded. You'll get a status message
telling you which modules have been reloaded.

To reload all ZCML without a restart, press the 'Reload Code and ZCML' button.

The action to perform is determined via a simple query string, so once you
did a 'Reload Code' once, you can simply reload the browser page to execute
the action once again.

Caveats: There's some code structures which cannot be reloaded via the
approach underlying this library. Plone portlets and content types are two
examples of this. In general decorators will currently not always work.

Development
-----------

The code and issue tracker can be found on GitHub at:
https://github.com/plone/plone.reload

Thanks
------

This code is heavily based on the `Products.RefreshNG` product found at
http://launchpad.net/refreshng.

The original `xreload.py` written by Guido van Rossum can be found at
``http://svn.python.org/projects/sandbox/trunk/xreload/xreload.py``

It has some enhancements, but those seem to break more code than do any good
in a Zope environment with patched in meta classes and monkey patches all over
the place.

Contributors
------------

* Hanno Schlichting (primary author)
* Martin Aspeli (test contribution)
