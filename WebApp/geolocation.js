$(document).ready(function(){
    $('.stpostbutton').click(function() {
      $(".loader").css("display", "inline-block");
      //Check if HTLM5 Geolocation is supported
      /*if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
      } else {
        alert("Geolocation is not supported by this browser.");
      }
      function showPosition(position) {*/
        var update = $('#text').val();
        //var latitude = position.coords.latitude; 
        //var longitude = position.coords.longitude; 
        var latitude = 45.55; 
        var longitude = -73.535; 
        var postdata = "latitude="+latitude+"&longitude="+longitude+"&message="+update;//+"&g-recaptcha-response="+ grecaptcha.getResponse();
        console.log(postdata);
        var base_url="http://localhost/mtlwatch/WebApp/backend/GoogleAPIs/";
        var url = base_url+'parse';
        $.ajax({
          type: "POST",
          url: url,
          data: postdata,
          success: function(data){
            if(data === "captcha"){
              $('.captcha').html("CAPTCHA verification failed.");
            }
            else{
              console.log(data);
              $('.w-form').html(data);
              $("#about").css("padding-bottom", "450px");
            }
          }
      });
      //}
        
    });
  });





