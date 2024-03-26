const defaultWallpaper = document.getElementById("default-wallpaper-form");

const chatWallpaper = document.getElementById("chat-wallpaper-form");

const message = document.getElementById("message-form");

function formValid(form) {
  form.addEventListener("submit", (e) => {
    if (!form.checkValidity()) e.preventDefault();
    form.classList.add("was-validated");
  });
}
formValid(defaultWallpaper);
formValid(chatWallpaper);
formValid(message);
