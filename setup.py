import os

from setuptools import setup, find_packages

name = 'plone.reload'
version = '1.2'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description=(
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
    )

setup(name=name,
      version=version,
      description="Configuration and code reload without Zope server restarts.",
      long_description=long_description,
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='Zope Plone reload',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.reload',
      license='GPL',
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
        cmf = ['Products.CMFCore'],
      ),
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
