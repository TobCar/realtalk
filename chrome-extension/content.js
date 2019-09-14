'use strict';

var url = location.href;

var videoId = url.toString().substring(32, url.toString().length);

/**
 *  MAKE REQUEST AND GET ARRAY
 */

var res = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0,0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1];

var timer = setInterval(function() {
    var yt = document.querySelector('.video-stream');
    var time = Math.floor(yt.currentTime);
    if (res[time] !== undefined) {
        if (res[time] === 0) {
            chrome.runtime.sendMessage({ message: "fake" });
        } else if (res[time] === 1) {
            chrome.runtime.sendMessage({ message: "real" });
        }
    }
}, 5000);
// TODO double check that 5000 interval distance is correct
