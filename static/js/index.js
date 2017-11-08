$(document).ready(function(){

    $(".formulas_box").on('change', '#rdsat_csv', function(){
        if ($(this).val()) {
            enable_submit_button();
        }
    })

    $(".formulas_box").on('click', '#submit_button', function(){

        var formData = new FormData($('#my_form')[0]);

        reset_upload_form();
        progress_bar_move();

        $.ajax({
            url: '/show_results',
            type: 'POST',
            data: formData,
            //cache: false,
            contentType: false,
            processData: false,
            //async: false,
            success : function(data) {
                //alert(data.result);
                //hide_upload_form();
                show_results(data.result);
            }
        });

    });

});


function reset_upload_form() {
    $('#my_form')[0].reset();
    $('#submit_button').prop('disabled', true).addClass("noHover");
}


function hide_upload_form() {
    $('#my_form')[0].reset();
    $('#submit_button').prop('disabled', true).addClass("noHover");
    $('#load_file').hide();
}


function show_results(result) {
    $('#results_box').slideDown();
    $('#tele_txt').empty().append(result);
}


function enable_submit_button() {
    $('#submit_button').prop('disabled', false).removeClass("noHover");
    $('#results_box').slideUp();
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
