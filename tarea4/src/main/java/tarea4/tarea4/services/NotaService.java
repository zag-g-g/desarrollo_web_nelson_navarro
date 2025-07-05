package tarea4.tarea4.services;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import org.springframework.stereotype.Service;

import tarea4.tarea4.models.Nota;
import tarea4.tarea4.models.NotaRepository;

@Service
public class NotaService {

    private final NotaRepository notaRepository;

    public NotaService(NotaRepository notaRepository) {
        this.notaRepository = notaRepository;
    }

    public double obtenerPromedio(Long actividadId) {
        List<Nota> notas = notaRepository.findByActividadId(actividadId); // obtener todas las notas referentes a la misma actividad
        if (notas.isEmpty()) {
            return -1; // como default
        }
        double suma = notas.stream().mapToInt(Nota::getNota).sum(); // sumar las notas
        return suma / notas.size(); // dividir por el total de notas para obtener el promedio
    }

    public Nota guardarNota(Long actividadId, int nota) {
        Nota nuevaNota = new Nota(actividadId, nota);
        return notaRepository.save(nuevaNota);
    }
}