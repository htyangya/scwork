function getdata() {
    var name= $("#id_name").val();
    if(!!name){
        $.get("/utils/getdata",{"name":name},function(e,status,xhr){
        if(!!e.errorcode){
            alert(e.errorcode);

        }
        else{
            $("#id_name").val(e["查找到公司名称"]);
            $("#id_address").val(e["地址"]);
            $("#id_city").val(e["城市"]);
            var  contact_man=e["法定代表人"]||e["负责人"]
            $("#id_contact_man").val(contact_man);
            $("#id_tel").val(e["电话"]);
            var coment=JSON.stringify(e)
            $("textarea:last").text(coment);

        }
        if(!!e.customs){
            alert("请注意，该客户名称在数据库中查询到相关条目，请检查该客户是否已存在，请勿重复新增：\n"+JSON.stringify(e.customs))
        }
    })
    }

}
