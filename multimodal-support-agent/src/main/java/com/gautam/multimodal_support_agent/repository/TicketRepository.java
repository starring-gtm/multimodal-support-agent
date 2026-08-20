package com.gautam.multimodal_support_agent.repository;

import com.gautam.multimodal_support_agent.model.Ticket;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TicketRepository extends JpaRepository<Ticket, Long> {
}
