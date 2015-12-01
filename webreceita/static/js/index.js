function busca_suggest(data){
    return '<div><a href="/detalhe_receita/' + data.id + '"/>' + data.value + '</a></div>';
}

function busca_result(data){
    'use strict';
    window.console.log(data);
    $('#busca_receita').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },{
        name: 'receitas',
        source: busca_source(data),
        limit: 20,
        display: 'value',
        templates:{
            empty: [
                '<div class="empty-message">',
                'Nenhuma receita encontrada',
                '</div>'
            ].join('\n'),
            notFound: [
                '<div class="empty-message">',
                'Nenhuma receita encontrada',
                '</div>'
            ].join('\n'),
            suggestion: busca_suggest
        }
    });
    $('.twitter-typeahead').bind('typeahead:select', function(ev, suggestion) {
        window.location.replace("/detalhe_receita/"+suggestion.id+"/");
    });
}

function busca_source(data){
    return function busca_match(q, cb){
        'use strict';
        var matches, subregx;
        matches = [];

        subregx = new RegExp(q, 'i');

        $.each(data.receitas, function(i, str){
            if (subregx.test(str[0])){
                matches.push({value: str[0], id: str[1]});
            }
        });

        cb(matches);
    };
}

$(function(){
    $.ajax({
        method: 'GET',
        url: "/busca/",
        dataType: "json",
        cache: true,
        success: busca_result
    });
});