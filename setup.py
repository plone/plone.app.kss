from setuptools import setup, find_packages

version = '1.7.0'

setup(name='plone.app.kss',
      version=version,
      description="KSS (Kinetic Style Sheets) for Plone",
      long_description=open("README.txt").read() + "\n" +
          open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.kss',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'Products.PloneTestCase',
        ]),
      install_requires=[
        'setuptools',
        'kss.core',
        'plone.portlets>=2.0.1dev',
        'plone.app.layout',
        'plone.app.portlets',
        'plone.locking',
        'zope.component',
        'zope.contentprovider',
        'zope.deprecation',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.viewlet',
        'Acquisition',
        'Products.Archetypes',
        'Products.CMFCore',
        'Products.DCWorkflow',
        'Products.statusmessages',
        'Zope2',
      ],
      )
