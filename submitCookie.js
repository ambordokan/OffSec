let submitButton = document.getElementById("submit-button");

submitButton.addEventListener("click", function() {
  let message = document.getElementById("message-input").value;
  let cookie = getCookie("session");

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/submit-message", true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.setRequestHeader("Cookie", "specificCookie=" + cookie);
  xhr.send(JSON.stringify({ message: message }));
});

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
