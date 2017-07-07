odoo.define('feuerwear.better_layout', function(require) {

    var base = require('web_editor.base');

    //var editor = require('base.editor');
    if (!$('table#uhelp').length) {
        return;
    }

    $(window).on('resize', function(event) {
        var fixed_height = $('#uhelp').height();
        $('.responsive-margin-top').css("margin-top",fixed_height+170)
        $('.responsive-background').css("height",fixed_height+250)
        $('.fixed-header').css("top",fixed_height+190)
    });
});

