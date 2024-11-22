const apiUrl = "http://localhost:3000";

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const roomId = generateRoomId();

  // Save user data
  await fetch(`${apiUrl}/save-user`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password, roomId }),
  });

  // Redirect to chatroom
  window.location.href = `chatroom.html?roomId=${roomId}`;
});

document.getElementById("send-button")?.addEventListener("click", async () => {
  const roomId = new URLSearchParams(window.location.search).get("roomId");
  const message = document.getElementById("message-input").value;

  // Save message
  await fetch(`${apiUrl}/save-message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ roomId, sender: "Me", message }),
  });

  displayMessage(message, "sent");
  document.getElementById("message-input").value = "";
});

function displayMessage(message, type) {
  const messagesDiv = document.getElementById("messages");
  const messageDiv = document.createElement("div");
  messageDiv.textContent = message;
  messagesDiv.appendChild(messageDiv);
}

function generateRoomId() {
  return Math.random().toString(36).substring(2, 8);
}
