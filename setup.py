from setuptools import setup

version = '3.0.1.dev0'

setup(
    name='plone.reload',
    version=version,
    description="Configuration and code reload without server restarts.",
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords='zope plone reload',
    author='Hanno Schlichting',
    author_email='hanno@hannosch.eu',
    url='https://pypi.org/project/plone.reload',
    license='BSD',
    packages=['plone', 'plone.reload'],
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'six',
        'zope.component',
        'zope.interface',
        'zope.processlifetime',
        'zope.publisher',
        'zope.site',
        'zope.testing',
        'Zope2 >= 2.13',
    ],
    extras_require=dict(
        cmf=['Products.CMFCore'],
    ),
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
