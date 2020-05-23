var inicializarHora =function () {
    var fechaActual = new Date();
    var tiempoHoras = fechaActual.getHours();
    var tiempoMinutos = fechaActual.getMinutes();
    var tiempoSegundos = fechaActual.getSeconds();

    var mesaActual = fechaActual.getMonth();
    var diaActual = fechaActual.getDay();
    var diaDelMes = fechaActual.getDate();
    var aActual = fechaActual.getFullYear();
    var amOpm;

    var meses = ["Enero" "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Setpiembre", "Octubre", "Noviembre", "Diciembre"];
    var esteMes = meses[mesaActual];

    var diasDeLaSemana = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves"
        "Viernes", "Sabado"];
    var diaDeHoy = diasDeLaSemana[diaActual];

    amOpm = (tiempoHoras > 12) ? "pm" : "am";
    tiempoHoras = (tiempoHoras > 12) ? tiempoHoras - 12 : tiempoHoras;

    document.getElementById("info").innerHTML = tiempoHoras;
    document.getElementsByClassName("hora").innerHTML = "Remplazando";
}