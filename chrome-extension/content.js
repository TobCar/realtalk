'use strict';

var youtubeURL = location.href;

var videoId = youtubeURL.toString().substring(32, youtubeURL.toString().length);

var res;

// TODO: MUST CHANGE THIS TO FALSE BEFORE DEMOS
var flag = true;

if (flag === false) {
  var polling = setInterval(function() {
    fetchData()
  }, 1000);
}

var prodUrl = 'https://realtalk-252903.appspot.com/video';
var devUrl = 'http://localhost:8000/video';

function fetchData() {
  var formData = new FormData();
  formData.append('url', youtubeURL);
  formData.append('id', videoId);
  fetch(prodUrl, {
      method: 'POST',
      body: formData
    })
    .then(function(data) {
      return data.json()
    }).then(function(response) {
      console.log("Response data", response.data)
      res = response.data;
      flag = true;
      tick();
    }).catch(function(err) {
      chrome.runtime.sendMessage({ message: "loading" });
      console.log('Fetch Error :-S', err);
    });
}

var yt = document.querySelector('.video-stream');
var timer;

var tick = function() {
  timer = setInterval(function() {
      yt = document.querySelector('.video-stream');
      var time = Math.floor(yt.currentTime);
      if (res[time] !== undefined) {
          if (res[time] === 0) {
              chrome.runtime.sendMessage({ message: "fake" });
          } else if (res[time] === 1) {
              chrome.runtime.sendMessage({ message: "real" });
          }
      } else {
        chrome.runtime.sendMessage({ message: "default" });
      }
  }, 5000);
}

// yt.addEventListener("onStateChange", function(state) {
//   if (state === 1) {
//     tick();
//   } else {
//     clearInterval(timer);
//     chrome.runtime.sendMessage({ message: "default" });
//   }
// });

// TODO double check that 5000 interval distance is correct
