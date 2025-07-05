package tarea4.tarea4.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "actividad", schema = "tarea2")
public class Actividad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String sector;

    private String nombre;

    @Column(name = "dia_hora_inicio")
    private LocalDateTime diaHoraInicio;

    @Column(name = "dia_hora_termino")
    private LocalDateTime diaHoraTermino;

    // Getters y setters:
    public Integer getId() { return id; }
    public String getSector() { return sector; }
    public String getNombre() { return nombre; }
    public LocalDateTime getDiaHoraInicio() { return diaHoraInicio; }
    public LocalDateTime getDiaHoraTermino() { return diaHoraTermino; }

    public void setId(Integer id) { this.id = id; }
    public void setSector(String sector) { this.sector = sector; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    public void setDiaHoraInicio(LocalDateTime diaHoraInicio) { this.diaHoraInicio = diaHoraInicio; }
    public void setDiaHoraTermino(LocalDateTime diaHoraTermino) { this.diaHoraTermino = diaHoraTermino; }
}
