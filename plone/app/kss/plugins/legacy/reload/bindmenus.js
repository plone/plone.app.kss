
// bind action menus on load


kukit.actionsGlobalRegistry.register("bindActionMenus", function (oper) {
        initializeMenus();
        kukit.logDebug('Plone menus initialized');
    });

kukit.log('actions for Plone legacy js registered (bind menus)');

