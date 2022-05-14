console.log("Connecting...")
ws = new WebSocket("ws://127.0.0.1:11000");
ws.onopen = function() {

}



ws.onmessage = function(event) {
    data = event.data;
    var split = event.data.split("^");
    if (split[0] == "updatePage") {
        document.head.innerHTML = split[2];
        document.body.innerHTML = split[1];
        console.log(split[3]);
        window.eval(split[3]);
        // get a ranodm number between 1 and 10
        // var randomNumber = Math.floor(Math.random() * 10) + 1;
        // document.body.style.zIndex = randomNumber;
        document.body.style.maxHeight = "100vh";
        document.body.style.height = "100vh";
        // document.body.style.width = "100%";
    }
}