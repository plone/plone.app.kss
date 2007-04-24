import unittest
from Products.PloneTestCase import PloneTestCase

import plone
from plone.app.kss.azaxview import AzaxBaseView
from plone.app.kss.interfaces import IPortalObject
from plone.app.kss.portlets import attributesTriggerNavigationPortletReload
from plone.app.kss.portlets import attributesTriggerRecentPortletReload
from plone.app.kss.tests.kss_and_plone_layer import KSSAndPloneTestCase

from zope.lifecycleevent import ObjectModifiedEvent
from zope import lifecycleevent

from Products.Archetypes.event import ObjectEditedEvent
from Products.Five.zcml import load_config

PloneTestCase.setupPloneSite()

class SampleView(AzaxBaseView):

    def change_title(self, title):
        # normally you would change the zope database here
        self.handle(ObjectModifiedEvent(self.context))
        return self.render()


class TestPortletReloading(KSSAndPloneTestCase):
    class layer(KSSAndPloneTestCase.layer):
        @classmethod
        def setUp(cls):
            load_config('configure-part_reloading.zcml',
                        package=plone.app.kss.tests)            

    def afterSetUp(self):
        PloneTestCase.PloneTestCase.afterSetUp(self)
        self.setDebugRequest()
        self.loginAsPortalOwner()
        self.setRoles(['Manager',])
        # register the sample view

        self.view = self.portal.restrictedTraverse('@@change_title')

    def test_no_update_of_nav_portlet_when_unhooked(self):
        # nothing should happen
        result = self.view.render()
        self.assertEqual(result, [])

    def test_no_update_of_nav_portlet_when_hooked_with_wrong_event(self):
        # nothing should happen still because we must change the title or the
        # description
        modified_event = ObjectEditedEvent(self.folder)
        attributesTriggerNavigationPortletReload(self.folder, self.view, modified_event)
        result = self.view.render()
        self.assertEqual(result, [])

    def test_update_of_nav_portlet(self):
        descriptor = lifecycleevent.Attributes(IPortalObject, 'title')
        modified_event = ObjectEditedEvent(self.folder, descriptor)
        attributesTriggerNavigationPortletReload(self.folder, self.view, modified_event)
        result = self.view.render()
        command = result[0]
        self.failUnless(command.has_key('selector'))
        self.failUnless(command['selector'].startswith('portletwrapper'))
        self.failUnless(command.has_key('name'))
        self.assertEqual(command['name'], 'replaceInnerHTML')
        self.failUnless(command.has_key('params'))
        params = result[0]['params']
        self.failUnless(params.has_key('html'))
        html = params['html']
        self.failUnless('portletNavigationTree' in html)
        self.failUnless(command.has_key('selectorType'))
        self.assertEqual(command['selectorType'], 'htmlid')

    def test_update_of_recent_portlet(self):
        descriptor = lifecycleevent.Attributes(IPortalObject, 'title')
        modified_event = ObjectEditedEvent(self.folder, descriptor)
        attributesTriggerRecentPortletReload(self.folder, self.view, modified_event)
        result = self.view.render()
        command = result[0]
        self.failUnless(command.has_key('selector'))
        self.failUnless(command['selector'].startswith('portletwrapper'))
        self.failUnless(command.has_key('name'))
        self.assertEqual(command['name'], 'replaceInnerHTML')
        self.failUnless(command.has_key('params'))
        params = result[0]['params']
        self.failUnless(params.has_key('html'))
        html = params['html']
        self.failUnless('portletRecent' in html)
        self.failUnless(command.has_key('selectorType'))
        self.assertEqual(command['selectorType'], 'htmlid')

def test_suite():
    suites = []
    suites.append(unittest.makeSuite(TestPortletReloading))
    return unittest.TestSuite(suites)
