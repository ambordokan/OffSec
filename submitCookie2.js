let submitButton = document.getElementById("submit-button");

submitButton.addEventListener("click", function() {
  let message = document.getElementById("message-input").value;

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/submit-message", true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify({ message: message, cookie: document.cookie }));
});
