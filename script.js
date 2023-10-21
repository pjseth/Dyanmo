document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('evacuation-form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const address = document.getElementById('address').value;

        fetch('/calculate_evacuation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ address: address })
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `Evacuation Capacity: ${data.evacuation_capacity}`;
        })
        .catch(error => {
            resultDiv.innerHTML = 'Error calculating evacuation capacity.';
        });
    });
});