$(function(){
    var len = $('table tr').length;
    for(var i = 1;i<len;i++){
        $('table tr:eq('+i+') td:first').text(i);
    }
});