// Expect messages from content scripts to change the popup
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    var msg = request.message;
    if (msg) {
        if (msg == "loading") {
            document.getElementById("prompt").innerHTML = "Loading";
        } else if (msg == "real") {
            document.getElementById("prompt").innerHTML = "Real";
        } else if (msg == "fake") {
            document.getElementById("prompt").innerHTML = "Fake";
        } else if (msg == "default") {
            document.getElementById("prompt").innerHTML = "";
        } else {
            document.getElementById("prompt").innerHTML = "";
        }
    }
});