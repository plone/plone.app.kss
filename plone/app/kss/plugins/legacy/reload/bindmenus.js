
// bind action menus on load


kukit.ar.actionRegistry.register("bindActionMenus", function (oper) {
        initializeMenus();
        kukit.logDebug('Plone menus initialized');
    });

kukit.log('actions for Plone legacy js registered (bind menus)');

