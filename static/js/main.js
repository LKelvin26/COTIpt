

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('moneyInput').addEventListener('input', function(e) {
        // Permite números y un punto decimal
        let valueEntered = this.value;
        if(valueEntered.match(/[^0-9.]/g)){
           
            this.value = valueEntered.replace(/[^0-9.]/g, '');

        
            if ((this.value.match(/\./g) || []).length > 1) {
                this.value = this.value.replace(/\.(?=\d*\.)/g, '');
            }
        }

       
        
        convertCurrency();
    });
});

function convertCurrency() {
    
    var amount = document.getElementById('moneyInput').value; // Asumiendo que este es el input para el monto en pesos
    var data = new FormData();
    data.append('amount', amount);

    

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

    
    xhttp.open("POST", "/usdtomxn/", true);
    
    xhttp.send(data);
}
