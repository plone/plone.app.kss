# -*- coding: UTF-8 -*-
# Copyright (c) 2006
# Authors:
#   David '/dev/null' Convent  <davconvent@gmail.com>
#   Daniel 'import pdb' Nouri
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

import unittest
from Products.PloneTestCase import PloneTestCase
from kss.core.tests.base import AzaxViewTestCase

PloneTestCase.setupPloneSite()

from plone.app.kss import content_replacer

class ContentActionMenusTestCase(PloneTestCase.PloneTestCase, AzaxViewTestCase):

    def afterSetUp(self):
        PloneTestCase.PloneTestCase.afterSetUp(self)
        self.loadCoreConfig(kss_core=False)
        # commands will be rendered as data structures,
        self.setDebugRequest()
        self.loginAsPortalOwner()
        self.fpage = self.portal['front-page']

    # --
    # test the Kss methods
    # --

    def testReplaceContentRegion(self):
        req = self.portal.REQUEST
        view = content_replacer.ContentView(self.fpage, req)
        result = view.replaceContentRegion('contentview-edit', self.fpage.absolute_url())
        self.assertEqual([(r['name'], r['selector'], r['selectorType']) for r in result],
            [('replaceHTML', 'region-content', 'htmlid'),
            ('setAttribute', 'ul.contentViews li', 'css'),
            ('setAttribute', 'contentview-edit', 'htmlid')]
            )

    def testChangeViewTemplate(self):
        # Let's set the default page on front-page,
        # should set default layout of portal
        req = self.portal.REQUEST
        self.assertEqual(self.portal.getLayout(), 'folder_listing')
        view = content_replacer.ContentView(self.fpage, req)
        url = self.fpage.absolute_url() + '?templateId=atct_album_view'
        result = view.changeViewTemplate(url)
        self.assertEqual(self.portal.getLayout(), 'atct_album_view')
        
        resh = req.RESPONSE.headers
        self.assertEqual(resh['status'], '200 OK')
        self.failUnless(req.RESPONSE.cookies['statusmessages'].has_key('expires'), 'cookies not expired')

    def testKukitCutObject(self):
        req = self.portal.REQUEST
        view = content_replacer.ContentView(self.fpage, req)
        result = view.cutObject()

        self.assertEqual([(r['name'], r['selector'], r['selectorType']) for r in result],
                         [('replaceHTML', 'div#content div.contentActions', 'css'),
                          ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
                          ('setStyle', 'kssPortalMessage', 'htmlid')]
            )

    def testCutObject(self):
        req = self.portal.REQUEST
        self.failIf(req.RESPONSE.cookies.has_key('__cp'), 'has cut cookie')
        view = content_replacer.ContentView(self.fpage, req)
        result = view.cutObject()
        resh = req.RESPONSE.headers
        self.assertEqual(resh['status'], '200 OK')
        self.failUnless(req.RESPONSE.cookies.has_key('__cp'), 'no cut cookie')
        
    def testKukitCopyObject(self):
        req = self.portal.REQUEST
        view = content_replacer.ContentView(self.fpage, req)

        result = view.copyObject()
        self.assertEqual([(r['name'], r['selector'], r['selectorType']) for r in result],
                         [('replaceHTML', 'div#content div.contentActions', 'css'),
                          ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
                          ('setStyle', 'kssPortalMessage', 'htmlid')]
            )

    def testCopyObject(self):
        req = self.portal.REQUEST
        self.failIf(req.RESPONSE.cookies.has_key('__cp'), 'has copy cookie')
        view = content_replacer.ContentView(self.fpage, req)
        result = view.copyObject()
        resh = req.RESPONSE.headers
        self.assertEqual(resh['status'], '200 OK')
        self.failUnless(req.RESPONSE.cookies.has_key('__cp'), 'no copy cookies')

    def beforeTearDown(self):
        # Overwrite AzaxViewTestCase's method as it tears down the CA manually
        # and doesn't use layers yet, which doesn't play nicely with layer
        # enabled tests.
        pass


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ContentActionMenusTestCase),
        ))

