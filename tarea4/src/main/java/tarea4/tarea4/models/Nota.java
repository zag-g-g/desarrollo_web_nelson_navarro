package tarea4.tarea4.models;

import java.time.LocalDateTime;

import org.springframework.web.multipart.MultipartFile;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import jakarta.persistence.Column; // Para poder nombrar los atributos en Java con nombre distinto ('actividadId en vez de 'actividad_id')

@Entity
@Table(name = "nota", schema = "tarea2")
public class Nota {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "actividad_id", nullable = false)
    private Long actividadId;

    @Column(nullable = false)
    private Integer nota;

    public Nota() {}

    public Nota(Long actividadId, Integer nota) {
        this.actividadId = actividadId;
        this.nota = nota;
    }


    
    public Long getId() { return id; }
    public Long getActividadId() { return actividadId; }
    public Integer getNota() { return nota; }
    public void setActividadId(Long actividadId) { this.actividadId = actividadId; }
    public void setNota(Integer nota) { this.nota = nota; }
}
 