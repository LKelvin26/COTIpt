

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('moneyInput').addEventListener('input', function(e) {
        // Permite números y un punto decimal
        let valueEntered = this.value;
        if(valueEntered.match(/[^0-9.]/g)){
            // Remueve caracteres no numéricos excepto el punto
            this.value = valueEntered.replace(/[^0-9.]/g, '');

            // Asegura que solo haya un punto decimal
            if ((this.value.match(/\./g) || []).length > 1) {
                this.value = this.value.replace(/\.(?=\d*\.)/g, '');
            }
        }

        // Llama a tu función aquí
        
        convertCurrency();
    });
});

function convertCurrency() {
    // Asignamos variables a guardar
    var amount = document.getElementById('moneyInput').value; // Asumiendo que este es el input para el monto en pesos
    var data = new FormData();
    data.append('amount', amount);

    // Aquí podrías agregar más datos al FormData si es necesario
    // Por ejemplo, especificar la moneda de origen y destino si el endpoint lo requiere

    // Obtiene el token CSRF de una manera similar a como lo haces en tu ejemplo
    

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            console.log(response); // Aquí puedes manejar la respuesta

            // Suponiendo que la respuesta incluye el valor convertido en 'valorUSD'
            if (response.success) {
                // Actualiza el DOM con las tasas de cambio
                document.getElementById('rateSource1').textContent = response.valorMXNER + ' MXN';
                document.getElementById('rateSource2').textContent = response.valorMXNOE + ' MXN';
            } else {
                // Manejo de errores
                alert('Hubo un error en la conversión de la moneda');
                // Actualizar el DOM para indicar que hubo un error
                document.getElementById('rateSource1').textContent = 'Error al cargar';
                document.getElementById('rateSource2').textContent = 'Error al cargar';
            }
        }
    };

    // Aquí especifica la URL del endpoint que realiza la conversión de divisas
    xhttp.open("POST", "/usdtomxn/", true);
    
    xhttp.send(data);
}
