'use strict';

/**
 *  For anyone reading this code,
 * I used this way instead of web navigation cause since youtube is an app,
 * URL changes aren't making actual page requests, and is just referenced
 * by the app's router for the components, so webNavigation events don't work.
 * Had to "hack" around to make an event for watching youtube videos.
 */

// Setup event listener for when user goes on a youtube video and gets the ID
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
        var url = tabs[0].url;
        if (url.toString().substring(0, 29) === 'https://www.youtube.com/watch') {
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'logo.png',
                title: 'Watching video',
                message: `ID: ${url.toString().substring(32, url.toString().length)}`,
                priority: 0
            });
        }
    });
});