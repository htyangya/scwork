var query_data;
var choose_list;
//根据当前筛选条件进行查询,然后加载选项到选择模态框
function query_and_load(type="normal"){
    var id=$('#mymodal').attr("data-id")
    var active_select=$("#id_equipment_bar_set-"+id+"-personel")[0].selectize
    var $major_type=$("#id_equipment_bar_set-"+id+"-major_type")[0].selectize
    var major_type_value=$major_type.getItem($major_type.getValue()).text()
    if(!major_type_value){
        return false
    }
    var $level=$("#id_equipment_bar_set-"+id+"-level")[0].selectize
    var level_value=$level.getItem($level.getValue()).text()
    var $subject=$("#id_equipment_bar_set-"+id+"-subject_or_worktype")[0].selectize
    var subject_value=$subject.getItem($subject.getValue()).text()
    id_list=active_select.getValue()
    var data={
        "major_type":major_type_value,
        "level":level_value,
        "subject":subject_value,
        "id_list":JSON.stringify(id_list),
        "type":type
    }
    $(".query").prop("disabled",true)
    if (JSON.stringify(data)==JSON.stringify(query_data)){
        after_query(Object.keys(choose_list.options).length,type)
        return true
    }
    query_data=data
    choose_list.clearOptions()
    choose_list.load(function(callback) {
        $.post('/personnel_choose/choose',data,function (e) {
            callback(e)
            choose_list.setValue(id_list)
            after_query(e.length,type)
        })
    })
    return true

}
function after_query(len,type) {
    $("#re-text").text("共找到"+(len)+"个人才")
    if (!len){
        $("#re-text").removeClass("text-success")
        $("#re-text").addClass("text-danger")


    }else{
        choose_list.focus()
        $("#re-text").removeClass("text-danger")
        $("#re-text").addClass("text-success")
        if(type == "reverse"){
            //如果有返回值，而且查询的是不可用列表，解开三个查询按钮，继续冻结两个set按钮
            $(".q-search").prop("disabled",false)
        }else{
            //如果查询的是可用列表，放开所有按钮
            $(".query").prop("disabled",false)
        }
    }
}
//打开模态框，并根据按钮的位置更新模态框的data-id，方便其他函数定位
function modalopen(btn){
    var $activeselect= $(btn).siblings("select")
    var id=$activeselect.attr('id').match(/\d+/i)[0]

    $('#mymodal').attr("data-id",id)
    $("#re-text").text("")
    if(!query_and_load()){
        alert("请选择所属大类！")
        return
    }

    $('#mymodal').modal({
            keyboard: false
    })
    }
 //点击覆盖或追加到人才库，进行计算
function to_activeselect(add_or_reset=0){
    var id=$('#mymodal').attr("data-id")
    var active_select=$("#id_equipment_bar_set-"+id+"-personel")[0].selectize
    var number=$("#id_equipment_bar_set-"+id+"-number")
    var sc_number=$("#id_equipment_bar_set-"+id+"-sc_number")
    var money=$("#id_equipment_bar_set-"+id+"-money")

    if (add_or_reset==0){
        active_select.setValue(active_select.getValue().concat(choose_list.getValue()))
    }else{
        active_select.setValue(choose_list.getValue())
    }
    value_list=active_select.getValue()
    sc_number.val(value_list.length)
    number.val(value_list.length)
    options=choose_list.options
    total=0
    $.each(value_list,function (index,value) {
        total+=options[value].money
    })
    money.val(total)
    $('#mymodal').modal("hide")

}

 //点击+新增的区域执行操作
function make_buttons(){
    var selects=$("select[id^=id_equipment_bar_set-][id$=-personel]");
    $.each(selects,function (index,select) {
        var selectize=select.selectize
        selectize.disable()
        if (!$(select).parents('.controls ').hasClass('form-inline')){
            $(select).parents('.controls ').addClass('form-inline')
        }
        if($(select).siblings('.btn.btn-info.modal-bu').length==0){
           $(select).parent().append("&nbsp;&nbsp; <button class='btn btn-info modal-bu' type='button'  onclick='modalopen(this)' ><span class='glyphicon glyphicon-search'></span></button>")
           select.selectize.disable()
        }

    })
}
//给原始选择框加载包含money的新opt，方便计算总价


//禁用默认选择框，初始化筛选界面的selectize
function init_choose(){
    var selects=$("select[id^=id_equipment_bar_set-][id$=-personel]");

    //添加按钮
    selects.parents('.controls ').addClass('form-inline')
    selects.parent().append(
        "&nbsp;&nbsp; <button class='btn btn-info modal-bu' type='button'  onclick='modalopen(this)' ><span class='glyphicon glyphicon-search'></span></button>")
    // 禁用默认选择框
    $.each(selects,function(index,select) {
        select.selectize.disable()
    })

    //初始化自定义筛选框
       $('#choose').selectize({
           delimiter: ",",
           create: false,
           valueField: 'id',
           labelField: 'name',
           searchField: ['id', 'name'],
           plugins: ['remove_button'],
           render: {
               // 自定义选项的显示
               option: function (item, escape) {
                   var tags = [];
                   for (var i = 0, n = item.subjects.length; i < n; i++) {
                        tags.push('<span class="label label-default">' + item.subjects[i] + '</span>');

                   }
                    return '<div><div class="title pull-left" style="padding-left: 5px">'+
                    '<div><strong class="name">'+escape(item.name)+'</strong></div>'+
                        '<div><small><em>'+escape(item.type)+'</em></small></div>'+
                        (item.statushtml=="空"?"<p><p class=\"text-success\">  <span class=\"badge\" style=\"background-color:green;color:white\">无</span><small>当前无占用</small></p><p>":item.statushtml)+
                    '<div class="tags">'+
                         tags.join(' ')+
                    '</div>'+
                    '</div></div>'

               }
           },
       })
    //给全局变量赋值
     choose_list=$('#choose')[0].selectize
}

function before_save_enable_selects(){
    var selects=$("select[id^=id_equipment_bar_set-][id$=-personel]");
    $.each(selects,function(index,select) {
        select.selectize.enable()
    })
}


$(function () {
     init_choose()
    $('#equipment_bar_set-add-row').click(make_buttons)
    $('#equipment_form').submit(before_save_enable_selects)

})