from setuptools import setup, find_packages

version = '1.6'

setup(name='plone.reload',
      version=version,
      description="Configuration and code reload without server restarts.",
      long_description=open('README.rst').read() + '\n' +
                       open('CHANGES.txt').read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='zope plone reload',
      author='Hanno Schlichting',
      author_email='hanno@hannosch.eu',
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
