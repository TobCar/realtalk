// Expect messages from content scripts to change the popup
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    var msg = request.message;
    if (msg) {
        if (msg == "loading") {
            const player = document.querySelector('lottie-player');
            player.load('https://assets8.lottiefiles.com/temp/lf20_3bpCnZ.json');
            document.getElementById("prompt").innerHTML = "Running analysis...";
        } else if (msg == "real") {
            const player = document.querySelector('lottie-player');
            player.load('https://assets8.lottiefiles.com/temp/lf20_3bpCnZ.json');
            document.getElementById("prompt").innerHTML = "Audio is likely real";
        } else if (msg == "fake") {
            const player = document.querySelector('lottie-player');
            player.load('https://assets3.lottiefiles.com/temp/lf20_tNI4Yn.json');
            document.getElementById("prompt").innerHTML = "Audio is likely fake";
        } else if (msg == "default") {
            const player = document.querySelector('lottie-player');
            player.load('https://assets6.lottiefiles.com/packages/lf20_lqsmgn.json');
            document.getElementById("prompt").innerHTML = "";
        } else {
            document.getElementById("prompt").innerHTML = "";
        }
    }
});
