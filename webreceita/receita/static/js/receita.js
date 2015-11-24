function votacao_result(data){
    window.alert(data.response);
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$(function(){

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var rating = $('.votacao').data('rate');
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.votacao span').each(function(i){
        if(i < rating) {
            $(this).removeClass('glyphicon-star-empty');
            $(this).addClass('glyphicon-star');
        }
    }).hover(
        function(){
            var index = $(this).data('value');
            $('.votacao span').each(function(i){
                if(i < index){
                    $(this).removeClass('glyphicon-star-empty');
                    $(this).addClass('glyphicon-star');
                }else{
                    $(this).removeClass('glyphicon-star');
                    $(this).addClass('glyphicon-star-empty');
                }
            });
        },
        function(){
            $('.votacao span').each(function(i){
                if(i >= rating) {
                    $(this).removeClass('glyphicon-star');
                    $(this).addClass('glyphicon-star-empty');
                }else{
                    $(this).removeClass('glyphicon-star-empty');
                    $(this).addClass('glyphicon-star');
                }
            });
        }
    ).on('click', function(){
            var rating, pk;
            rating = $(this).data('value');
            pk = $('.votacao').data('receita');
            $.ajax({
                method: 'POST',
                url: "/votar/",
                dataType: "json",
                data: { 'pk': pk, 'rating': rating },
                success: votacao_result
            });
        });
    $('.imagem_galeria_item').on('mouseover', function(){
        $('#receita_imagem').attr('src', $(this).attr('src'));
    });
});