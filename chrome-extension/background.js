'use strict';

// Setup event listener for when user goes on a youtube video and gets the ID
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
        var url = tabs[0].url;
        if (url.toString().substring(0, 29) === 'https://www.youtube.com/watch') {
            chrome.tabs.executeScript({
                file: "content.js"
            });
        } else {
            chrome.tabs.sendMessage(tabs[0].id, { message: "default" });
        }
    });
});