$(document).ready(function () {

    $(".js_in").change(function () {
        var therow = $(this).closest('.js_row');
        var stock = parseInt(therow.find('.js_stock').text(), 10);
        var input = parseInt($(this).val(), 10);

        var has_errors = _.isNaN(input) || input < 0 || input > stock;
        therow.toggleClass('danger', has_errors);
        $('.js_overflow_alert').toggleClass('hidden', !has_errors);

        $('.js_sbutton').attr('disabled', !!$('.danger').length);
    });

});
