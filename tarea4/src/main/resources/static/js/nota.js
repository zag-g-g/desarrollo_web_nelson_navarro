const evaluarActividad = (actividadId) => {
    const nota = prompt("Ingrese su nota (Entero entre 1 y 7):");
    const notaInt = parseInt(nota);

    if (!Number.isInteger(notaInt) || notaInt < 1 || notaInt > 7) {
        alert("Nota inválida.");
        return;
    }

    fetch("/api/notas/evaluar", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `actividadId=${actividadId}&nota=${notaInt}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Nota registrada. Nuevo promedio: " + data.promedio);
            location.reload();
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(err => console.error("Error al enviar su nota:", err));
}
