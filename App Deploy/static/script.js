$(document).ready(function () {
  // Init
  $(".image-section").hide();
  $(".loader").hide();
  $("#result").hide();

  $("#btn-predict").hide();
  // Upload Preview
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#previewImg").attr("src", e.target.result);
        $(".image-section").show();
        $("#btn-predict").show();
        $("#result").text("");
        $("#result").hide();
      };
      reader.readAsDataURL(input.files[0]);
    }
  }

  $("#imageUpload").change(function () {
    readURL(this);
  });

  $("#imageUpload").change(function () {
    $(".image-section").show();
    $("#btn-predict").show();
    $("#result").text("");
    $("#result").hide();
    readURL(this);
  });

  // Predict
  $("#btn-predict").click(function () {
    var form_data = new FormData($("#upload-file")[0]);

    // Show loading animation
    $(this).hide();
    $(".loader").show();

    // Make prediction by calling api /predict
    $.ajax({
      type: "POST",
      url: "/predict",
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Get and display the result
        $(".loader").hide();
        $("#result").fadeIn(600);
        $("#result").text(" Result:  " + data);
        console.log("Success!");
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
        // Show error message if upload fails
        $("#result").text("Error uploading image. Please try again.");
        $("#result").fadeIn(600);
      },
    });
  });
});
