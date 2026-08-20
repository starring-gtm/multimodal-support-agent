package com.gautam.multimodal_support_agent.controller;

import org.springframework.web.bind.annotation.*;

@RestController
public class HealthController {

    @GetMapping("/health")
    public String health() {
        return "Hey, I am open!";
    }
}
