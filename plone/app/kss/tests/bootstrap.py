try:
    from Products.Five import BrowserView
    from kss.demo.simplecontent import SimpleContent
    BrowserView = BrowserView   # satisfy pyflakes
except ImportError:
    from zope.publisher.browser import BrowserView
    from kss.demo.simplecontent_z3 import SimpleContent

KSSDEMO_NAME = 'demo'
ZUITE_NAME = 'zuite'

class Bootstrap(BrowserView):
    """A very simple view that creates a zuite and a kss.demo object"""

    def createZuite(self, context):
        """creates the zuite. I need context to be passed as
        parameter because putting it in self will screw up...
        guess what? Acquisition"""
        zuite_factory = context.manage_addProduct['Zelenium']
        if hasattr(context, ZUITE_NAME):
            context.manage_delObjects([ZUITE_NAME])
        zuite_factory.manage_addZuite(id = ZUITE_NAME)

    def createKssDemo(self, context):
        """creates the kss.demo. Yes, I need context to be passed
        as parameter"""
        if hasattr(context, KSSDEMO_NAME):
            context.manage_delObjects([KSSDEMO_NAME])
        kssdemo_id = context._setObject(KSSDEMO_NAME,
                                        SimpleContent(KSSDEMO_NAME, KSSDEMO_NAME))

    def bootStrap(self):
        context = self.context.aq_inner
        self.createZuite(context)
        self.createKssDemo(context)
        return """<html>
                    <body>
                      <div id="ok">OK</div>
                    </body>
                  </html>"""

    __call__ = bootStrap
