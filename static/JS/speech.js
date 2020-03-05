window.addEventListener('load', function () {

  var speech = {
      start : function () {
      // speech.start() : start speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        speech.recognition = new SpeechRecognition();
        speech.recognition.continuous = true;
        speech.recognition.interimResults = false;
        speech.recognition.lang = "en-US";
        speech.recognition.onerror = function (evt) {
          console.log(evt);
        };
        speech.recognition.onresult = function (evt) {
          document.getElementById('user_text').textContent = evt.results[0][0].transcript;
          var given_text = document.getElementById('given_text').textContent;
          //console.log(given_text)
          //console.log(evt.results[0][0].transcript)
  
          if ($("#user_text").text() != '')
          {
            var user_text = $("#user_text").text();
            var given_text = $("#given_text").text();
            $.ajax({
                      type: "POST",
                      cache: false,
                      data:{user_text:user_text, given_text:given_text},
                      url: '/speach_analize',
                      success: function(data) {
                          // remove whitespace from text
                          var g = $.trim(given_text);
                          var u = $.trim(user_text);
                          // split it into a array
                          var text = g.split(" ");
                          var user = u.split(" ");

                          if (data['mess'] === "You are right"){
                            $('#congrats').show();
                            $('#cp').text("Congratulations you learned new text");
                            $('#count').text('');
                            $('#rightness').text('');
                            $('#given_text').css('color', 'green');
                          }
                          
                          else
                          {
                            $('#given_text').css('color', 'red');
                            $('#count').text('Count of wrong words: ' + data['count']);
                            count = data['count']
                            
                            if (user.length <= text.length)
                            {
                              av_right = Math.round((user.length - count) * 100 / text.length);
                              $('#rightness').text('You were ' + av_right + "% right");
                            }
                            else
                            {
                              av_right = Math.round((text.length - count) * 100 / text.length);
                              $('#rightness').text('You were ' + av_right + "% right");
                            }
                            //console.log(text.length)
                          }
  
                          $('#result').show();
  
                          if (data['mess'] == "You said those wrong words" && data['count'] == 0){
                            $('#res').text("You didn't said some words");
                          }
                          else if(data['mess'] === "You said those wrong words" && user.length > text.length){
                            $('#res').text("You said some more words than has text");
                          }
                          else{
                            $('#res').text(data['mess']);
                          }
  
  
                          var ul = $('#misspeled ul');
                          $("#misspeled ul").empty();
                          var wrong_words = data['wrong'];
                          for (i = 0; i < wrong_words.length; i++)
                          {
                            var li = $('<li>'+ wrong_words[i]+ '</li>');
                            $(ul).append(li);
                          }
  
                         // console.log(data);
  
                      },
                      error: function(jqXHR) {
                          alert("error: " + jqXHR.status);
                          console.log(jqXHR);
                      }
                  })
          }
          document.getElementById('mic-on').style.display = 'none';
          document.getElementById('mic-off').style.display = 'block';
          speech.stop();
        };
        speech.recognition.start();
        document.getElementById('mic-on').disabled = true;
  
        document.getElementById('mic-off').disabled = false;
      },
  
      //stop : function () {
      // speech.stop() : end speech recognition
        
       stop : function(){
          speech.recognition.onspeechend = function(){
            
            document.getElementById('mic-on').style.display = 'block';
            document.getElementById('mic-off').style.display = 'none';
            document.getElementById('tts').disabled = false;
            document.getElementById('mic-on').disabled = false;
            document.getElementById('mic-off').disabled = true;
            
       }  
       speech.recognition.onspeechend();
         // }
          /*
        if (speech.recognition != null) {
          speech.recognition.stop();
          speech.recognition = null;
          document.getElementById('tts').disabled = false;
          document.getElementById('mic-on').disabled = false;
          document.getElementById('mic-off').disabled = true;
        }
        */
      }
    };
  
    window.addEventListener("load", function () {
      // [1] CHECK IF BROWSER SUPPORTS SPEECH RECOGNITION
      if (window.hasOwnProperty('SpeechRecognition') || window.hasOwnProperty('webkitSpeechRecognition')) {
        document.getElementById("search-speech").style.display = "block";
  
        // [2] ASK FOR USER PERMISSION TO ACCESS MICROPHONE
        // WILL ALSO FAIL IF NO MICROPHONE IS ATTACHED TO COMPUTER
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
          document.getElementById("mic-on").disabled = false;
        })
        .catch(function(err) {
          document.getElementById("search-speech").innerHTML = "Please enable access and attach a microphone";
        });
      }
    });
  
  
  
  
  
    document.getElementById("mic-on").addEventListener("click", function(){ speech.start(); });
    document.getElementById("mic-off").addEventListener("click", function(){ speech.stop(); });
  
  })