const validateSector = (sector) => {
  return sector.trim().length <= 100;
}

const validateName = (name) => {
  return name && name.trim().length <= 200;
}

const validateEmail = (email) => {
  if (!email) return false;
  email = email.trim()
  let lengthValid = email.length <= 100;
  let re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  let formatValid = re.test(email);

  return lengthValid && formatValid;
};

const validateNumCelular = (num_celular) => {
  if (!num_celular) return true;
  num_celular = num_celular.trim()
  if (num_celular == '') return true

  let re = /^\+\d{3}\.\d{8}$/;
  let formatValid = re.test(num_celular);

  return formatValid;
};

const validateContactos = (contactos) => {
  for (cb of contactos) {
    if (cb.checked) {
      plat = document.getElementById(cb.name);
      val = plat.value.trim();
      lengthValid = (val.length >= 4) && (val.length <= 50);

      if (!lengthValid) return false;


      if (plat.id === "whatsapp") {
        const re_num = /^\+?[1-9]\d{1,14}$/;
        const formatValid_num = re_num.test(val);

        const re_url = /^(https?:\/\/)?(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/send/i;
        const formatValid_url = re_url.test(val);
        
        if (!(formatValid_num || formatValid_url)) return false;
      }
      if (plat.id === "telegram") {
        const re_num = /^\+?[1-9]\d{1,14}$/;
        const formatValid_num = re_num.test(val);

        const re_username = /^@[a-zA-Z0-9_]{5,32}$/;
        const formatValid_username = re_username.test(val);
      
        const re_url = /^(https?:\/\/)?(t\.me|telegram\.me)\/[a-zA-Z0-9_]{5,32}$/i;
        const formatValid_url = re_url.test(val);

        if (!(formatValid_num || formatValid_username || formatValid_url)) return false;
      }
      if (plat.id === "instagram") {
        const re_username = /^@?[a-zA-Z0-9._]{1,30}$/;
        const formatValid_username = re_username.test(val);
      
        const re_url = /^(https?:\/\/)?(www\.)?instagram\.com\/[a-zA-Z0-9._]{1,30}$/i;
        const formatValid_url = re_url.test(val);
      
        if (!(formatValid_username || formatValid_url)) return false;
      }
      if (plat.id === "x") {
        const re_username = /^@?[a-zA-Z0-9_]{1,15}$/;
        const formatValid_username = re_username.test(val);
      
        const re_url = /^(https?:\/\/)?(www\.)?(twitter\.com|x\.com)\/[a-zA-Z0-9_]{1,15}$/i;
        const formatValid_url = re_url.test(val);
      
        if (!(formatValid_username || formatValid_url)) return false;
      }
      if (plat.id === "tiktok") {
        const re_username = /^@?[a-zA-Z0-9_]{2,24}$/;
        const formatValid_username = re_username.test(val);
      
        const re_url = /^(https?:\/\/)?(www\.)?tiktok\.com\/@([a-zA-Z0-9_]{2,24})$/i;
        const formatValid_url = re_url.test(val);
      
        if (!(formatValid_username || formatValid_url)) return false;
      }
    }
  }
  return true;
};


const validateFechaInicio = (fecha_hora) => {
  if (!fecha_hora) return false;
  const fechaObj = new Date(fecha_hora);
  return fechaObj instanceof Date && !isNaN(fechaObj);
};

const validateFechaTermino = (fecha_inicio, fecha_termino) => {
  if (fecha_termino) {
    const fechaInicioObj = new Date(fecha_inicio);
    const fechaTerminoObj = new Date(fecha_termino);

    if (isNaN(fechaTerminoObj) || (fechaInicioObj >= fechaTerminoObj)) return false;
  }
  return true;
};

const validateTemas = (temas_cb) => {
  for (cb of temas_cb) {
    if (cb.checked) return true;
  }
  return false;
};

const validateTemaExtra = (tema) => {
  const tema_extra_cb = document.getElementById("otro-tema-cb-id");
  const lengthValid = (tema.trim().length >= 3) && (tema.trim().length <= 15);

  return (!tema_extra_cb.checked || lengthValid);
}


const validateFiles = (files) => {
  if (!files) return false;

  // validación del número de archivos
  let lengthValid = 1 <= files.length && files.length <= 5;

  // validación del tipo de archivo
  let typeValid = true;

  for (const file of files) {
    // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
  }

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && typeValid;
};

const validateSelect = (select) => {
  if (!select || select === "") {
    return false;
  }
  return true;
};

const volverPortada = (ruta) => {
  window.location.href = ruta;
}

const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.forms["myForm"];
  let region = myForm["select-region"].value;
  let comuna = myForm["select-comuna"].value;
  let sector = myForm["sector"].value;
  let nombre = myForm["nombre"].value;
  let email = myForm["email"].value;
  let num_celular = myForm["phone"].value;
  let contactos_cb = document.querySelectorAll('.platform-cb');
  let dia_hora_inicio = myForm["dia-hora-inicio"].value;
  let dia_hora_termino = myForm["dia-hora-termino"].value;
  let temas_cb = document.querySelectorAll('.tema-cb');
  let tema = myForm["otro-tema"].value;
  

  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // lógica de validación
  if (!validateSelect(region)) {
    setInvalidInput("Región");
  }
  if (!validateSelect(comuna)) {
    setInvalidInput("Comuna");
  }
  if (!validateSector(sector)) {
    setInvalidInput("Sector");
  }
  if (!validateName(nombre)) {
    setInvalidInput("Nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validateNumCelular(num_celular)) {
    setInvalidInput("Número de celular");
  }
  if (!validateContactos(contactos_cb)) {
    setInvalidInput("Contactos");
  }
  if (!validateFechaInicio(dia_hora_inicio)) {
    setInvalidInput("Día y hora de inicio");
  } else if (!validateFechaTermino(dia_hora_inicio, dia_hora_termino)) {
    setInvalidInput("Día y hora de término");
  }
  if (!validateTemas(temas_cb)) {
    setInvalidInput("Temas");
  }
  if (!validateTemaExtra(tema)) {
    setInvalidInput("Tema extra");
  }


  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación y regresar al inicio del formulario
    validationBox.hidden = false;
    window.scrollTo(0, 0);
  } else {
    // Ocultar el formulario
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText = "¿Está segur@ que desea agregar esta actividad?";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    // Agregar botones para enviar el formulario o volver
    let submitButton = document.createElement("button");
    submitButton.innerText = "Sí, estoy segur@";
    submitButton.style.marginRight = "10px";
    submitButton.type = "button";
    submitButton.addEventListener("click", () => {
    myForm.submit();
    });

    let backButton = document.createElement("button");
    backButton.innerText = "No, no estoy segur@, quiero volver al formulario";
    backButton.addEventListener("click", () => {
      // Mostrar el formulario nuevamente
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  }
};






let fotosCount = 1;
const maxFotos = 5;
const addFotoBtn = document.getElementById("add-foto-btn");
const fotosContainer = document.getElementById("fotos-id");

const revelarAddFoto = () => {
  const allFotos = document.querySelectorAll('.foto-input');
  const allSelected = Array.from(allFotos).every(foto => foto.files.length > 0);
  if (allSelected) {
    addFotoBtn.style.display = '';
  } else {
    addFotoBtn.style.display = 'none';
  }
};

const addFoto = () => {
  if (fotosCount >= maxFotos) {
    return;
  }
  const newFoto = document.createElement("input");
  newFoto.type = "file";
  newFoto.name = "fotos[]";
  newFoto.id = `foto-id-${fotosCount}`;
  newFoto.className = "foto-input";
  newFoto.accept = "image/*,.pdf";
  newFoto.addEventListener("change", revelarAddFoto);
  fotosContainer.appendChild(newFoto);
  fotosCount++;
  addFotoBtn.style.display = 'none';
};


addFotoBtn.addEventListener("click", addFoto);
let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);

window.onload = () => {
  const inicio = document.getElementById('dia-hora-inicio');
  const termino = document.getElementById('dia-hora-termino');
  const now = new Date();
  inicio.value = now.toISOString().slice(0, 16);
  now.setHours(now.getHours() + 3);
  termino.value = now.toISOString().slice(0, 16);
}