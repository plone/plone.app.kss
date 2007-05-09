# -*- coding: UTF-8 -*-
from zope.interface import implements
from azaxview import PloneKSSView
from kss.core import force_unicode, kssaction
from interfaces import IPloneKSSView

class CalendarView(PloneKSSView):

    # --
    # Calendar in-place refreshment
    # --

    implements(IPloneKSSView)

    @kssaction
    def refreshCalendar(self, month, year, portlethash):
        'In-place refreshment of the calendar.'
        month, year = int(month), int(year)
        # do it
        self.getCommandSet('refreshportlet').refreshPortlet(portlethash, year=year, month=month)
