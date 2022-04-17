$("#nuke").click(function () {
  $("#formCode").fadeOut();
  $("#btns-form").fadeOut();
});

$(document).ready(function () {
  new ClipboardJS('.copythis');

  $.ajax({
    url: "/static/example01.txt",
    dataType: "text",
    success: function (data) {
      $("#example-code").html(data);
    }
  });
});