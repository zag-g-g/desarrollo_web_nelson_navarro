const poblarRegiones = () => {
  let regionSelect = document.getElementById("select-region");
  for (const region in region_comuna) {
    let option = document.createElement("option");
    option.value = region;
    option.text = region;
    regionSelect.appendChild(option);
  }
};

const updateComunas = () => {
  let regionSelect = document.getElementById("select-region");
  let comunaSelect = document.getElementById("select-comuna");
  let selectedRegion = regionSelect.value;
  
  comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
  
  if (region_comuna[selectedRegion]) {
      region_comuna[selectedRegion].forEach(comuna => {
          let option = document.createElement("option");
          option.value = comuna;
          option.text = comuna;
          comunaSelect.appendChild(option);
      });
  }
};

let contactCount = 0;
const maxContacts = 5;

const revisaCheck = (element) => {
  const platformCheckboxes = document.querySelectorAll('input.platform-cb');
  const input = document.getElementById(element.name);

  if (element.checked) {
    input.style.display = "block";
    input.focus();
    contactCount++;
    if (contactCount >= maxContacts) platformCheckboxes.forEach(cb => !cb.checked && (cb.disabled = true));
  } else {
    input.style.display = "none";
    contactCount--;
    platformCheckboxes.forEach(cb => cb.disabled = false);
  }

  if (element.name === "otra-plataforma") {
    const extraPlatform = document.getElementById("plataforma-extra");
  
    if (element.checked && !document.getElementById("platform-name")) {
      const extraInput = document.createElement("input");
      extraInput.type = "text";
      extraInput.id = "nombre-otra-plataforma";
      extraInput.name = "nombre-otra-plataforma-id";
      extraInput.placeholder = "Nombre de la plataforma";
      extraPlatform.appendChild(extraInput);
    } else {
      const extraInput = document.getElementById("nombre-otra-plataforma");
      if (extraInput) {
        extraInput.remove();
      }
    }
  }
};

const revelarDesc = (element) => {
  inputOtroTema = document.getElementById("otro-tema-id");
  if (element.checked) {
    inputOtroTema.style.display = "block";
    inputOtroTema.focus();
  } else {
    inputOtroTema.style.display = "none";
    inputOtroTema.value = "";
  }
};

document.getElementById("select-region").addEventListener("change", updateComunas);


document.addEventListener('DOMContentLoaded', () => {
  poblarRegiones();
});
