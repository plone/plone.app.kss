
// bind external links marking on load


kukit.actionsGlobalRegistry.register("bindExternalLinks", function (oper) {
        scanforlinks();
        kukit.logDebug('Plone external links marker registered');
    });

kukit.log('actions for Plone legacy js registered (mark external links)');

