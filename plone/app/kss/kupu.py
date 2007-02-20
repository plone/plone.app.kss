# -*- coding: UTF-8 -*-
from zope.interface import implements
from azaxview import AzaxBaseView
from kss.core import force_unicode, kssaction
from interfaces import IPloneAzaxView

from datetime import datetime

class KupuSaveView(AzaxBaseView):

    # --
    # Calendar in-place refreshment
    # --

    implements(IPloneAzaxView)

    @kssaction
    def save(self, text, fieldname):
        "In-place saving of kupu text area's."
        time = datetime.now()
        corecommands = self.getCommandSet('core')
        self.context.getField(fieldname).set(self.context, text, mimetype='text/html')
        messageid = "kupu-save-message-%s" % fieldname
        selector = corecommands.getCssSelector('#kupu-editor-%s div.kupu-tb' % fieldname)
        corecommands.deleteNode('#' + messageid)
        corecommands.insertHTMLAsLastChild(
            selector, '<blink id="%s" style="color: red; font-weight: bold; font-size: 16pt">Document saved: %s</blink>' % (messageid, time.strftime('%H:%M:%S')))
