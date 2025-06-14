from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
from datetime import datetime
from markupsafe import escape
from utils.validations import validate_actividad
from database import db
from database.db import SessionLocal, Comentario

app = Flask(__name__)
app.secret_key = "s1cr3_tek3y"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# --- Rutas Principales ---
# Índice/Portada
@app.route('/', methods=['GET'])
def index():
    gracias = request.args.get('gracias') == '1'
    _, data = db.get_actividades_con_datos(page=1, per_page=5)
    return render_template('index.html', data=data, gracias=gracias)

# Estadísticas
@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/api/estadisticas')
def api_estadisticas():
    (actividades_por_dia, actividades_por_tema, meses_ordenados, franja_por_mes) = db.get_estadisticas()
    return jsonify({
        'actividades_por_dia': [
            {'fecha': str(f[0]), 'cantidad': f[1]} for f in actividades_por_dia
        ],
        'actividades_por_tema': [
            {'tema': f[0], 'cantidad': f[1]} for f in actividades_por_tema
        ],
        'actividades_por_franja_mes': {
            mes: franja_por_mes[mes] for mes in meses_ordenados
        }
    })


# Formulario
@app.route('/informar_actividad', methods=['GET', 'POST'])
def informar_actividad():
    region_comuna = db.get_region_comuna() # para los select

    if request.method == 'POST':
        # Obtener los datos
        region_nombre = request.form.get('select-region')
        comuna_nombre = request.form.get('select-comuna')
        sector = request.form.get('sector')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('phone')
        dia_hora_inicio = request.form.get('dia-hora-inicio')
        dia_hora_termino = request.form.get('dia-hora-termino')
        descripcion = request.form.get('descripcion')
        temas_form = request.form.getlist('temas[]')
        otro_tema = request.form.get('otro-tema')
        fotos_files = request.files.getlist('fotos[]')

        # Guardar contactos de forma más ordenada para procesarlos más tarde
        plataformas = ['whatsapp', 'telegram', 'instagram', 'x', 'tiktok', 'otra-plataforma']
        contactos = []
        for plataforma in plataformas:
            identificador = request.form.get(f'{plataforma}-id')
            if identificador:
                contactos.append({
                    'nombre': plataforma.replace('otra-plataforma', 'otra'),
                    'identificador': identificador
                })

        # Validar datos
        is_valid, errores = validate_actividad(
            region_nombre, comuna_nombre, sector, nombre, email, celular,
            {c['nombre']: c['identificador'] for c in contactos},
            dia_hora_inicio, dia_hora_termino, temas_form, otro_tema, fotos_files
        )

        if not is_valid:
            flash(f"Errores en los siguientes campos: {', '.join(errores)}", 'error') # separar errores por comas
            return render_template('informar_actividad.html', region_comuna=region_comuna)

        # Procesar fotos y añadirles un nombre con hashing para evitar colisiones en la base de datos
        fotos_data = []
        for foto in fotos_files:
            if foto.filename:
                _filename = hashlib.sha256(
                    secure_filename(foto.filename)
                    .encode('utf-8')
                    ).hexdigest()
                _extension = filetype.guess(foto).extension
                img_filename = f"{_filename}.{_extension}"

                filepath = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
                foto.save(filepath)

                fotos_data.append({
                    'ruta': f"uploads/{img_filename}",
                    'nombre': img_filename
                })

        # Procesar temas
        temas_data = []
        for tema in temas_form:
            tema_data = {'tema': tema.lower()}
            if tema.lower() == 'otro':
                tema_data['glosa_otro'] = otro_tema
            temas_data.append(tema_data)

        # Obtener comuna_id con nombre de comuna y nombre de región
        comuna_id = db.get_comuna_id_by_nombres(comuna_nombre, region_nombre)
        # Crear actividad
        db.create_actividad(
            comuna_id=int(comuna_id),
            nombre=nombre,
            email=email,
            dia_hora_inicio=datetime.fromisoformat(dia_hora_inicio),
            fotos=fotos_data,
            temas=temas_data,
            contactos=contactos,
            sector=sector,
            celular=celular,
            dia_hora_termino=datetime.fromisoformat(dia_hora_termino) if dia_hora_termino else None,
            descripcion=descripcion
        )
        return redirect(url_for('index', gracias='1'))
    
    return render_template('informar_actividad.html', region_comuna=region_comuna)


# Listado de actividades
@app.route('/listado_actividades', methods=['GET'])
def listado_actividades():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    actividades_paginadas, data = db.get_actividades_con_datos(page, per_page)
    return render_template('listado_actividades.html', actividades=actividades_paginadas, data=data)

# Para el detalle de la actividad según su id
@app.route('/actividad/<int:actividad_id>', methods=['GET'])
def ver_actividad(actividad_id):
    data = db.get_full_actividad_data(actividad_id)
    if not data or not data['actividad']:
        flash("Actividad no encontrada.", "error")
        return redirect(url_for('listado_actividades'))
    return render_template('detalle_actividad.html', data=data)



@app.route('/api/comentarios/<int:actividad_id>', methods=['GET'])
def api_get_comentarios(actividad_id):
    db = SessionLocal()
    comentarios = db.query(Comentario).filter_by(actividad_id=actividad_id).order_by(Comentario.fecha.desc()).all()
    db.close()
    return jsonify([{
        'nombre': c.nombre,
        'texto': c.texto,
        'fecha': c.fecha.strftime('%d/%m/%Y %H:%M')
    } for c in comentarios])

@app.route('/api/comentarios/<int:actividad_id>', methods=['POST'])
def api_post_comentario(actividad_id):
    data = request.get_json()
    nombre = data.get("nombre", "").strip()
    texto = data.get("texto", "").strip()

    if not (3 <= len(nombre) <= 80):
        return jsonify(ok=False, error="El nombre debe contener entre 3 y 80 caracteres."), 400
    if len(texto) < 5:
        return jsonify(ok=False, error="El comentario debe contener al menos 5 caracteres"), 400

    db = SessionLocal()
    comentario = Comentario(
        nombre=nombre,
        texto=texto,
        fecha=datetime.now(),
        actividad_id=actividad_id
    )
    db.add(comentario)
    db.commit()
    db.close()
    return jsonify(ok=True)



if __name__ == '__main__':
    app.run(debug=True)