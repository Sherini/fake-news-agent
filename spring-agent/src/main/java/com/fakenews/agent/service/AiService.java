package com.fakenews.agent.service;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import java.util.Map;

@Service
public class AiService {
    private final RestClient client;

    public AiService(@Value("${ai.service.url:http://localhost:5000}") String aiUrl) {
        this.client = RestClient.builder().baseUrl(aiUrl).build();
    }

    public JsonNode predict(String text, String url, String model, boolean explain) {
        Map<String, Object> body = Map.of(
            "text", text == null ? "" : text,
            "url", url == null ? "" : url,
            "model", model == null || model.isBlank() ? "ml" : model,
            "explain", explain
        );
        return client.post().uri("/api/predict")
            .contentType(MediaType.APPLICATION_JSON)
            .body(body).retrieve().body(JsonNode.class);
    }
}
