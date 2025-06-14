document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-comentario");
  const listado = document.getElementById("comentarios-listado");
  const errorDiv = document.getElementById("error-comentario");
  

  const cargarComentarios = () => {
    fetch(`/api/comentarios/${actividadId}`)
      .then(response => {
          if (!response.ok) {
            throw new Error("Hubo un problema al intentar establecer una conexión")
          }
          return response.json() // parseamos
        })
      .then(data => {
        listado.innerHTML = data.map(c => 
          `<p><strong>${c.fecha}</strong> - <em>${c.nombre}</em>: ${c.texto}</p>`
        ).join('');
      });
  }

  form.addEventListener("submit", e => {
    e.preventDefault();
    errorDiv.textContent = "";

    const formData = new FormData(form);
    const payload = {
      nombre: formData.get("nombre").trim(),
      texto: formData.get("texto").trim()
    };

    if (payload.nombre.length < 3 || payload.nombre.length > 80) {
      errorDiv.textContent = "El nombre debe tener entre 3 y 80 caracteres.";
      return;
    }
    if (payload.texto.length < 5) {
      errorDiv.textContent = "El comentario debe tener al menos 5 caracteres.";
      return;
    }

    fetch(`/api/comentarios/${actividadId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(resp => {
      if (resp.ok) {
        form.reset();
        cargarComentarios();
      } else {
        errorDiv.textContent = resp.error || "Error al agregar comentario.";
      }
    });
  });

  cargarComentarios();
});