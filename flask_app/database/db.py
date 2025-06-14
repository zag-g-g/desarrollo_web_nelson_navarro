from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum, extract, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
from collections import defaultdict #para crear un diccionario js con regiones y sus comunas

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Modelos ---

class Region(Base):
    __tablename__ = 'region'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    
    comunas = relationship("Comuna", back_populates="region")


class Comuna(Base):
    __tablename__ = 'comuna'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    
    region = relationship("Region", back_populates="comunas")
    actividades = relationship("Actividad", back_populates="comuna")


class Actividad(Base):
    __tablename__ = 'actividad'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime)
    descripcion = Column(String(500))
    
    comuna = relationship("Comuna", back_populates="actividades")
    fotos = relationship("Foto", back_populates="actividad", cascade="all, delete-orphan")
    contactos = relationship("ContactarPor", back_populates="actividad", cascade="all, delete-orphan")
    temas = relationship("ActividadTema", back_populates="actividad", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="actividad", cascade="all, delete-orphan")



class Foto(Base):
    __tablename__ = 'foto'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    
    actividad = relationship("Actividad", back_populates="fotos")


class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra', name='contact_methods'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    
    actividad = relationship("Actividad", back_populates="contactos")


class ActividadTema(Base):
    __tablename__ = 'actividad_tema'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 
                      'juegos', 'baile', 'comida', 'otro', name='activity_topics'), nullable=False)
    glosa_otro = Column(String(15))
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    
    actividad = relationship("Actividad", back_populates="temas")


class Paginador:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = (total + per_page - 1) // per_page  # total páginas
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_num = page - 1
        self.next_num = page + 1

    def iter_pages(self):
        return range(1, self.pages + 1)



class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(DateTime, nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("Actividad", back_populates="comentarios")







# Funciones para obtener valores de la base de datos


def get_comuna_id_by_nombres(comuna_nombre, region_nombre):
    db = SessionLocal()
    comuna = (
        db.query(Comuna)
        .join(Region, Comuna.region_id == Region.id)
        .filter(
            Comuna.nombre == comuna_nombre.strip(),
            Region.nombre == region_nombre.strip()
        )
        .first()
    )
    db.close()
    return comuna.id if comuna else None


def get_comuna_y_region_nombres_by_comuna_id(comuna_id):
    db = SessionLocal()
    comuna = db.query(Comuna).filter(Comuna.id == comuna_id).first()
    region_nombre = comuna.region.nombre if comuna else None
    db.close()
    return comuna.nombre if comuna else None, region_nombre



def get_actividad_by_id(id):
    db = SessionLocal()
    actividad = db.query(Actividad).filter(Actividad.id == id).first()
    db.close()
    return actividad


# Para los selects de regiones y comunas, así no hay discrepancias con la base de datos
def get_region_comuna():
    db_session = SessionLocal()
    regiones = db_session.query(Region).all()
    region_comuna = defaultdict(list)

    for region in regiones:
        for comuna in region.comunas:
            region_comuna[region.nombre].append(comuna.nombre)

    db_session.close()
    return region_comuna

# Insertar los valores en las respectivas bases de datos

def create_actividad(
    comuna_id,
    nombre,
    email,
    dia_hora_inicio,
    fotos,
    temas,
    contactos = None,
    **kwargs
):
    db = SessionLocal()

    actividad = Actividad(
        comuna_id=comuna_id,
        nombre=nombre,
        email=email,
        dia_hora_inicio=dia_hora_inicio,
        **{k: v for k, v in kwargs.items() if k in ['sector', 'celular', 'dia_hora_termino', 'descripcion']}
    )
    db.add(actividad)
    db.flush()  # Para obtener actividad.id

    for foto in fotos:
        db.add(Foto(
            ruta_archivo=foto['ruta'],
            nombre_archivo=foto['nombre'],
            actividad_id=actividad.id
        ))

    for tema in temas:
        db.add(ActividadTema(
            tema=tema['tema'],
            glosa_otro=tema.get('glosa_otro'),
            actividad_id=actividad.id
        ))

    if contactos:
        for contacto in contactos:
            db.add(ContactarPor(
                nombre=contacto['nombre'],
                identificador=contacto['identificador'],
                actividad_id=actividad.id
            ))

    db.commit()
    db.refresh(actividad)
    db.close()
    return actividad


# Ordenar con paginación de 5 actividades, obteniendo los valores en orden descendente de id (considerando que un id mayor se relaciona con una actividad añadida hace menos tiempo)

def get_actividades_paginadas(page = 1, per_page = 5):
    db = SessionLocal()
    actividades = db.query(Actividad).\
        order_by(Actividad.id.desc()).\
        paginate(page=page, per_page=per_page, error_out=False)
    db.close()
    return actividades


def get_actividades_con_datos(page = 1, per_page = 5):
    db = SessionLocal()
    actividades_query = db.query(Actividad).order_by(Actividad.id.desc())

    total = actividades_query.count()
    actividades_items = actividades_query.offset((page - 1) * per_page).limit(per_page).all()

    data = []
    for actividad in actividades_items:
        comuna = db.query(Comuna).get(actividad.comuna_id)
        fotos = db.query(Foto).filter_by(actividad_id=actividad.id).all()
        temas = db.query(ActividadTema).filter_by(actividad_id=actividad.id).all()

        data.append({
            "actividad": actividad,
            "comuna": comuna,
            "fotos": fotos,
            "temas": temas
        })

    db.close()

    actividades_paginadas = Paginador(actividades_items, page, per_page, total)
    return actividades_paginadas, data





def get_full_actividad_data(actividad_id):
    db = SessionLocal()
    actividad = db.query(Actividad).get(actividad_id)
    result = {'actividad': actividad}

    if actividad:
        comuna = db.query(Comuna).get(actividad.comuna_id)
        result.update({
            'comuna': comuna,
            'region': comuna.region if comuna else None,
            'fotos': db.query(Foto).filter(Foto.actividad_id == actividad_id).all(),
            'temas': db.query(ActividadTema).filter(ActividadTema.actividad_id == actividad_id).all(),
            'contactos': db.query(ContactarPor).filter(ContactarPor.actividad_id == actividad_id).all()
        })

    db.close()
    return result




def get_estadisticas():
    db = SessionLocal()

    # --- Gráfico 1: actividades por día (últimos 5 días con actividades)
    actividades_por_dia = (
        db.query(func.date(Actividad.dia_hora_inicio), func.count())
        .group_by(func.date(Actividad.dia_hora_inicio))
        .order_by(func.date(Actividad.dia_hora_inicio).desc())
        .all()
    )
    actividades_por_dia.reverse()  # Para que vayan en orden ascendente de fecha

    # --- Gráfico 2: actividades por tipo (tema)
    actividades_por_tema = (
        db.query(ActividadTema.tema, func.count())
        .group_by(ActividadTema.tema)
        .all()
    )

    # --- Gráfico 3: actividades por franja horaria por mes (últimos 3 meses)
    actividades = db.query(
        extract('month', Actividad.dia_hora_inicio).label('mes'),
        extract('year', Actividad.dia_hora_inicio).label('anio'),
        extract('hour', Actividad.dia_hora_inicio).label('hora')
    ).all()

    franja_por_mes = {}
    for a in actividades:
        mes_str = f"{int(a.anio)}-{int(a.mes):02d}"
        if mes_str not in franja_por_mes:
            franja_por_mes[mes_str] = {'mañana': 0, 'mediodía': 0, 'tarde': 0}
        if 6 <= a.hora < 12:
            franja_por_mes[mes_str]['mañana'] += 1
        elif 12 <= a.hora < 18:
            franja_por_mes[mes_str]['mediodía'] += 1
        else:
            franja_por_mes[mes_str]['tarde'] += 1

    # Ordena los meses por fecha
    meses_ordenados = sorted(franja_por_mes.keys())[-3:]

    db.close()

    return (actividades_por_dia, actividades_por_tema, meses_ordenados, franja_por_mes)



