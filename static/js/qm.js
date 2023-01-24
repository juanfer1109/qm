inscribirse = () => {
    var x = document.getElementById("inscribirse");
    var y = document.getElementById("btn-inscribir");
    var z = document.getElementById("btn-cancelar");
    if (x.style.display === "none") {
        x.style.display = "flex";
        z.style.display = "flex";
    } else {
        x.style.display = "none";
        z.style.display = "none";
    }
    if (y.style.display === "none") {
        y.style.display = "block";
    } else {
        y.style.display = "none";
    }
}