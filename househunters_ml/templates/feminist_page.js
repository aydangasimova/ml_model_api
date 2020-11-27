$(document).ready(function(){
var $checks = $('input:checkbox').click(function(e) {
    var numChecked = $checks.filter(':checked').length;
    if (numChecked >= 3) {
        $("#test-result").text("lalala");
    } else {$("#test-result").text("Blalala");}
});
}
)