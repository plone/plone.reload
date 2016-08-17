Changelog
=========

2.0.2 (2016-08-18)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


2.0.1 (2016-02-11)
------------------

Fixes:

- Minor packaging fixes.  [gforcada, maurits]


2.0 (2011-06-04)
----------------

- Update test assertions to avoid deprecation warnings under Python 2.7.
  [hannosch]

- Relicensed to BSD.
  [hannosch]

- Minor PEP8 cleanup.
  [hannosch]

- Exclude tests from the shipped source distribution.
  [hannosch, iElectric]

2.0b1 (2011-04-03)
------------------

- Require at least Zope 2.12 / Python 2.6 and add preliminary support for
  Zope 2.13 with Python 2.6 and 2.7.
  [hannosch]

1.5 (2010-07-18)
----------------

- Update license to GPL version 2 only.
  [hannosch]

1.4 (2010-05-27)
----------------

- Fixed some tests that relied on a specific directory layout.
  [hannosch]

- Fixed a bug in dealing with class descriptors, like Five's BoundTemplateFile.
  We replaced the descriptor with the descriptor result, leading to strange
  problems. We check for those by looking directly into the ``__dict__`` and
  comparing it to the result of a normal ``getattr`` call.
  [hannosch, optilude]

1.3 (2010-01-16)
----------------

- Use a different hook for providing the initial setup of tracked code files.
  In Zope 2.12+ there's a proper event published right before the process has
  started. If this is available we use it, instead of our no longer working
  approach to hook ``setupFinalLogging``.
  [hannosch]

1.2 (2009-11-21)
----------------

- Moved the template reloading support into an extra.
  [hannosch]

- Added test_suite functions to the test modules.
  [hannosch]

1.1 (2009-10-19)
----------------

- Added CMF specific functionality: We support explicitly reloading all file
  system based objects from skins folders while running in production mode.
  [hannosch]

1.0 (2009-10-11)
----------------

- Avoid the `ENABLED` config flag and check against Globals.DevelopmentMode in
  the browser view.
  [hannosch]

- Make sure the import of the Globals module happens after the variable has
  been set. This should make it compatible with Zope 2.10.9+.
  [hannosch]

1.0b1 (2009-08-11)
------------------

- Got the test coverage for the code reloading part up to 100%.
  [hannosch]

- Fixed reloading of the module scope. The func_globals of functions is now
  updated with new names introduced into the module scope, so adding new
  import statements will work.
  [hannosch]

- Specified package dependencies, added development buildout and added
  extensive test coverage.
  [hannosch]

- Figured out a way to support reloading code that uses decorators.
  [hannosch]

0.11 (2009-05-30)
-----------------

- Added the z3c.autoinclude entry point so that plone.reload is automatically
  loaded on Plone 3.3 and above.
  [optilude]

0.10 (2009-03-22)
-----------------

- Do not remove attributes from classes when reloading. ZCML directives and
  other wiring is liable to add attributes to class that will then disappear
  on reload. This means that if you have removed a class attribute, it will
  *not* disappear on reload. In this case: restart. :)
  [optilude]


0.9 (2008-07-23)
----------------

- Removed the manual cleanup approach for extra registries populated by ZCML
  parsing. Instead we use the registry of cleanup functions inside
  zope.testing.cleanup to automatically pick up all cleaning functions.
  [hannosch]

0.8 (2008-06-30)
----------------

- Wrap the setupFinalLogging method of the Zope2 starter objects to initialize
  our internal modified times registry once after Zope is finished loading.
  This is the closest I could find that resembles a `Zope is finished loading`
  event and should help to remove the double-reload behavior.
  [hannosch]

- Only expose the reload view in Zope 2 development mode.
  [hannosch]

- In case of errors during ZCML reload, restore the original global site
  manager state, instead of leaving it in a broken state. This allows you to
  fix and retry the ZCML reload as many times as you need.
  [hannosch]

0.7 (2008-06-17)
----------------

- Merged the two distinct views into one called @@reload. Added a somewhat
  nicer UI to it and explain some of the current limitations on that page.
  [hannosch]

- Refactored ZCML loading code a bit. Always do an automatic code reload
  before reloading ZCML.
  [hannosch]

- Removed all blacklisting code.
  [hannosch]

0.6 (2008-06-11)
----------------

- Disabled blacklist until it can be made configurable. The speedup is hardly
  noticeable anyway, and it can block too much (especially if plone.reload
  is being used in a lib/python style deployment rather than as an egg).
  [optilude]

0.5 (2008-05-24)
----------------

- Merged r20 from http://bazaar.launchpad.net/~refreshng-dev/refreshng/dev.
  This fixes https://bugs.launchpad.net/refreshng/+bug/175898.
  [hannosch]

- Removed various levels of caching which turned out to be premature and
  caused lots of modules not to be found.
  [hannosch]

0.4 (2008-03-01)
----------------

- Made the code reload available as its own @@code_reload view.
  [hannosch]

- Integrated xreload.py from RefreshNG and added a first working version of a
  general manual code reload feature.
  [hannosch]

0.3 (2008-02-21)
----------------

- Fixed caching issues by invalidating all ZODB caches. If you have local site
  managers spread across multiple FileStorages this might still not work as
  expected.
  [hannosch]

- Added cleanup for CMFCore and PAS.
  [hannosch]

0.2 (2008-01-25)
----------------

- Added compatibility with Zope 2.10 / Plone 3.0.
  [hannosch]

0.1 (2008-01-25)
----------------

- Initial implementation based heavily on Products.RefreshNG.
  [hannosch]

- Initial package structure.
  [zopeskel]
