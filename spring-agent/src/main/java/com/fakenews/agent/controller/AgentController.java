package com.fakenews.agent.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fakenews.agent.service.AiService;
import jakarta.validation.constraints.Size;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class AgentController {
    private final AiService aiService;
    public AgentController(AiService aiService) { this.aiService = aiService; }

    @PostMapping("/predict")
    public ResponseEntity<?> predict(@RequestBody PredictionRequest request) {
        if ((request.text() == null || request.text().isBlank()) &&
            (request.url() == null || request.url().isBlank())) {
            return ResponseEntity.badRequest().body(Map.of("error", "Enter article text or a URL."));
        }
        String model = request.model() == null || request.model().isBlank() ? "ml" : request.model();
        if (!model.equals("ml") && !model.equals("dt") && !model.equals("dl")) {
            return ResponseEntity.badRequest().body(Map.of("error", "Model must be ml, dt, or dl."));
        }
        try {
            JsonNode result = aiService.predict(request.text(), request.url(), model, request.explain());
            return ResponseEntity.ok(result);
        } catch (org.springframework.web.client.RestClientResponseException ex) {
            return ResponseEntity.status(ex.getStatusCode()).body(Map.of("error", "AI service: " + ex.getStatusText()));
        } catch (Exception ex) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                .body(Map.of("error", "AI service is unavailable. Ensure the Python service is running."));
        }
    }

    public record PredictionRequest(@Size(max=100000) String text, String url, String model, boolean explain) {}
}
