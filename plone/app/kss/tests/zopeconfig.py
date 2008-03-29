
from kss.demo.interfaces import (
    IKSSDemoResource,
    IKSSSeleniumTestResource,
    )
from kss.demo.resource import (
    KSSSeleniumTestSuite,
    KSSSeleniumTestDirectory,
    KSSSeleniumTestLayerBase,
    KSSSandboxCreationTestCase,
    KSSSeleniumTestCaseList,
    KSSSeleniumTestCase,
    )
from zope.interface import implements
     
# Create a mesh of provided interfaces
# This is needed, because an utility must have a single interface.
class IResource(IKSSDemoResource, IKSSSeleniumTestResource):
    pass


class PloneSiteLayer(KSSSeleniumTestLayerBase):
    setup = KSSSandboxCreationTestCase('@@kss_test_create_site')

class LoggedInManagerLayer(PloneSiteLayer):
    setup = KSSSeleniumTestCaseList(KSSSandboxCreationTestCase('@@kss_test_create_site'),
            KSSSeleniumTestCase('log-in-manager.html'))
    teardown = KSSSeleniumTestCase('log-out.html')

class PloneDemos(object):
    implements(IResource)

    selenium_tests = (
        KSSSeleniumTestSuite(
            tests = KSSSeleniumTestDirectory('selenium_tests'),
            layer = PloneSiteLayer,
            component = 'plone.app.kss',
            application = 'Plone',
            ),
        KSSSeleniumTestSuite(
            tests = KSSSeleniumTestDirectory('selenium_tests/run_as_testmanager'),
            layer = LoggedInManagerLayer,
            component = 'plone.app.kss',
            application = 'Plone',
            ),

        )
