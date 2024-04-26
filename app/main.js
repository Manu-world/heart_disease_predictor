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

    for (let [key, value] of formData.entries()) {
      if (
        key === "thal" ||
        key === "slope" ||
        key === "ca" ||
        key === "exang" ||
        key === "fbs" ||
        key === "restecg" ||
        key === "cp" ||
        key === "sex"
      ) {
        // Add other select fields as needed
        formData.set(key, parseInt(value));
      }
    }

    fetch("https://heart-disease-predictor-6.onrender.com/check", {
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
  const messageInput = document.getElementById("message-input");

  messageForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const messageText = messageInput.value.trim();
    if (!messageText) return; // Don't send empty messages

    // Send the message to the chatbot
    fetch("https://heart-disease-predictor-6.onrender.com/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: messageText }),
      credentials: "include", // Include cookies in the request
    })
      .then((response) => response.json())
      .then((data) => {
        // Append the chatbot's response to the chat history
        const responseText = data.response.join(" "); // Assuming response is an array of strings
        chatHistory.innerHTML += `<p>Chatbot: ${responseText}</p>`;
      })
      .catch((error) => {
        console.error("Error:", error);
        chatHistory.innerHTML += `<p>Error: ${error.message}</p>`;
      });

    // Clear the input field
    messageInput.value = "";
  });
});
