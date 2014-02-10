$('.extract').click(function(){
    var btn = $(this);
    var file = btn.attr('data-target');
    btn.addClass('btn-warning');
    btn.removeClass('btn-info');
    $.ajax('/x/'+file)
        .done(function(data){
            $('#status').text("finished " + data.file + " in " + data.time);
            btn.removeClass('btn-warning');
            btn.addClass('btn-success');
        })
        .fail(function() {
            btn.removeClass('btn-warning');
            btn.addClass('btn-danger');
        });
});

$('.copy').click(function(){
    var btn = $(this);
    var file = btn.attr('data-target');
    btn.addClass('btn-warning');
    btn.removeClass('btn-info');
    $.ajax('/c/'+file)
        .done(function(data){
            $('#status').text("finished " + data.file + " in " + data.time);
            btn.removeClass('btn-warning');
            btn.addClass('btn-success');
        })
        .fail(function() {
            btn.removeClass('btn-warning');
            btn.addClass('btn-danger');
        });
});

$('.delete').click(function(){
    var btn = $(this);
    var file = btn.attr('data-target');
    console.log('calling');
    $.ajax('/d/'+file)
        .done(function(data){
            btn.closest('tr').remove();
        })
        .fail(function() {
            btn.removeClass('btn-danger');
            btn.addClass('btn-warning');
        });
});