$(document).ready(function(){
var $checks = $('input:checkbox').click(function(e) {
    var numChecked = $checks.filter(':checked').length;
    if (numChecked > 3) {
        alert("sorry, you have already selected 3 checkboxes!");
    }});
}
)