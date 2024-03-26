const roomName = JSON.parse(
  document.getElementById("json-room-name").textContent
);
const userName = JSON.parse(
  document.getElementById("json-username").textContent
);
const userEmail = JSON.parse(document.getElementById("json-email").textContent);
const userId = JSON.parse(document.getElementById("json-id").textContent);

const receiver = JSON.parse(
  document.getElementById("json-receiver-username").textContent
);

console.log(roomName, userName, userEmail, userId);

// const chatSocket = new WebSocket(`ws://localhost:8000/ws/${Number(userId)}/`);
const chatSocket = new WebSocket(
  `ws://${window.location.host}/ws/${Number(userId)}/`
);

function formatAMPM(date) {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let ampm = hours >= 12 ? "p.m." : "a.m.";
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? "0" + minutes : minutes;
  let strTime = hours + ":" + minutes + " " + ampm;
  console.log(strTime);
  return strTime;
}

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  const { message, username, room, image_url } = data;
  console.log(data, data.message);
  let html = null;
  if (username === userName) {
    html = `
         <div class="d-flex sender justify-content-end p-2 me-2 align-items-center">
                  <div class="d-flex bg-warning p-2 text-black" style="border-radius: 10px;">
                     <p class="px-2 py-3" style="min-width: 200px;">${
                       data.message
                     }</p>
                     <p class="align-self-end" style="font-size: 12px;">${formatAMPM(new Date())[0]}</p>
                  </div>
               </div>
         `;
  } else {
    html = `
         <div class="d-flex receiver justify-content-start p-2 ms-2 align-items-center">
                  <div class="d-flex bg-secondary p-2 text-white" style="border-radius: 10px;">
                     <p class="px-2 py-3" style="min-width: 200px; border-radius: 10px;">${
                       data.message
                     }</p>
                     <p class="align-self-end" style="font-size: 12px;">${formatAMPM(new Date())[0]}</p>
                  </div>
               </div>
         `;
  }
  const div = document.createElement("div");
  // div.setAttribute('class', 'my-3');
  console.log(html);
  div.innerHTML = html;

  document.querySelector(".endHr").insertAdjacentElement("beforebegin", div);
  scrollToBottom();
};

chatSocket.onclose = function (e) {
  console.log("SOCKET CLOSED!");
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  // e.preventDefault();
  console.log("BUTTON CLICKED!");
  const msgContainer = document.querySelector("#chat-message-input");
  const msg = msgContainer.value;

  if (msg.length === 0) return;

  chatSocket.send(
    JSON.stringify({
      message: msg,
      name: userName,
      mail: userEmail,
      room: roomName,
      receiver: userName,
    })
  );

  msgContainer.value = "";

  return false;
};

function scrollToBottom() {
  // LOL!
  const chatContainer = document.getElementById("message-container");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

scrollToBottom();
