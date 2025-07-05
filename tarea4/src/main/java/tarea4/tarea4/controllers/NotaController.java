package tarea4.tarea4.controllers;

import org.springframework.web.bind.annotation.RestController;

import tarea4.tarea4.services.NotaService;

import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequestMapping("/api/notas")
public class NotaController {
    private final NotaService notaService;

    public NotaController(NotaService notaService) {
        this.notaService = notaService;
    }

    @PostMapping("/evaluar")
    public Map<String, Object> evaluar(@RequestParam Long actividadId, @RequestParam int nota) {
        if (nota < 1 || nota > 7) {
            return Map.of("success", false, "error", "Nota fuera de rango");
        }
        notaService.guardarNota(actividadId, nota); // guardar la nueva nota
        double promedio = notaService.obtenerPromedio(actividadId); // recalcular promedio
        return Map.of("success", true, "promedio", promedio); // actualizar promedio
    }
}
