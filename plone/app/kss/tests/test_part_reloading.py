import unittest
from Products.PloneTestCase import PloneTestCase

from kss.core.events import AzaxEvent
from kss.core.tests.base import AzaxViewTestCase

import plone
from plone.app.kss.azaxview import AzaxBaseView
from plone.app.kss.interfaces import IPortalObject
from plone.app.kss.portlets import navigation_portlet_reloader
from plone.app.kss.tests.layer import PloneKSS

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


class TestPortletReloading(PloneTestCase.PloneTestCase, AzaxViewTestCase):

    layer = PloneKSS

    def afterSetUp(self):
        PloneTestCase.PloneTestCase.afterSetUp(self)
        self.loadCoreConfig(kss_core=False)
        self.setDebugRequest()
        self.loginAsPortalOwner()
        self.setRoles(['Manager',])
        # register the sample view
        load_config('configure-part_reloading.zcml', package=plone.app.kss.tests)
        self.view = self.portal.restrictedTraverse('@@change_title')

    def test_no_update_of_nav_portlet_when_unhooked(self):
        # nothing should happen
        result = self.view.render()
        self.assertEqual(result, [])

    def test_no_update_of_nav_portlet_when_hooked_with_wrong_event(self):
        # nothing should happen still because we must change the title or the
        # description
        modified_event = ObjectEditedEvent(self.folder)
        azax_event = AzaxEvent(self.view, modified_event)
        navigation_portlet_reloader(azax_event)
        result = self.view.render()
        self.assertEqual(result, [])

    def test_update_of_nav_portlet(self):
        descriptor = lifecycleevent.Attributes(IPortalObject, 'title')
        modified_event = ObjectEditedEvent(self.folder, descriptor)
        azax_event = AzaxEvent(self.view, modified_event)
        navigation_portlet_reloader(azax_event)
        result = self.view.render()

        self.assertEqual(result[0]['selector'], '#portlet-navigation-tree')


def test_suite():
    suites = []
    suites.append(unittest.makeSuite(TestPortletReloading))
    return unittest.TestSuite(suites)
