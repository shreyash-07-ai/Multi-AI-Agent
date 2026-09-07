import json
import re

from .llm import ask


def _extract_json(text):
    """
    Extract JSON from Gemini response even when
    Gemini wraps it inside ```json ... ```
    """

    if not text:
        return {}

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    return {}


def create_content(
    user_request,
    rag,
    web,
    doc_analysis=None,
    ppt_analysis=None,
):
    prompt = {
        "request": user_request,
        "enterprise_context": rag[:10],
        "web_sources": web[:10],
        "document_template_analysis": doc_analysis or {},
        "ppt_template_analysis": ppt_analysis or {},
    }

    system = """
You are the content-planning agent for an enterprise
multi-agent document and PowerPoint generation system.

Your job is to create structured presentation content.

IMPORTANT:
Return ONLY valid JSON.
DO NOT return markdown.
DO NOT return ```json.
DO NOT return explanations outside JSON.

Use exactly this structure:

{
  "title": "Presentation title",
  "company_name": "Company name",
  "project_name": "Project name",
  "executive_summary": "Short overview",
  "sections": [
    {
      "heading": "Section title",
      "bullets": [
        "Point 1",
        "Point 2",
        "Point 3"
      ]
    }
  ],
  "slides": [
    {
      "title": "Slide title",
      "bullets": [
        "Point 1",
        "Point 2",
        "Point 3"
      ],
      "notes": ""
    }
  ],
  "citations": []
}

PRESENTATION RULES:

1. Slide 1 is ONLY for:
   - Title
   - Company name
   - Project/topic
   - Short overview

2. Slide 2 onward must contain the actual
   business/content parameters.

3. Create MULTIPLE slides.

4. Each major parameter/section must get its own slide.

5. Do NOT put the complete answer into one slide.

6. Maximum 4-5 bullets per slide.

7. If a section contains many points, split it
   into multiple slides.

8. Never put raw JSON inside a bullet.

9. Never create empty slides.

10. Do not create fake content such as:
   "Additional detail based on the requested business context."

11. Use the enterprise/RAG context when available.

12. Do not invent enterprise-specific facts.

13. Preserve important values from the supplied
   enterprise context.

For example, if the content contains:

- Response Targets
- Ticket Priority
- Escalation Process
- Data Retention
- AI Assistant Usage

then create separate slides such as:

Slide 1:
Title + Company + Overview

Slide 2:
Response Targets

Slide 3:
Ticket Priority

Slide 4:
Escalation Process

Slide 5:
Data Retention

Slide 6:
AI Assistant Usage

The number of slides should depend on the amount
of actual content.
"""

    raw = ask(
        system,
        json.dumps(
            prompt,
            ensure_ascii=False,
            indent=2,
        ),
    )

    content = _extract_json(raw)

    if not content:
        raise RuntimeError(
            "Gemini returned invalid presentation JSON."
        )

    # --------------------------------------------------
    # If Gemini did not create slides, build them
    # automatically from sections.
    # --------------------------------------------------

    sections = content.get("sections", [])

    if not isinstance(sections, list):
        sections = []

    slides = []

    for section in sections:

        if not isinstance(section, dict):
            continue

        heading = section.get(
            "heading",
            section.get("title", "Section"),
        )

        bullets = section.get(
            "bullets",
            [],
        )

        if isinstance(bullets, str):
            bullets = [bullets]

        # Split section into multiple slides
        # with maximum 4 bullets each.
        for i in range(0, len(bullets), 4):

            chunk = bullets[i:i + 4]

            if not chunk:
                continue

            if len(bullets) > 4:
                part = (i // 4) + 1
                total = (len(bullets) + 3) // 4

                slide_title = (
                    f"{heading} ({part}/{total})"
                )
            else:
                slide_title = heading

            slides.append(
                {
                    "title": slide_title,
                    "bullets": chunk,
                    "notes": "",
                }
            )

    # If Gemini already supplied slides,
    # prefer them when they contain real content.
    generated_slides = content.get("slides", [])

    if (
        isinstance(generated_slides, list)
        and len(generated_slides) > 1
    ):
        valid_slides = []

        for slide in generated_slides:

            if not isinstance(slide, dict):
                continue

            title = slide.get(
                "title",
                "Section",
            )

            bullets = slide.get(
                "bullets",
                [],
            )

            if isinstance(bullets, str):
                bullets = [bullets]

            if bullets:
                valid_slides.append(
                    {
                        "title": title,
                        "bullets": bullets,
                        "notes": slide.get(
                            "notes",
                            "",
                        ),
                    }
                )

        if valid_slides:
            slides = valid_slides

    content["slides"] = slides

    # Make sure required fields exist
    content.setdefault(
        "title",
        "AI-Generated Business Proposal",
    )

    content.setdefault(
        "company_name",
        "Company",
    )

    content.setdefault(
        "project_name",
        "",
    )

    content.setdefault(
        "executive_summary",
        "",
    )

    content.setdefault(
        "citations",
        web,
    )

    return content