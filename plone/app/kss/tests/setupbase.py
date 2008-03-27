try:
    from Products.Five import BrowserView
    BrowserView = BrowserView   # satisfy pyflakes
except ImportError:
    from zope.publisher.browser import BrowserView

from Acquisition import aq_parent
from OFS.interfaces import IApplication

class SetupBase(BrowserView):
    """This class provides the basic bootstrap set for every
    test suite bootstrapping. You must inherit from this class
    and override just the run method"""

    _required_role = 'Manager'

    def __init__(self, context, request):
        super(SetupBase, self).__init__(context, request)
        #go up to the root
        parent = aq_parent(self.context.aq_inner)
        while not IApplication.providedBy(parent):
            try:
                parent = parent.aq_parent
            except AttributeError:
                break
        self.zoperoot = parent

    def checkPermission(self):
        method = self.request.get("REQUEST_METHOD", "GET").upper()
        username = self.request.get("username", None)
        password = self.request.get("password", None)
        if method == "POST" and username is not None and password is not None:
            admin = self.zoperoot.acl_users.authenticate(username, password, None)
            if self._required_role in admin.getRoles():
                return True
        return False
    
    def run(self):
        """Just override me"""
        raise Exception("Functionality not implemented")

    def start(self):
        if self.checkPermission():
            return self.run()
        else:
            raise Exception("You are trying to run potentially disruptive code without providing a good auth")

    __call__ = start
