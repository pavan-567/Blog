const currentUser = JSON.parse(
  document.getElementById("present_user").textContent
);

console.log(currentUser);

function formatAMPM(date) {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][new Date().getDay()];
  let ampm = hours >= 12 ? 'p.m.' : 'a.m.';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  let strTime = hours + ':' + minutes + ' ' + ampm;
  return [strTime, weekday];
}

if (currentUser.trim() !== "") {
  console.log(currentUser, typeof currentUser, currentUser.length);
  console.log("INSIDE HERE!");

  // const chatOnlineSocket = new WebSocket(
  //   `ws://localhost:8000/ws/status/`
  // );
  const chatOnlineSocket = new WebSocket(
    `ws://${window.location.host}/ws/status/`
  );

  chatOnlineSocket.onopen = function (e) {
    console.log("WEBSOCKET CONNECTED!");
    chatOnlineSocket.send(
      JSON.stringify({
        username: currentUser,
        type: "open",
      })
    );
  };

  chatOnlineSocket.onmessage = function (e) {
    console.log(e.data);
    let data = JSON.parse(e.data);
    const { users: activeUsers, all_users: totalUsers } = data;

    const onlineContainer = document.querySelector(".online-container");
    const profileStatus = document.querySelector(".profile-status");

    if (onlineContainer && profileStatus) {
      const receiver = JSON.parse(document.getElementById('json-receiver-username').textContent);
      console.log(receiver);
      if (data.username !== currentUser) {
        if (data.online_status) {
          onlineContainer.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" style="color:greenyellow;" fill="currentColor" class="bi bi-circle-fill" viewBox="0 0 16 16">
                <circle cx="8" cy="8" r="8"/>
              </svg>
            `;
          profileStatus.innerText = "Online";

        } else {
          onlineContainer.innerHTML = `
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-circle-fill" viewBox="0 0 16 16">
                <circle cx="8" cy="8" r="8"/>
              </svg>
            `;
          // profileStatus.innerText = `Last Seen ${formatAMPM(new Date)[1]} at ${formatAMPM(new Date)[0]}`;
          profileStatus.innerText = `Last Seen Today at ${formatAMPM(new Date)[0]}`;
        }
      }
    }

    function enableOnlinePerPerson(container, status) {
      container.innerHTML = `
            <input type="hidden" value="${
              container.firstElementChild.value
            }" />
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" style="${
              status === "online" ? "color:greenyellow" : ""
            };" fill="currentColor" class="bi bi-circle-fill" viewBox="0 0 16 16">
                <circle cx="8" cy="8" r="8"/>
              </svg>
            `;
    }

    function checkOnline(container, users) {
      for (let user of users) {
        if (user === container.firstElementChild.value) {
          enableOnlinePerPerson(container, "online");
          break;
        } else {
          enableOnlinePerPerson(container, "offline");
        }
      }
    }

    function insertAllOnlineOffline(containerActive, containerInactive, users) {
      containerActive.innerText = ''
      containerInactive.innerText = ''

      for (let user of users) {
        const div = document.createElement("div");
        const a = document.createElement('a');

        a.innerText = user.username;

        a.setAttribute('href', user.profileLink);
        a.setAttribute('style', 'text-decoration: none; color: black;');

        div.append(a);
        
        if (user.active) {
          containerActive.appendChild(div);
        } else {
          containerInactive.appendChild(div);
        }
      }
    }

    const activeUsersContainer = document.getElementById("active-users");
    const inactiveUsersContainer =
      document.getElementById("inactive-users");

    insertAllOnlineOffline(
      activeUsersContainer,
      inactiveUsersContainer,
      totalUsers
    );

    const userContainer = document.querySelector(".userStatus")

    // insertOnline(userContainer, activeUsers);

    const onlineHomeContainer = document.querySelectorAll(
      ".online-home-container"
    );

    function insertOnline(userContainer, users) {
      for(let user of users) {
        const p = document.createElement('p');
        p.innerText = user;
        activeUsersContainer.appendChild(p);
      }
    }

    if (onlineHomeContainer.length > 0) {
      for (let container of onlineHomeContainer) {
        checkOnline(container, activeUsers);
      }
    }
  };

  chatOnlineSocket.onclose = function (e) {
    console.log("SOCKET CLOSED!");
  };

  window.addEventListener("beforeunload", (event) => {
    chatOnlineSocket.send(
      JSON.stringify({
        username: currentUser,
        type: "offline",
      })
    );
  });
}
