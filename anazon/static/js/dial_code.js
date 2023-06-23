var input = document.querySelector("#shipping_phone");
var iti = intlTelInput(input, {
    initialCountry: "auto",
    separateDialCode: true,
    nationalMode: false,
    autoInsertDialCode: true,
    hiddenInput : "full_phone",
    geoIpLookup: function (success, failure) {
        $.get("https://ipinfo.io", function () { }, "jsonp").always(function (resp) {
          var countryCode = (resp && resp.country) ? resp.country : "us";
          success(countryCode);
        });
      },
});

$("#shipping_form").submit(function() {
var full_phone = $('input:hidden[name=full_phone]').val();
$('input[name=phone]').val(full_phone);
});