package tarea4.tarea4.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import tarea4.tarea4.models.Actividad;
import tarea4.tarea4.services.ActividadService;

import java.util.List;

@Controller
public class ActividadController {

    private final ActividadService actividadService;

    public ActividadController(ActividadService actividadService) {
        this.actividadService = actividadService;
    }

    @GetMapping("/actividades-nota")
    public String mostrarActividadesFinalizadas(Model model) {
        List<Actividad> actividades = actividadService.obtenerActividadesFinalizadas(); // seleccionamos actividades ya terminadas
        model.addAttribute("actividades", actividades); // entregamos las actividades como data a actividades-nota.html
        return "actividades-nota";
    }
}
