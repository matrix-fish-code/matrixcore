document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const userInput = document.getElementById('user-input').value;
    const responseDiv = document.getElementById('response');

    // Limpar o campo de entrada após o envio
    document.getElementById('user-input').value = '';

    // Adiciona uma mensagem indicando que está esperando a resposta
    responseDiv.classList.add('waiting');
    responseDiv.innerHTML = 'Esperando a resposta...';

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
            responseDiv.classList.remove('waiting');
            responseDiv.innerHTML = `Resposta: ${data.response}`; // Exibe a resposta
        } else {
            responseDiv.classList.remove('waiting');
            responseDiv.innerHTML = 'Erro: Nenhuma resposta recebida.';
        }
    })
    .catch(error => {
        responseDiv.classList.remove('waiting');
        responseDiv.innerHTML = 'Erro ao processar o prompt';
    });
});

