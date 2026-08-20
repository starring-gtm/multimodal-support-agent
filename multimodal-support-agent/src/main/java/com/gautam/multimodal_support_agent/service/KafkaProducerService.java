package com.gautam.multimodal_support_agent.service;

import com.gautam.multimodal_support_agent.model.TicketJobEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class KafkaProducerService {

    private static final String TOPIC = "tickets";
    @Autowired private final KafkaTemplate<String, TicketJobEvent> kafkaTemplate;

    public KafkaProducerService(KafkaTemplate<String, TicketJobEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendMessage(TicketJobEvent ticketJobEvent) {
        System.out.println("Sending message...");
        kafkaTemplate.send(TOPIC, ticketJobEvent);
        System.out.println("Topic: tickets - Message sent for: " + ticketJobEvent.getTitle() + " (TicketID: " + ticketJobEvent.getTicketId() + ")");
    }
}
