// async function sendMessageToBot(message) {
//   const response = await fetch("http://localhost:8000/chat", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ text: message }),
//   });
//   const data = await response.json();
//   console.log(data.response);
// }

// // Example usage
// sendMessageToBot("Hello, chatbot!");

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("vitals-form");
  const resultsDiv = document.getElementById("results");

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(form); // Collect form data

    fetch("https://heart-disease-predictor-7.onrender.com/check", {
      method: "POST",
      body: formData, // Send form data
    })
      .then((response) => response.json()) // Parse the response as JSON
      .then((data) => {
        // Append the response to the results div
        resultsDiv.innerHTML = `<p>${data.response}</p>`;
      })
      .catch((error) => {
        console.error("Error:", error);
        resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const messageForm = document.getElementById("message-form");
  const chatHistory = document.getElementById("chat-history");
  const resultsDiv = document.getElementById("results");
  const messageInput = document.getElementById("message-input");
  const prediction = document.getElementById("context");
  const session_id = document.getElementById("session_id");

  messageForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const messageText = messageInput.value.trim();
    const sessionID = session_id.value.trim();
    const context = prediction.value.trim();
    if (!messageText) return; // Don't send empty messages
    chatHistory.innerHTML += `<p class='bg-green-500 text-white rounded-lg p-2 max-w-xs'>You: ${messageText}</p>`;

    // Send the message to the chatbot
    fetch("https://heart-disease-predictor-7.onrender.com/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: messageText,
        context: context,
        session_id: sessionID,
      }),
      credentials: "include", // Include cookies in the request
    })
      .then((response) => response.json())
      .then((data) => {
        // Append the chatbot's response to the chat history

        const responseText = data.response.join(" "); // Assuming response is an array of strings
        chatHistory.innerHTML += `<p class="bg-blue-500 text-white rounded-lg p-2 max-w-xs">Chatbot: ${responseText}</p>`;
      })
      .catch((error) => {
        console.error("Error:", error);
        chatHistory.innerHTML += `<p class="bg-blue-500 text-white rounded-lg p-2 max-w-xs">Error: ${error.message}</p>`;
      });

    // Clear the input field
    messageInput.value = "";
  });
});
