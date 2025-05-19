**Tarea 1:**

if (.trim() = '') revisar que no esté vacío o lleno de espacios.

input.focus() para ahorrar clicks al usuario

ternario: if (contactCount >=5) platformCheckboxes.forEach(cb => !cb.checked && (cb.disabled = true));
Posiblemente cambia style = "display: none;" a .hidden en un futuro.

return (!tema_extra_cb.checked || lengthValid);
Se descarta el caso en que el usuario escribe algo y lo envía sin tener seleccionada la checkbox gracias a la línea `inputOtroTema.value = ""` dentro del método `revelarDesc()` en `select.js`.

`window.scrollTo(0, 0)` para regresar al usuario al tope del formulario donde se encuentra el listado de  campos inválidos, en caso de haber cometido algún error.

A futuro, se piensa añadir:
- Pequeños íconos para las plataformas en el select de "Contactar por"
- Utilizar .replace(/\s+/g, '-') para reemplazar espacios con guiones en los nombres e id's.

**Tarea 2:**

Para probar la tarea:

-Considerar el archivo requirements.txt para los requerimientos de liberías de Python y demases.

-En vez de utilizar el archivo tarea2.sql completo, se hace Run al archivo database/init_db.py
-Posteriormente, se hace Run a todo el archivo database/region-comuna.sql

Si algo falla, puede intentar correr create.user.sql antes de las instrucciones, y algunas de las primeras consultas en tarea2.sql, mientras estas no sean para crear tablas (CREATE TABLE)

En el peor de los casos, probar con tarea2.sql en vez de init_db.py, y/o contactar en lo posible por U-cursos u otro medio.

---

Se dejaron las fechas en formato UTC predeterminado, para no producir errores a futuro.

Jinja2 funciona con autoescaping, por lo que se omite usar la función escape(), por ejemplo, en los request.form.get()
En algunos templates de HTML, se hizo una excepción utilizando { ... | escape } para las fechas, asumiendo que un usuario no puede inyectar HTML mediante esa vía (en caso contrario, se buscará una alternativa en el futuro para manejar aquella entrada)

En el enunciado se menciona "En caso de errores de validación, debe mantener visible el formulario con los mensajes de validación correspondientes". Si bien no se especifica si hay que guardar la información del usuario o recargar el formulario vacío, es evidente que lo más adecuado es mantener la información que ingresó el usuario y así pueda saber qué modificar. Sin embargo, se consideró que esto ya se hacía en parte con la validación mediante js en el Frontend, pues ahí la información no se recarga y se mantiene. Lo mismo sucede si se presiona el botón "No, no estoy segur@, (...)". También se muestran los mensajes de error, tanto para la validación en el Frontend como en el Backend.
Aún así, en la futura entrega se implementará el guardado de datos para el caso de errores en Backend, dado que actualmente los métodos investigados solían escapar de los contenidos base del curso, y no había suficiente tiempo para consultar si se podían utilizar ciertas funciones o librerías.

Se movió el mensaje de agradecimiento del formulario a la portada, nuevamente por mención del enunciado: "Si todo resulta bien, debe volver a la página de inicio informando un mensaje apropiado". Se supuso que el mensaje apropiado era el mismo mensaje que en el enunciado de la Tarea 1.

Para index.html, se considera como portada única la primera imagen ingresada por el usuario en el formulario. Las demás imágenes se pueden ver en listado_actividades.html y detalle_actividad/<>.html

En la siguiente entrega, se moverá el script con region_comuna de informar_actividad.html a un archivo .js por seguridad ante inyecciones.

**Importante*: Durante todo el desarrollo de la Tarea 2, no se ocupó una carpeta "flask_app", todos los archivos estaban inicialmente en una carpeta "T2", incluyendo el virtual environment 'venv' de Python. Antes de la entrega, se decidió seguir el formato y mover todos los archivos a una nueva carpeta flask_app, pero no se pudo mover el venv manualmente. Al crear uno nuevo e intentar realizar 'pip install' de las liberías necesarias, se mencionó que podía haber colisiones con las librerías en el venv fuera de flask_app, por lo que se decidió dejar la tarea así. Si sucede algún error, por favor probar los archivos (en sus respectivas carpetas) en una carpeta de nombre 'T2' que las contenga. Nuevamente, en el peor de los casos, por favor contactar via U-cursos.

También salieron varios errores de este tipo:

warning: in the working copy of 'flask_app/app.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'flask_app/database/create_user.sql', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'flask_app/database/db.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'flask_app/database/region-comuna.sql', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'flask_app/database/tarea2.sql', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'flask_app/static/css/styles.css', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'flask_app/static/js/validation.js', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'flask_app/templates/informar_actividad.html', LF will be replaced by CRLF the next time Git touches it       
warning: in the working copy of 'flask_app/utils/validations.py', LF will be replaced by CRLF the next time Git touches it

warning: in the working copy of 'venv/Lib/site-packages/zipp/__init__.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'venv/Lib/site-packages/zipp/_functools.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'venv/Lib/site-packages/zipp/compat/overlay.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'venv/Lib/site-packages/zipp/compat/py310.py', LF will be replaced by CRLF the next time Git touches it       
warning: in the working copy of 'venv/Lib/site-packages/zipp/glob.py', LF will be replaced by CRLF the next time Git touches it


Se intentó borrar los venv