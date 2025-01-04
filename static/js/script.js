document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const userInput = document.getElementById('user-input').value;
    const responseDiv = document.getElementById('response');

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Exibe a resposta recebida da API no frontend
        if (data.response) {
            responseDiv.innerHTML = `Resposta: ${data.response}`;
        } else {
            responseDiv.innerHTML = 'Erro: Nenhuma resposta recebida.';
        }
    })
    .catch(error => {
        responseDiv.innerHTML = 'Erro ao processar o prompt';
    });
});

