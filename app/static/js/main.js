$("#nuke").click(function () {
  $("#formCode").fadeOut();
  $("#btns-form").fadeOut();
});

$(document).ready(function () {
  new ClipboardJS('.copythis');
});