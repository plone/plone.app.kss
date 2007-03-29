from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from kss.core.BeautifulSoup import BeautifulSoup

ZOPE_DEPS = []
PLONE_DEPS = []
#ZOPE_DEPS = ['MyZopeProductDependecy']
#PLONE_DEPS = ['MyPloneProduct',
#              'MyPloneDependency']

for x in ZOPE_DEPS + PLONE_DEPS:
    ztc.installProduct(x)
ptc.setupPloneSite(products=PLONE_DEPS)

class TestForKSSInlineEditing(ptc.FunctionalTestCase):
    """
    Ok, this is a strange case of doctest: actually, we are able to use
    self inside the doctests, but the import stuff is still quite broken,
    hence the abundance of function that do just one libne of code or so
    (take a look at Daniel Nouri's blog for more details)
    """
    
    
    def setupTest(self):
        self.folder.invokeFactory('Document', 'page')
        self.page = self.folder.page
        self.page.setTitle('My title')
        self.page.setDescription('My description')
        self.page.setText('<p>My text</p>')
        self.user = ptc.default_user
        self.password = ptc.default_password
    
    def makeSoup(self, html):
        soup = BeautifulSoup(html)
        return soup
    
    def test_notLogged():
        r"""
        
        We import some stuff, else we're not gonna go anywhere
        cause the import is more broken than Saddam's neck
        
          >>> from Products.Five.testbrowser import Browser
        
        We setup the testing environment
        
          >>> self.setupTest()
        
        We call the page
        
          >>> browser = Browser(self.page.absolute_url())
          >>> soup = self.makeSoup(browser.contents)
        
        We find the title tag
        
          >>> title = soup.find('h1', attrs = { 'id': 'parent-fieldname-title' })
          >>> self.failUnless(title)
        
        We see that the KSS hooks shouldn't be there because we're not logged in!
        
          >>> self.failIf('kssattr-atfieldname-' in title['class'])
          >>> self.failIf('kssattr-templateId-' in title['class'])
          >>> self.failIf('kssattr-macro-' in title['class'])
        """

    def test_logged():
        r"""
        
        All the usual setup
        
          >>> from Products.Five.testbrowser import Browser
          >>> self.setupTest()
        
        Okay, we don't go straight away for the page but we actually do authenticate
        
          >>> browser = Browser()
          >>> browser.addHeader('Authorization', 'Basic %s:%s' % (self.user, self.password))
          >>> browser.open(self.page.absolute_url())
          >>> soup = self.makeSoup(browser.contents)
        
        We find the title
        
          >>> title = soup.find('h1', attrs = { 'id': 'parent-fieldname-title' })
          >>> self.failUnless(title)
        
        We check everything is in now, especially that kssattr-fieldname- matched the right field,
        and is not only there, but actually makes some sense
        
          >>> self.failUnless('kssattr-atfieldname-title' in title['class'])
          >>> self.failUnless('kssattr-templateId-' in title['class'])
          >>> self.failUnless('kssattr-macro-' in title['class'])
        
        Rerun, description now! (which is not a Francis Ford Coppola's movie)
        
          >>> title = soup.find('p', attrs = { 'id': 'parent-fieldname-description' })
          >>> self.failUnless(title)
          >>> self.failUnless('kssattr-atfieldname-description' in title['class'])
          >>> self.failUnless('kssattr-templateId-' in title['class'])
          >>> self.failUnless('kssattr-macro-' in title['class'])
        
        Now, time for the text
        
          >>> title = soup.find('div', attrs = { 'id': 'parent-fieldname-text' })
          >>> self.failUnless(title)
          >>> self.failUnless('kssattr-atfieldname-text' in title['class'])
          >>> self.failUnless('kssattr-templateId-' in title['class'])
          >>> self.failUnless('kssattr-macro-' in title['class'])
        """

def test_suite():
    suite = ztc.FunctionalDocTestSuite(test_class=TestForKSSInlineEditing)
    suite.layer = PloneSite
    return suite