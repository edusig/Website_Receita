$(function(){
    var rating = $('.votacao').data('rate');

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
    );
});