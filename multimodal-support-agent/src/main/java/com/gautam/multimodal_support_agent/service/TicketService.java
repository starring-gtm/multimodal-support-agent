package com.gautam.multimodal_support_agent.service;

import com.gautam.multimodal_support_agent.model.Ticket;
import com.gautam.multimodal_support_agent.repository.TicketRepository;
import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class TicketService {
    private final TicketRepository ticketRepository;

    public TicketService(TicketRepository ticketRepository) {
        this.ticketRepository = ticketRepository;
    }

    public List<Ticket> getAllTickets() {
        return ticketRepository.findAll();
    }

    public Ticket getTicketById(Long id) {
        return ticketRepository.findById(id).orElse(null);
    }

    public Ticket createTicket(Ticket ticket) {
        ticket.setStatus("OPEN");
        return ticketRepository.save(ticket);
    }

    public Ticket updateTicket(Long id, Ticket updated) {
        return ticketRepository.findById(id).map(existing -> {
            if (updated.getTitle() != null) {
                existing.setTitle(updated.getTitle());
            }
            if (updated.getDescription() != null) {
                existing.setDescription(updated.getDescription());
            }
            if (updated.getStatus() != null) {
                existing.setStatus(updated.getStatus());
            }
            return ticketRepository.save(existing);
        }).orElse(null);
    }

    public boolean deleteTicket(Long id) {
        if (!ticketRepository.existsById(id)) return false;
        ticketRepository.deleteById(id);
        return true;
    }

    public Ticket attachImage(Long id, String path) {
        return ticketRepository.findById(id).map(t -> {
            t.setImagePath(path);
            return ticketRepository.save(t);
        }).orElse(null);
    }

    public Ticket attachAudio(Long id, String path) {
        return ticketRepository.findById(id).map(t -> {
            t.setAudioPath(path);
            return ticketRepository.save(t);
        }).orElse(null);
    }
}
