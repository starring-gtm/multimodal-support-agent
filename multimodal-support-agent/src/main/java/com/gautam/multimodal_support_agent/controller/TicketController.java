package com.gautam.multimodal_support_agent.controller;

import com.gautam.multimodal_support_agent.model.Ticket;
import com.gautam.multimodal_support_agent.model.TicketJobEvent;
import com.gautam.multimodal_support_agent.service.FileStorageService;
import com.gautam.multimodal_support_agent.service.KafkaProducerService;
import com.gautam.multimodal_support_agent.service.TicketService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/tickets")
public class TicketController {
    private final TicketService ticketService;
    private final FileStorageService fileStorageService;
    private final KafkaProducerService kafkaProducerService;

    public TicketController(TicketService ticketService, FileStorageService fileStorageService, KafkaProducerService kafkaProducerService) {
        this.ticketService = ticketService;
        this.fileStorageService = fileStorageService;
        this.kafkaProducerService = kafkaProducerService;
    }

    @GetMapping
    public List<Ticket> getAllTickets() {
        return ticketService.getAllTickets();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Ticket> getTicket(@PathVariable Long id) {
        Ticket ticket = ticketService.getTicketById(id);
        if (ticket == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(ticket);
    }

    @PostMapping
    public Ticket createTicket(@RequestBody Ticket ticket) {
        Ticket createdTicket = ticketService.createTicket(ticket);
        TicketJobEvent ticketEvent = new TicketJobEvent(ticket);
        kafkaProducerService.sendMessage(ticketEvent);
        return createdTicket;
    }

    @PatchMapping("/{id}")
    public ResponseEntity<Ticket> updateTicket(@PathVariable Long id, @RequestBody Ticket ticket) {
        Ticket updated = ticketService.updateTicket(id, ticket);
        if (updated == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTicket(@PathVariable Long id) {
        boolean deleted = ticketService.deleteTicket(id);
        return deleted ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
    }

    @PostMapping("/{id}/image")
    public ResponseEntity<Ticket> uploadImage(@PathVariable Long id, @RequestParam("file") MultipartFile file) {
        String path = fileStorageService.store(file);
        Ticket updated = ticketService.attachImage(id, path);
        if (updated == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(updated);
    }

    @PostMapping("/{id}/audio")
    public ResponseEntity<Ticket> uploadAudio(@PathVariable Long id, @RequestParam("file") MultipartFile file) {
        String path = fileStorageService.store(file);
        Ticket updated = ticketService.attachAudio(id, path);
        if (updated == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(updated);
    }
}
