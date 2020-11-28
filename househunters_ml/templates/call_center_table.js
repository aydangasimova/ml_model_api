$(document).ready(function(){
//   $("#schedule").schedule();

  $("#export").click(function(){
  $("#schedule").table2excel({
    // exclude CSS class
    exclude:".noExl",
    name:"Worksheet Name",
    filename:"Schedule_27112020.xls",//do not include extension
    fileext:".xls" // file extension
  });
});
})
