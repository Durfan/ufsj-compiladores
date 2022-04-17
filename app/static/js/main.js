$("#nuke").click(function () {
  $("#formCode").fadeOut()
  $("#btns-form").fadeOut()
});

$(document).ready(function () {
  const clipboard = new ClipboardJS('.copythis')
  $('[data-bs-toggle="tooltip"]').tooltip()

  clipboard.on('success', function (e) {
    $('.tooltip-inner').html('Copiado!')
    $(e.trigger).tooltip('update')
    e.clearSelection()
  });

  $.ajax({
    url: "/static/example01.txt",
    dataType: "text",
    success: function (data) {
      $("#example-code").html(data);
    }
  });
});