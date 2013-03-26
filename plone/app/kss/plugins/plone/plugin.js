
/* Use onDOMLoad event to initialize kukit
   earlier then the document is fully loaded,
   but after the DOM is at its place already.
*/

kukit.plone = {};

/* This check must not result in a javascript error, even if jq is
 * not present. Such an error would case all subsequent kss plugin
 * (this file and any other plugins that are loaded later)
 * fail to load.
 *
 * For this reason, it must be guarded by a condition.
 */
if (window.jq) {
    jq(function() {
        kukit.log('KSS started by jQuery DOMLoad event.');
        kukit.bootstrapFromDOMLoad();
    });
}



/* Base kukit plugins for Plone*/

kukit.actionsGlobalRegistry.register("plone-initKupu", function(oper) {
    kukit.logDebug('Enter plone-initKupu');
    oper.evaluateParameters([], {}, 'plone-initKupu action');
    // we start from the iframe node...
    if (oper.node.tagName.toLowerCase() != 'iframe') {
;;;     kukit.E = 'The plone-initKupu action can only be setup on an iframe';
;;;     kukit.E += ' node.';
        throw kukit.E;
    }
    var divnode = oper.node.parentNode.parentNode.parentNode.parentNode;
    var id = divnode.id;
    if (! id) {
;;;     kukit.E = 'The plone-initKupu action did not find the editor id from';
;;;     kukit.E += ' the iframe node.';
        throw kukit.E;
    }
 
    //
    // Register the kupu editor in KSS
    // This enables KSS to update the textarea explicitely. 
    //
    var prefix = '#'+id+' ';
    var textarea = getFromSelector(prefix+'textarea.kupu-editor-textarea');
    kukit.fo.fieldUpdateRegistry.register(textarea,
            {editor: null,
             node: textarea,
             doInit: function() {
                kukit.log('Setup Kupu initialization on load event.');
                var self = this;
                initKupuOnLoad = function() {
                    kukit.log('Initialize Kupu from onload event.');
                    self.editor = initPloneKupu(id);
                };
                this.editor = initPloneKupu(id);
                jq(window).load(initKupuOnLoad);
                },
             doUpdate: function() {
                this.editor.saveDataToField(this.node.form, this.node);
                // set back _initialized
                // XXX check if this is actually ok?
                this.editor._initialized = true;
                }
             });
    kukit.logDebug('plone-initKupu action done.');
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initKupu', 
    kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("init-tinymce", function(oper) {
    var textarea = document.getElementById(oper.node.id);
    config = jQuery.parseJSON(jQuery(textarea).attr('data-mce-config'));
    jQuery(textarea).tinymce(config);
});

kukit.actionsGlobalRegistry.register("save-tinymce", function(oper) {
    if(tinymce.EditorManager != undefined && tinymce.EditorManager.activeEditor != null){
        tinymce.EditorManager.activeEditor.save();
    }
});

kukit.actionsGlobalRegistry.register("plone-followLink", function(oper) {
    oper.evaluateParameters([], {}, 'plone-followLink action');
    var url = oper.node.href;
    if (url.substr(0, 7) == "http://") {
        // redirect to it
        window.location.replace(url);
    } else if (url.substr(0, 13) == "javascript://") {
        // execute it
        eval(url.substr(13));
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-followLink',
    kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-submitCurrentForm", function (oper) {
    oper.evaluateParameters([], {}, 'plone-submitCurrentForm action');
    // disable the onbeforeunload event since we want to submit now.
    window.onbeforeunload = null;
    var form = new kukit.fo.CurrentFormLocator(oper.node).getForm();
    form.submit();
});
kukit.commandsGlobalRegistry.registerFromAction('plone-submitCurrentForm',
    kukit.cr.makeSelectorCommand);

kukit.plone.FormProtectionCheckedEvents = function() {
};

kukit.plone.FormProtectionCheckedEvents.prototype.__default_failed__ = 
    function(name, oper) {
};

kukit.eventsGlobalRegistry.register('plone', 'formProtectionChecked',
    kukit.plone.FormProtectionCheckedEvents, null, null);

kukit.eventsGlobalRegistry.register('plone', 'formProtectionFailed',
    kukit.plone.FormProtectionCheckedEvents, null, '__default_failed__');

// Form Locking

kukit.actionsGlobalRegistry.register("plone-initLockingProtection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-initLockingProtection action');
    if (oper.node.tagName.toLowerCase() != 'form') {
;;;     kukit.E = 'The plone-initLockingProtection action can only execute';
;;;     kukit.E += ' on a form node as a target.';
        throw kukit.E;
    }
    plone.UnlockHandler.init();
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initLockingProtection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-removeLockProtection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-removeLockProtection action');
    plone.UnlockHandler.cleanup();
});
kukit.commandsGlobalRegistry.registerFromAction('plone-removeLockProtection',
    kukit.cr.makeGlobalCommand);

// Folder contents shift click selection
kukit.actionsGlobalRegistry.register("plone-initShiftDetection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-initShiftDetection action');

    kukit.engine.stateVariables['plone-shiftdown'] = false;
    jq(document).keydown(function(e) {
        if(e.keyCode == 16)
            kukit.engine.stateVariables['plone-shiftdown'] = true;
    });

    jq(document).keyup(function(e) {
        if(e.keyCode == 16)
            kukit.engine.stateVariables['plone-shiftdown'] = false;
    });
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initShiftDetection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-initCheckBoxSelection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-initCheckBoxSelection action');
    kukit.engine.stateVariables['plone-foldercontents-firstcheckeditem'] = null;
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initCheckBoxSelection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-createCheckBoxSelection",
    function(oper) {
    var actionMsg = 'plone-createCheckBoxSelection action';
    oper.evaluateParameters(['group'], {}, actionMsg);

    var node = oper.node;
    var firstItemVarName = 'plone-foldercontents-firstcheckeditem';
    var firstItem = kukit.engine.stateVariables[firstItemVarName];
    if(firstItem && kukit.engine.stateVariables['plone-shiftdown']) {
        var group = oper.parms.group;
        var allNodes = jq(group);
        var start = allNodes.index(firstItem);
        var end = allNodes.index(firstItem);
        if(start>end){
            var temp = start;
            start = end;
            end = temp;
        }
        allNodes.slice(start, end).attr('checked', firstItem.checked);
    }
    else {
        kukit.engine.stateVariables[firstItemVarName] = node;
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-createCheckBoxSelection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-initDragAndDrop",
    function(oper) {
    oper.evaluateParameters(['table'], {}, 'plone-initDragAndDrop action');
    var table = oper.parms.table;
    ploneDnDReorder.table = jq(table);
    if (!ploneDnDReorder.table.length)
        return;
    ploneDnDReorder.rows = jq(table + " > tr," +
                              table + " > tbody > tr");
     jq(table + " > tr > td.draggable," +
        table + " > tbody > tr > td.draggable")
        .not('.notDraggable')
        .mousedown(ploneDnDReorder.doDown)
        .mouseup(ploneDnDReorder.doUp)
        .addClass("draggingHook")
        .css("cursor","ns-resize")
        .html('&#x28ff;');
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initDragAndDrop',
    kukit.cr.makeSelectorCommand);
