function inscribirse() {
    var x = document.getElementById("inscribirse");
    var y = document.getElementById("btn-inscribir");
    if (x.style.display === "none") {
        x.style.display = "flex";
    } else {
        x.style.display = "none";
    }
    if (y.style.display === "none") {
        y.style.display = "block";
    } else {
        y.style.display = "none";
    }
}