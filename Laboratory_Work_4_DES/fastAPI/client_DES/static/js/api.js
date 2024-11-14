console.log("api.js loaded successfully");

async function handle_encrypt_button_click() {
  const text = document.getElementById('text').value;
  const key = document.getElementById('key').value;

  console.log('Encrypt Button Clicked:');
  console.log('Text:', text);
  console.log('Key:', key);

  const taskSelector = document.getElementById('task');
  const selectedTask = taskSelector.value;

  let endpoint = '/api/encrypt'; // Default endpoint for encryption
  let requestBody = {
    "message": text,
    "key": key
  };

  if (selectedTask === 'task') {
    // For Task 2.10, send specific data as per TaskBody model
    endpoint = '/api/task';
    const round_i = parseInt(document.getElementById('text').value); // Assuming you have a field for round_i
    const S_BOXED_R_i_1 = document.getElementById('key_hidden').value; // Same for S_BOXED_R_i_1
    const L_i_1 = document.getElementById('key').value; // Same for L_i_1

    // Prepare the request body for TaskBody model
    requestBody = {
      "round_i": round_i,
      "S_BOXED_R_i_1": S_BOXED_R_i_1,
      "L_i_1": L_i_1
    };

    console.log(requestBody)
  }

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  });
  console.log(response)


  handleResponse(response);
}

async function handle_decrypt_button_click() {
  const text = document.getElementById('text').value;
  const key = document.getElementById('key').value;

  console.log('Decrypt Button Clicked:');
  console.log('Text:', text);
  console.log('Key:', key);

  const response = await fetch('/api/decrypt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        "message": text,
        "key": key,
    })
  });

  handleResponse(response);
}

async function handleTaskChange() {
    const taskSelector = document.getElementById('task');
    const selectedTask = taskSelector.value;

    const messageLabel = document.querySelector('label[for="text"]');
    const keyLabel = document.querySelector('label[for="key"]');
    const inputsContainer = document.querySelector('.app_input_hidden');

    const button = document.getElementById('encrypt');

    // Reset all fields when task changes
    document.getElementById('text').value = "";
    document.getElementById('key').value = "";
    document.getElementById('result').value = "";
    document.getElementById('key_hidden').value = "";

    // Hide error message
    const errorMessageDiv = document.getElementById('error-message');
    errorMessageDiv.style.display = 'none';

    if (selectedTask === 'encrypt/decrypt') {
        // Reset labels to default
        messageLabel.textContent = 'Message:';
        keyLabel.textContent = 'Key:';
        inputsContainer.style.display = "none";  // Hide additional inputs for encryption/decryption
        document.getElementById('key_hidden').value = "";
        // Show the encrypt/decrypt buttons
        document.getElementById('encrypt').style.display = 'inline-block';
        document.getElementById('decrypt').style.display = 'inline-block';
        button.textContent = "Encrypt";
    }
    else if (selectedTask === 'task') {
        // Change the labels for Task 2.10
        messageLabel.textContent = 'Round_i:';
        keyLabel.textContent = 'L_(i-1):';
        inputsContainer.style.display = "grid";  // Show additional inputs for Task 2.10

        // Hide the decrypt button
        document.getElementById('decrypt').style.display = 'none';

        button.textContent = "Perform";
    }
}


async function handleResponse(response) {
    const errorMessageDiv = document.getElementById('error-message');

    if (response.ok) {
        errorMessageDiv.style.display = 'none';
        response.json().then(data => {
            if (data.content.encrypted_message) {
                document.getElementById('result').value = data.content.encrypted_message;
            }
            if (data.content.decrypted_message) {
                document.getElementById('result').value = data.content.decrypted_message;
            }
            if (data.content.R_i) {
                document.getElementById('result').value = data.content.R_i;
            }
        });
    }
    else {
        document.getElementById('result').value = '';
        const data = await response.json();
        errorMessageDiv.querySelector('.error-title').textContent = "ERROR " + data.status_code;
        errorMessageDiv.querySelector('.error-body').textContent = data.content.message;
        if (data.details) {
            errorMessageDiv.querySelector('.error-details').textContent = "Details: " + data.details;
        }
        errorMessageDiv.style.display = 'flex';
        setTimeout(() => {
            errorMessageDiv.style.display = 'none';
        }, 7000);
    }
}
