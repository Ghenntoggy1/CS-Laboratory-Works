console.log("api.js loaded successfully");

async function handle_encrypt_button_click() {
  const text = document.getElementById('text').value;
  const key = document.getElementById('key').value;

  console.log('Encrypt Button Clicked:');
  console.log('Text:', text);
  console.log('Key:', key);

  const response = await fetch('/api/encrypt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        "plain_text": text,
        "key": key,
    })
  });

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
        "cipher_text": text,
        "key": key,
    })
  });

  handleResponse(response);
}

async function handleResponse(response) {
    const errorMessageDiv = document.getElementById('error-message');

    if (response.ok) {
        errorMessageDiv.style.display = 'none';
        response.json().then(data => {
            if (data.encrypted_text) {
                document.getElementById('result').value = data.encrypted_text;
            }
            if (data.decrypted_text) {
                document.getElementById('result').value = data.decrypted_text;
            }
        });
    }
    else {
        document.getElementById('result').value = '';
        const data = await response.json();
        errorMessageDiv.querySelector('.error-title').textContent = "ERROR " + data.status_code;
        errorMessageDiv.querySelector('.error-body').textContent = data.message;
        if (data.details) {
            errorMessageDiv.querySelector('.error-details').textContent = "Details: " + data.details;
        }
        errorMessageDiv.style.display = 'flex';
        setTimeout(() => {
            errorMessageDiv.style.display = 'none';
        }, 7000);
    }
}