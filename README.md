Algunas decisiones:

if (.trim() = '') revisar que no esté vacío o lleno de espacios.

input.focus() para ahorrar clicks al usuario

ternario: if (contactCount >=5) platformCheckboxes.forEach(cb => !cb.checked && (cb.disabled = true));
Posiblemente cambia style = "display: none;" a .hidden en un futuro.

return (!tema_extra_cb.checked || lengthValid);
Se descarta el caso en que el usuario escribe algo y lo envía sin tener seleccionada la checkbox gracias a la línea `inputOtroTema.value = ""` dentro del método `revelarDesc()` en `select.js`.

`window.scrollTo(0, 0)` para regresar al usuario al tope del formulario donde se encuentra el listado de  campos inválidos, en caso de haber cometido algún error.

Se dejaron las fechas en formato UTC predeterminado, para no producir errores a futuro.

A futuro, añadir:
- Íconos para las plataformas en el select de "Contactar por"
- .replace(/\s+/g, '-'): Reemplazar espacios con guiones en los nombres e id's.