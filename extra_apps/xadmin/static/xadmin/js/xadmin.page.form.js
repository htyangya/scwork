;(function($){
    $(function() {
        var action_bar = $('.form-actions');
        if(action_bar.length){
            var height=action_bar[0].offsetTop + action_bar.outerHeight();
            var onchange = function(){
                var s=(document.body.scrollTop||document.documentElement.scrollTop) + window.innerHeight;
                if(s<height){action_bar.addClass('fixed');}
                else{action_bar.removeClass('fixed');}
            }
            window.onscroll=onchange;
            onchange();
        }
        if(window.__admin_ismobile__){
            $(window).bind('resize', function(e){
                var rate = $(window).height() / $(window).width();
                var action_bar = $('.form-actions');
                if(rate < 1){
                    action_bar.css('display', 'none');
                } else {
                    action_bar.css('display', 'block');
                }
            });
        }
    });
    var exform = $('.exform').first();
    if (exform.find('.text-error').length > 0){
        var first_activated = false;
        exform.find('.error').each(function(){
            if (!first_activated){
                var parent = $(this);
                while (!(parent.html() == exform.html())){
                    if (parent.hasClass('tab-pane')){
                        parent.addClass('active');
                        parent.siblings().removeClass('active');
                        var menu_tab = $('a[href="#' + parent.attr('id') + '"]');
                        menu_tab.parent().addClass('active');
                        menu_tab.parent().siblings().removeClass('active');
                        first_activated = true;

                    }
                    if (parent.hasClass('box-content')){
                        parent.show();
                    }
                    parent = parent.parent();
                }
            }
        });
    }
})(jQuery)

function zhizhitoggle(){
    var contract_type_select=$("#id_contract_type")[0].selectize
    var zizhipb=$(".panel-heading:contains('资质合同')").next()
    var deadlines = $("input[id*='id_deadline']")
    var dllabels=$("label[for*='id_deadline']")
    dllabels.find("span.asteriskField").remove()
    if (contract_type_select.getValue()=="资质合同"){
            zizhipb.show()
            deadlines.prop("required",true)
            dllabels.append("<span class=\"asteriskField\">*</span>")
        }else{
            zizhipb.hide()
            deadlines.prop("required",false)

        }
}

$(function () {
    if(window.location.href.includes('contract/contract') ) {
        var contract_type_select=$("#id_contract_type")[0].selectize
        $(".panel-heading").not(":contains('通用')").not(":contains('资质合同')").next().hide()
        zhizhitoggle()
        contract_type_select.on('blur',zhizhitoggle)
    }

    if($("#custom_form").length){
       var f= $("#custom_form")
        f.submit(function () {
            var name=$("#id_name").val()
            var address=$("#id_address").val()
            if (name.length>=5 && !address){
                var re=confirm("您的客户名称长度大于5，疑似是公司名称。\n" +
                    "如果客户是公司而非个人，请点击【根据客户名称查询企查查信息】按钮查询出公司地址和城市。\n" +
                    "确定提交表单，取消返回查询。");
                if (!re) return false;
                return true
            }

        })
    }
})
function toggle_value(link){
        var a=$(link)
        var hidevalue=a.attr('hidevalue')
        var v=a.text()
        if (v == "..."){
            a.text(hidevalue)
            a.removeAttr('style')

        }else{
            a.text("...")
            a.css({
                "color":"red",
                "font-size" : "large"
            })
        }

    }