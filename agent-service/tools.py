import base64
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from retrieval import search_knowledge_base as _search_kb
import whisper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("escalation")

_whisper_model = whisper.load_model("base")

load_dotenv()

VALID_TEAMS = {"network-ops", "billing", "account-support", "logistics", "general"}

TEAM_EMAIL_MAP = {
    "network-ops": "network-ops@novalink.example.com",
    "billing": "billing@novalink.example.com",
    "account-support": "accounts@novalink.example.com",
    "logistics": "logistics@novalink.example.com",
    "general": "support-intake@novalink.example.com",
}

vision_llm = ChatNVIDIA(
    model="nvidia/llama-3.1-nemotron-nano-vl-8b-v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
)


def _send_notification(team: str, subject: str, body: str) -> None:
    """
    Sends the actual escalation notification. Currently logs instead of
    sending a real email — swap this out for smtplib/an email API later
    without touching the tool logic above it.
    """
    recipient = TEAM_EMAIL_MAP.get(team, TEAM_EMAIL_MAP["general"])
    logger.info(
        f"\n--- ESCALATION NOTIFICATION ---\n"
        f"To: {recipient}\n"
        f"Subject: {subject}\n"
        f"Time: {datetime.utcnow().isoformat()}Z\n"
        f"Body:\n{body}\n"
        f"--------------------------------"
    )


@tool
def escalate_to_team(ticket_id: str, team: str, reason: str, attempted_steps: str) -> str:
    """
    Escalate a support ticket to the appropriate internal team when it cannot
    be resolved from the knowledge base alone. Only call this after searching
    the knowledge base and finding no relevant or sufficient information.

    Args:
        ticket_id: The ID of the ticket being escalated.
        team: Which team should handle this. Must be one of:
              network-ops, billing, account-support, logistics, general.
              Use "general" only if you are genuinely unsure which team applies.
        reason: A brief explanation of the customer's issue.
        attempted_steps: What was already tried or searched before deciding to escalate.
    """
    if team not in VALID_TEAMS:
        team = "general"

    subject = f"Escalation: Ticket #{ticket_id} -> {team}"
    body = (
        f"Ticket ID: {ticket_id}\n"
        f"Routed to: {team}\n\n"
        f"Reason for escalation:\n{reason}\n\n"
        f"Steps already attempted:\n{attempted_steps}\n"
    )

    _send_notification(team, subject, body)

    return f"Ticket #{ticket_id} escalated to {team} team."

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the NovaLink support knowledge base for information relevant to a
    customer's issue. Use this to find troubleshooting steps, policy info,
    or team ownership for a support ticket.

    Args:
        query: A short description of the customer's issue or question.
    """
    results = _search_kb(query, k=3)

    if not results or results[0]["score"] > 0.9:
        return "No relevant knowledge base articles found for this query."

    formatted = []
    for r in results:
        formatted.append(
            f"[Source: {r['source']} / {r['section']} | Team: {r['team']} | Score: {r['score']:.3f}]\n{r['content']}"
        )
    return "\n\n---\n\n".join(formatted)


def _encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


@tool
def classify_image(image_path: str) -> str:
    """
    Analyze a customer-uploaded image (e.g. a photo of their router) to identify
    relevant details for troubleshooting, such as light patterns, colors, or
    visible damage. Use this when a ticket has an attached image and the
    customer's description alone isn't enough to diagnose the issue.

    Args:
        image_path: Local file path to the uploaded image.
    """
    try:
        image_b64 = _encode_image(image_path)
    except FileNotFoundError:
        return f"Error: could not find image at {image_path}."

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "This is a photo submitted with a customer support ticket for an "
                    "internet service provider. Describe what you see, focusing on: "
                    "any visible router/equipment lights and their color/pattern, "
                    "cable connections, or any visible physical damage. Be concise."
                ),
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
            },
        ]
    )

    response = vision_llm.invoke([message])
    return response.content

@tool
def transcribe_voice(audio_path: str) -> str:
    """
    Transcribe a customer's voice note attached to a support ticket into text.
    Use this when a ticket has an attached audio file describing the issue,
    before reasoning about what the customer needs.

    Args:
        audio_path: Local file path to the uploaded audio file.
    """
    try:
        result = _whisper_model.transcribe(audio_path)
        return result["text"].strip()
    except FileNotFoundError:
        return f"Error: could not find audio file at {audio_path}."
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

# # at the bottom of tools.py, temporarily
# if __name__ == "__main__":
#     print(search_knowledge_base.invoke({"query": "router blinking red"}))

if __name__ == "__main__":
    print(transcribe_voice.invoke({"audio_path": "/Users/gautamchaudhary/Documents/Projects/Multimodal support agent/agent-service/images/New Recording.m4a"}))