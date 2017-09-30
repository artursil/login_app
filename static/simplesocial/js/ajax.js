$(function(){

    $('#search').keyup(function(){
        console.log("dziala");
        $.ajax({
            type: "POST",
            url: "/tags/search/",
            data: {
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'

        });

    });
});
function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data);
}

// $(function() {
//     $("#id_input").on('keyup', function(){
//         var value = $(this).val();
//         $.ajax({
//             url: "{% url 'tags:ajax_autocomplete' %}",
//             data: {
//               'search': value
//             },
//             dataType: 'json',
//             success: function (data) {
//                 list = data.list;
//                 $("#id_input").autocomplete({
//                 source: list,
//                 minLength: 3
//                 });
//             }
//         });
//     });
//   });




// $(function(){
//
//         $.ajax({
//             type: "POST",
//             url: "/tags/search/",
//             data: {
//                 'search_text': $('#search').val(),
//                 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
//             },
//             success: searchSuccess,
//             dataType: 'html'
//
//         });
//
//     });
//
// function searchSuccess(data, textStatus, jqXHR)
//     {
//         $('#search').autocomplete(data);
//     }

// $( function() {
//
//   $( "#search" ).autocomplete({
//     source: function( request, response ) {
//       $.ajax( {
//         type: "POST",
//         url: "/tags/search/",
//         data: {
//             'search_text': $('#search').val(),
//             'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
//         },
//         success: searchSuccess
//       } );
//     },
//     minLength: 2,
//   } );
// } );
//
// function searchSuccess(data, textStatus, jqXHR)
// {
//     $('#search-results').html(data);
// }
