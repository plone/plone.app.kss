

// bind toc code


kukit.actionsGlobalRegistry.register("createTableOfContents", function (oper) {
        createTableOfContents();
    });
kukit.commandsGlobalRegistry.registerFromAction('createTableOfContents', kukit.cr.makeGlobalCommand);

kukit.log('actions for Plone legacy js registered (create TOC)');

