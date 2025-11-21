from setuptools import setup

version = "5.0.0.dev0"

setup(
    name="plone.reload",
    version=version,
    description="Configuration and code reload without server restarts.",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="zope plone reload",
    author="Hanno Schlichting",
    author_email="hanno@hannosch.eu",
    url="https://pypi.org/project/plone.reload",
    license="BSD",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "zope.component",
        "zope.interface",
        "zope.processlifetime",
        "zope.publisher",
        "zope.site",
        "zope.testing",
        "Zope",
    ],
    extras_require=dict(
        cmf=["Products.CMFCore"],
    ),
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
