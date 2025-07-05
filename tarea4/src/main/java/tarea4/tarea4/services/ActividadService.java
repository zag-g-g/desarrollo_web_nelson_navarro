package tarea4.tarea4.services;

import org.springframework.stereotype.Service;
import tarea4.tarea4.models.Actividad;
import tarea4.tarea4.models.ActividadRepository;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ActividadService {

    private final ActividadRepository actividadRepository;

    public ActividadService(ActividadRepository actividadRepository) {
        this.actividadRepository = actividadRepository;
    }

    public List<Actividad> obtenerActividadesFinalizadas() {
        return actividadRepository.findByDiaHoraTerminoBefore(LocalDateTime.now()); // antes del momento actual, es decir, ya terminadas
    }
}
