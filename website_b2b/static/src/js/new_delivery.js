$( document ).ready(function () {

    $(".js_additionnal").change(function () {

        var therow = $(this).closest('.js_row');
        var additionnal = parseInt($(this).val(), 10);
        var delivery = parseInt(therow.find('.js_delivery').val(), 10);
        if (_.isNaN(additionnal) || additionnal < 0) {
            additionnal = 0;
            $(this).val(0);
        }
        therow.find('.js_total').text(delivery + additionnal);
    });

});
