from setuptools import setup

version = '2.0.2'

setup(
    name='plone.reload',
    version=version,
    description="Configuration and code reload without server restarts.",
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
      ],
    keywords='zope plone reload',
    author='Hanno Schlichting',
    author_email='hanno@hannosch.eu',
    url='https://pypi.python.org/pypi/plone.reload',
    license='BSD',
    packages=['plone', 'plone.reload'],
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.component',
        'zope.interface',
        'zope.processlifetime',
        'zope.publisher',
        'zope.site',
        'zope.testing',
        'Zope2 >= 2.12',
    ],
    extras_require=dict(
      cmf=['Products.CMFCore'],
    ),
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
    )
