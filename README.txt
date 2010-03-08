plone.app.kss Package Readme
============================

Overview
--------
This product gives generic KSS support for Plone. It depends on the product
"kss.core".

Installation
------------

Compatible with Zope 2.12, and Plone 4.0.

Features implemented
--------------------

- Content tab replacer. This works with all the content (aka. "green") tabs
  including the non-action tabs in the setup screens. (put to experimental
  rules, by default off)

  As we have no way to identify a macro for the content-region in the current
  templating system of Plone, we render down the whole template. As a speedup,
  we replace the main_template in the rendering context, this may or may not
  have an effect depending on the template. If we cannot find a template at
  all, we fall back to submit.

  Missing/TODOS:

  - ...

- Portlet refresher

  We currently refresh the "recent" portlet. The rendering of the portlet is
  done by the general macro renderer, the portlet is then replaced in the 
  client in its position.

  There is one rule that is refreshing all the portlets, the only change
  that needs to be done in the Plone templates is put a KssPortletRefresh
  class to those portlet's outer <dl> tag that need to be refreshed.
  Refreshing is done in every 30 seconds currently, this can be adjusted
  from the template.

- In-place calendar navigation: the two little arrows replace the calendar
  portlet, without reloading the screen.

  We put kss attributes on the calendar node for the year and month
  to tell the server where to navigate. Actually, we could have done
  that without modifying the template either, since the server could
  have just received the original "href" of the little arrow and could
  parse the year and month from that, but this is a cleaner solution.

KSS extensions defined for general purpose use
----------------------------------------------

- A generic macro replacer server action

- client action for submitting to an url

- client action for submitting the current form

