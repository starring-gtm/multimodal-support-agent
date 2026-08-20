package com.gautam.multimodal_support_agent.model;

public class TicketJobEvent {
    private Long ticketId;
    private String title;
    private String description;
    private String imagePath;
    private String audioPath;

    public TicketJobEvent() {}

    public TicketJobEvent(Ticket ticket) {
        this.ticketId = ticket.getId();
        this.title = ticket.getTitle();
        this.description = ticket.getDescription();
        this.imagePath = ticket.getImagePath();
        this.audioPath = ticket.getAudioPath();
    }

    // getters and setters
    public Long getTicketId() { return ticketId; }
    public void setTicketId(Long ticketId) { this.ticketId = ticketId; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getImagePath() { return imagePath; }
    public void setImagePath(String imagePath) { this.imagePath = imagePath; }
    public String getAudioPath() { return audioPath; }
    public void setAudioPath(String audioPath) { this.audioPath = audioPath; }
}
