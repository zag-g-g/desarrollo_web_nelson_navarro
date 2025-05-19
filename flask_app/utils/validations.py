import re
import filetype
from datetime import datetime

def validate_sector(sector):
    if not sector:
        return True
    return len(sector.strip()) <= 100

def validate_name(name):
    return bool(name) and len(name.strip()) <= 200

def validate_email(email):
    if not email:
        return False
    
    email = email.strip()
    
    length_valid = len(email) <= 100
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    format_valid = bool(re.fullmatch(email_regex, email))
    
    return length_valid and format_valid

def validate_num_celular(num_celular):
    if not num_celular:
        return True
    
    num_celular = num_celular.strip()
    if num_celular == '':
        return True
    
    celular_regex = r'^\+\d{3}\.\d{8}$'
    return bool(re.fullmatch(celular_regex, num_celular))

def validate_contactos(contactos):
    for plataforma, valor in contactos.items():
        if not valor:
            continue
        valor = valor.strip()
        if not (4 <= len(valor) <= 50):
            return False

        if plataforma == "whatsapp":
            num_regex = r'^\+?[1-9]\d{1,14}$'
            url_regex = r'^(https?:\/\/)?(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/send'
            if not (re.fullmatch(num_regex, valor) or re.fullmatch(url_regex, valor, re.IGNORECASE)):
                return False

        elif plataforma == "telegram":
            num_regex = r'^\+?[1-9]\d{1,14}$'
            username_regex = r'^@[a-zA-Z0-9_]{5,32}$'
            url_regex = r'^(https?:\/\/)?(t\.me|telegram\.me)\/[a-zA-Z0-9_]{5,32}$'
            if not (re.fullmatch(num_regex, valor) or
                    re.fullmatch(username_regex, valor) or
                    re.fullmatch(url_regex, valor, re.IGNORECASE)):
                return False

        elif plataforma == "instagram":
            username_regex = r'^@?[a-zA-Z0-9._]{1,30}$'
            url_regex = r'^(https?:\/\/)?(www\.)?instagram\.com\/[a-zA-Z0-9._]{1,30}$'
            if not (re.fullmatch(username_regex, valor) or re.fullmatch(url_regex, valor, re.IGNORECASE)):
                return False

        elif plataforma == "x":
            username_regex = r'^@?[a-zA-Z0-9_]{1,15}$'
            url_regex = r'^(https?:\/\/)?(www\.)?(twitter\.com|x\.com)\/[a-zA-Z0-9_]{1,15}$'
            if not (re.fullmatch(username_regex, valor) or re.fullmatch(url_regex, valor, re.IGNORECASE)):
                return False

        elif plataforma == "tiktok":
            username_regex = r'^@?[a-zA-Z0-9_]{2,24}$'
            url_regex = r'^(https?:\/\/)?(www\.)?tiktok\.com\/@[a-zA-Z0-9_]{2,24}$'
            if not (re.fullmatch(username_regex, valor) or re.fullmatch(url_regex, valor, re.IGNORECASE)):
                return False

    return True

def validate_fecha_inicio(fecha_hora):
    if not fecha_hora:
        return False
    
    try:
        datetime.fromisoformat(fecha_hora)
        return True
    except ValueError:
        return False

def validate_fecha_termino(fecha_inicio, fecha_termino):
    if not fecha_termino:
        return True
    
    try:
        inicio = datetime.fromisoformat(fecha_inicio)
        termino = datetime.fromisoformat(fecha_termino)

        return inicio < termino
    except ValueError:
        return False

def validate_temas(temas):
    return any(temas)

def validate_tema_extra(tema, otro_seleccionado):
    if not otro_seleccionado:
        return True
    
    tema = tema.strip()
    return 3 <= len(tema) <= 15

def validate_files(files):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}

    if not files or len(files) == 0:
        return False
    
    # Validación del número de archivos
    if not (1 <= len(files) <= 5):
        return False
    
    for file in files:
        # Que no sea un archivo vacío
        if file.filename == "":
            return False
        # Validación de extensión
        ftype_guess = filetype.guess(file)
        if ftype_guess.extension not in ALLOWED_EXTENSIONS:
            return False
         # Validación de mimetype
        if ftype_guess.mime not in ALLOWED_MIMETYPES:
            return False
    return True

def validate_select(selected_value):
    return bool(selected_value) and selected_value.strip() != ""






# Validación completa antes de crear la actividad

def validate_actividad(
    region_nombre,
    comuna_nombre,
    sector,
    nombre,
    email,
    celular,
    contactos,
    dia_hora_inicio,
    dia_hora_termino,
    temas,
    otro_tema,
    files
):
    # Si hay errores, incluirá una lista con estos en el return, para mostrarlos en un mensaje flash.
    errores = []

    # Validaciones individuales
    if not validate_select(region_nombre):
        errores.append("Región no seleccionada")
    
    if not validate_select(comuna_nombre):
        errores.append("Comuna no seleccionada")
    
    if not validate_sector(sector):
        errores.append("Sector no válido (máximo 100 caracteres)")
    
    if not validate_name(nombre):
        errores.append("Nombre no válido (requerido, máximo 200 caracteres)")
    
    if not validate_email(email):
        errores.append("Email no válido")
    
    if not validate_num_celular(celular):
        errores.append("Número de celular no válido (formato: +569.12345678)")
    
    if not validate_contactos(contactos):
        errores.append("Contactos no válidos (verifique los formatos)")
    
    if not validate_fecha_inicio(dia_hora_inicio):
        errores.append("Fecha de inicio no válida")
    elif not validate_fecha_termino(dia_hora_inicio, dia_hora_termino):
        errores.append("Fecha de término debe ser posterior a la de inicio")
    
    if not validate_temas(temas):
        errores.append("Debe seleccionar al menos un tema")
    elif not validate_tema_extra(otro_tema, 'otro' in temas):
        errores.append("Tema 'otro' requiere descripción (3-15 caracteres)")
    
    if not validate_files(files):
        errores.append("Archivos no válidos (1-5 archivos, formatos: png, jpg, jpeg)")

    return (len(errores) == 0, errores)