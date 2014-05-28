var csrftoken = $('meta[name="csrf-token"]').attr('content');

$(document).ready(function(){
  $('#noteButton').click(postNewNote);
});

function postNewNote()
{
  var fatherForm = $(this).parent();
  var body = $(fatherForm).find('textarea').first().val();
  if (body === ""){
    // The content is not allowed to be empty
  }else{
    var uid = $(fatherForm).find('span').first().text();

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    });

    var flag = 0;
    $.getJSON('/note',
       {
         content : body,
         "uid" : uid
       },
       function(data){
        if( data.success == "1"){
          // insert into database successfully
          location.href = "/index";
        }else{
          //show errors
        }
       }
    );

  }
}
