from setuptools import setup, find_packages

version = '1.6.0a3'

setup(name='plone.app.kss',
      version=version,
      description="KSS (Kinetic Style Sheets) for Plone",
      long_description=open("README.txt").read() + "\n" +
          open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://plone.org',
      license='GPL',
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
        'plone.portlets',
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
        'Products.Archetypes',
        'Products.CMFCore',
        'Products.DCWorkflow',
        'Products.statusmessages',
        # 'Acquisition',
        # 'Zope2',
      ],
      )
