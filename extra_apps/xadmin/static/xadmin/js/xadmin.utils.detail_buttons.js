function init() {
  $( "#dialog" ).dialog(
      {
          autoOpen:false,
          title:"请确认您的选择",
          // dialogClass: "no-close",
          resizable: false,
          height:300,width:400,
          modal: true,
           buttons: {
              "确认":function () {

              },
              "取消": function() {
              $( this ).dialog( "close" );
            }
           }

      }
  );

}
function btns_click(btn) {
  var confirmbtn=$(".ui-dialog-buttonset button:contains('确认')");
  $('#ui-dialog-input-div').remove();
  if ($(btn).attr('d_hasper')=='True'){

      if ($(btn).attr('has_msg')=='True'){
          $('#ui-dialog-input-div').remove()
          $('.ui-dialog-content').append(
              "<div  id='ui-dialog-input-div' style='max-width: 99%'  class='center-block'>" +
              '<div class="form-group">'+
              "<label class='control-label col-md-2'>附语：</label>" +
              "<div class='col-md-10'>" +
              "<input text='text'id='ui-dialog-input' class='form-control'/>" +
              " </div>" +
              "</div></div>"
          )
      }

        var btns=$( "#dialog" ).dialog("option","buttons")
        btns["确认"]=function() {

            var url=$(btn).attr('d_url')
            if ($(btn).attr('has_msg')=='True'){url=url+"&msg="+$('#ui-dialog-input').val()}
            $(window).attr('location', url);

        }
        $( "#dialog" ).dialog("option","buttons",btns);
  }else{
        confirmbtn.hide()
  }

  $('.ui-dialog-content h4').text($(btn).attr('d_text'))

    $( ".ui-dialog-title" ).text($(btn).attr('d_title'));

    $( "#dialog" ).dialog("open")
};
$(function () {
  init()
})
