$(document).ready(function(){

    $(".formulas_box").on('change', '#rdsat_csv', function() { upload_file_selected(this) })

    $('.formulas_box').on('click', ".rb-tab", function() { formula_selector(this) })


    $(".formulas_box").on('click', '#submit_button', function() {

        var formData = new FormData($('#my_form')[0]);
        funcs_selected = get_selected_formulas();
        formData.append("funcs_selected", funcs_selected);

        reset_upload_form();
        $('#spinner_box').show();

        $.ajax({
            url: '/show_results',
            type: 'POST',
            data: formData,
            //cache: false,
            contentType: false,
            processData: false,
            //async: false,
            success : function(data) {
                show_results(data);
            }
        });
    });
});


function get_selected_formulas() {
    var nums = [];
    for (i=0; i<$('.rb-tab').length; i++) {
        var this_id = $('.rb-tab')[i].id;
        if ($('#'+this_id).hasClass('rb-tab-active')) {
            nums.push(i+1);
        }
    }
    return nums;
}


function upload_file_selected(elem) {
    if ($(elem).val()) {
        $('#select_formula').slideDown();
        $('#results').children().hide();
        $('#results').slideUp();
    }
}


function formula_selector(elem) {
    if ( $(elem).hasClass( "rb-tab-active" ) ) {
        $(elem).removeClass("rb-tab-active");
    } else {
        $(elem).addClass("rb-tab-active");
    }

    if ($('#select_formula').children().hasClass('rb-tab-active')) {
        $('#submit_button').prop('disabled', false).removeClass("noHover");
    } else {
        $('#submit_button').prop('disabled', true).addClass("noHover");
    }
}


function reset_upload_form() {
    $('#my_form')[0].reset();
    $('#submit_button').prop('disabled', true).addClass("noHover");
    $('#select_formula').slideUp();
    $('#select_formula').children().removeClass("rb-tab-active");
}


function show_results(data) {
    result = data.result;
    $('#spinner_box').hide();
    $('#results').slideDown();
    $('#results h1').show();
    $('#results h2').show();
    for (var key in result) {
        $('#results_' + key).show();
        $('#tele_txt' + key).empty().append(result[key]);
    }

    $('#filename').empty().append(data.filename);
}


function progress_bar_move() {
    $('#progress').show();
    var w = 1;
    var id = setInterval(frame, 10);
    function frame() {
        if (w >= 100) {
            clearInterval(id);
        } else {
            w++;
            $('#progress_bar').css("width", w + '%');
        }
    }
}
