$('.extract').click(function(){
    var btn = $(this);
    var file = btn.attr('data-target');
    btn.addClass('btn-warning');
    console.log('calling');
    $.ajax('/x/'+file)
        .done(function(data){
            console.log('success');
            console.log(data);
            $('#status').text("finished in " + data.time);
            btn.removeClass('btn-warning');
            btn.addClass('btn-success');
        })
        .fail(function(data) {
            console.log('error');
            console.log(data);
            btn.removeClass('btn-warning');
            btn.addClass('btn-error');
        })
        .always(function(data) {
            console.log( "complete" );
        });
});