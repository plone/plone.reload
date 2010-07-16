from setuptools import setup, find_packages

version = '1.5'

setup(name='plone.reload',
      version=version,
      description="Configuration and code reload without server restarts.",
      long_description=open('README.txt').read() + '\n' +
                       open('CHANGES.txt').read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='Zope Plone reload',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.reload',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.component',
          'zope.interface',
          'zope.testing',
          'Acquisition',
          'Zope2',
      ],
      extras_require = dict(
        cmf=['Products.CMFCore'],
      ),
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
