$('.extract').click(function(){
    var btn = $(this);
    var file = btn.attr('data-target');
    btn.addClass('btn-warning');
    btn.removeClass('btn-info');
    $.ajax('/x/'+file)
        .done(function(data){
            $('#status').text("extracted " + data.file + " in " + data.time);
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
            $('#status').text("copied " + data.file + " in " + data.time);
            btn.removeClass('btn-warning');
            btn.addClass('btn-success');
        })
        .fail(function() {
            btn.removeClass('btn-warning');
            btn.addClass('btn-danger');
        });
});

$('.move').click(function(){
    var btn = $(this);
    var file = btn.attr('data-target');
    btn.addClass('btn-warning');
    $.ajax('/m/'+file)
        .done(function(data){
            $('#status').text("moved " + data.file + " in " + data.time);
            btn.closest('tr').remove();
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
    var idx = btn.closest('tr').attr('class');
    var idxs = idx.split(' ');
    idx = idxs[idxs.length - 1];
    $.ajax('/d/'+file)
        .done(function(data){
            $('#status').text("deleted " + file);
            $('.'+idx).remove();
        })
        .fail(function(data) {
            $('#status').text("delete failed " + data.staus);
            btn.removeClass('btn-danger');
            btn.addClass('btn-warning');
        });
});

$('#down tr').click(function () {
    var element = $(this).find('.move');
    var file = element.attr('data-target');
    $('#fileInfo').load('/ih/' + encodeURIComponent(file), function (response, status, xhr) {
        if (status == 'error') {
            $('#fileInfo').html('Not an mkv file').css('zIndex', 3).css('marginLeft', 0);
            return;
        }
        $('#fileInfo').css('zIndex', 1).css('marginLeft', '148px');
        $('#fileInfo').find('td.track').click(function () {
            var track = $(this);
            var trackId = track.attr('data-target');
            var trackType = track.attr('data-type');
            console.log(trackId, trackType);
            // TODO use trackinfo
        });
    });
});

$('#fileInfo').find('td.track').click(function () {
    console.log($(this));
});

$('#fileInfo').hover(function () {
    $(this).css('zIndex', 3).css('marginLeft','0px');
}, function () {
    $(this).css('zIndex', 1).css('marginLeft','148px');
});

$(function() {
    var $sidebar, $window, offset, delta, topPadding, $navbar;
    $sidebar = $("#fileInfo");
    $window = $(window);
    offset = $sidebar.offset();
    $navbar = $('#nav-bar');
    console.log($("#footer").offset());
    delta = $("#footer").offset().top - $navbar.offset().top - $navbar.outerHeight() - $sidebar.outerHeight();
    topPadding = 50;

    $window.scroll(function() {
        console.log(delta);
        $sidebar.stop().animate({
            marginTop: Math.max(Math.min($window.scrollTop() - offset.top + topPadding, delta), 0)
        });
    });

});
