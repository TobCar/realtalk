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
            chrome.browserAction.setPopup({ popup: "popup.html" });
        }
    });
});

// Expect messages from content scripts to change the popup
/*chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.loading && (request.loading == "true")) {
        chrome.browserAction.setPopup({ popup: "popup-loading.html" });
    }
    if (request.good) {
        if (request.good == "true") {
            chrome.browserAction.setPopup({ popup: "popup-real.html" });
        }
    }
    var msg = request.message;
    if (msg) {
        if (msg == "loading") {
            chrome.browserAction.setPopup({ popup: "popup-loading.html" });
        } else if (msg == "real") {
            chrome.browserAction.setPopup({ popup: "popup-real.html" });
        } else if (msg == "fake") {
            chrome.browserAction.setPopup({ popup: "popup-fake.html" });
        } else if (msg == "default") {
            chrome.browserAction.setPopup({ popup: "popup.html" });
        } else {
            chrome.browserAction.setPopup({ popup: "popup.html" });
        }
    }
});*/