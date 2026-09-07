from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


# ============================================================
# BASIC SETTINGS
# ============================================================

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

LEFT_MARGIN = Inches(0.75)
RIGHT_MARGIN = Inches(0.75)

TITLE_TOP = Inches(0.45)
TITLE_HEIGHT = Inches(0.75)

CONTENT_TOP = Inches(1.45)
CONTENT_HEIGHT = Inches(5.25)

MAX_BULLETS = 4


# ============================================================
# REMOVE ALL EXISTING SLIDES
# ============================================================

def _delete_all_slides(prs):

    slide_ids = list(prs.slides._sldIdLst)

    for slide_id in slide_ids:
        prs.part.drop_rel(slide_id.rId)
        prs.slides._sldIdLst.remove(slide_id)


# ============================================================
# GET BLANK LAYOUT
# ============================================================

def _get_blank_layout(prs):

    for layout in prs.slide_layouts:

        if layout.name.lower() == "blank":
            return layout

    return prs.slide_layouts[0]


# ============================================================
# CLEAN TEXT
# ============================================================

def _clean_text(text):

    if text is None:
        return ""

    text = str(text)

    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("```json", "")
    text = text.replace("```", "")

    return text.strip()


# ============================================================
# ADD HEADER
# ============================================================

def _add_header(slide, title):

    # Header background
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0),
        Inches(0),
        SLIDE_WIDTH,
        Inches(1.15),
    )

    header.line.fill.background()

    # Title
    title_box = slide.shapes.add_textbox(
        LEFT_MARGIN,
        TITLE_TOP,
        Inches(11.8),
        TITLE_HEIGHT,
    )

    tf = title_box.text_frame
    tf.clear()

    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf.paragraphs[0]

    p.text = _clean_text(title)

    p.font.size = Pt(28)
    p.font.bold = True

    p.alignment = PP_ALIGN.LEFT


# ============================================================
# ADD FOOTER
# ============================================================

def _add_footer(slide, number, total):

    footer = slide.shapes.add_textbox(
        Inches(11.4),
        Inches(7.05),
        Inches(1.2),
        Inches(0.25),
    )

    tf = footer.text_frame
    tf.clear()

    p = tf.paragraphs[0]

    p.text = f"{number} / {total}"

    p.font.size = Pt(9)

    p.alignment = PP_ALIGN.RIGHT


# ============================================================
# ADD CONTENT BOX
# ============================================================

def _add_content_box(slide, bullets):

    # Main content container
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        LEFT_MARGIN,
        CONTENT_TOP,
        Inches(11.83),
        CONTENT_HEIGHT,
    )

    box.fill.background()
    box.line.fill.background()

    # Text area
    text_box = slide.shapes.add_textbox(
        Inches(1.05),
        Inches(1.75),
        Inches(11.25),
        Inches(4.65),
    )

    tf = text_box.text_frame

    tf.clear()

    tf.word_wrap = True

    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)

    tf.vertical_anchor = MSO_ANCHOR.TOP

    # --------------------------------------------------------
    # Add bullets
    # --------------------------------------------------------

    for index, bullet in enumerate(bullets):

        bullet = _clean_text(bullet)

        if not bullet:
            continue

        p = (
            tf.paragraphs[0]
            if index == 0
            else tf.add_paragraph()
        )

        p.text = bullet

        p.font.size = Pt(19)

        p.space_after = Pt(16)

        p.line_spacing = 1.15

        p.level = 0

        p.alignment = PP_ALIGN.LEFT

    return text_box


# ============================================================
# TITLE SLIDE
# ============================================================

def _create_title_slide(
    prs,
    content,
    layout,
    number,
    total,
):

    slide = prs.slides.add_slide(layout)

    title = _clean_text(
        content.get(
            "title",
            "AI-Generated Business Proposal",
        )
    )

    company = _clean_text(
        content.get(
            "company_name",
            content.get(
                "company",
                "",
            ),
        )
    )

    project = _clean_text(
        content.get(
            "project_name",
            content.get(
                "topic",
                "",
            ),
        )
    )

    summary = _clean_text(
        content.get(
            "executive_summary",
            "",
        )
    )

    # --------------------------------------------------------
    # Main title
    # --------------------------------------------------------

    title_box = slide.shapes.add_textbox(
        Inches(1.0),
        Inches(1.25),
        Inches(11.3),
        Inches(1.3),
    )

    tf = title_box.text_frame

    tf.clear()

    tf.word_wrap = True

    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf.paragraphs[0]

    p.text = title

    p.font.size = Pt(34)

    p.font.bold = True

    p.alignment = PP_ALIGN.CENTER

    # --------------------------------------------------------
    # Company / Project
    # --------------------------------------------------------

    details = []

    if company:
        details.append(
            f"Company: {company}"
        )

    if project:
        details.append(
            f"Project: {project}"
        )

    if details:

        details_box = slide.shapes.add_textbox(
            Inches(1.5),
            Inches(2.8),
            Inches(10.3),
            Inches(0.9),
        )

        tf = details_box.text_frame

        tf.clear()

        tf.word_wrap = True

        for i, detail in enumerate(details):

            p = (
                tf.paragraphs[0]
                if i == 0
                else tf.add_paragraph()
            )

            p.text = detail

            p.font.size = Pt(18)

            p.alignment = PP_ALIGN.CENTER

            p.space_after = Pt(5)

    # --------------------------------------------------------
    # Overview box
    # --------------------------------------------------------

    if summary:

        overview = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1.2),
            Inches(4.0),
            Inches(10.9),
            Inches(1.8),
        )

        overview.fill.background()
        overview.line.fill.background()

        summary_box = slide.shapes.add_textbox(
            Inches(1.5),
            Inches(4.25),
            Inches(10.3),
            Inches(1.3),
        )

        tf = summary_box.text_frame

        tf.clear()

        tf.word_wrap = True

        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        p = tf.paragraphs[0]

        p.text = summary[:650]

        p.font.size = Pt(17)

        p.alignment = PP_ALIGN.CENTER

    _add_footer(
        slide,
        number,
        total,
    )

    return slide


# ============================================================
# CONTENT SLIDE
# ============================================================

def _create_content_slide(
    prs,
    title,
    bullets,
    layout,
    number,
    total,
):

    slide = prs.slides.add_slide(layout)

    # Header
    _add_header(
        slide,
        title,
    )

    # Content
    _add_content_box(
        slide,
        bullets,
    )

    # Footer
    _add_footer(
        slide,
        number,
        total,
    )

    return slide


# ============================================================
# SPLIT BULLETS
# ============================================================

def _split_bullets(bullets):

    if isinstance(bullets, str):

        bullets = [bullets]

    cleaned = []

    for bullet in bullets:

        if isinstance(bullet, dict):

            bullet = bullet.get(
                "text",
                bullet.get(
                    "content",
                    "",
                ),
            )

        bullet = _clean_text(bullet)

        if bullet:
            cleaned.append(bullet)

    return cleaned


# ============================================================
# GENERATE PPT
# ============================================================

def generate_pptx(
    content,
    output_path,
    template_path=None,
    target_slides=12,
):

    # --------------------------------------------------------
    # Load presentation
    # --------------------------------------------------------

    if (
        template_path
        and Path(template_path).exists()
    ):

        prs = Presentation(
            template_path
        )

    else:

        prs = Presentation()

    # --------------------------------------------------------
    # Remove all old slides
    # --------------------------------------------------------

    _delete_all_slides(prs)

    # --------------------------------------------------------
    # Use ONLY blank layout
    # --------------------------------------------------------

    blank_layout = _get_blank_layout(prs)

    # --------------------------------------------------------
    # Prepare sections
    # --------------------------------------------------------

    sections = content.get(
        "sections",
        [],
    )

    if not isinstance(sections, list):

        sections = []

    slide_data = []

    for section in sections:

        if not isinstance(
            section,
            dict,
        ):
            continue

        heading = _clean_text(
            section.get(
                "heading",
                section.get(
                    "title",
                    "Section",
                ),
            )
        )

        bullets = _split_bullets(
            section.get(
                "bullets",
                [],
            )
        )

        if not bullets:

            continue

        # ----------------------------------------------------
        # 4 bullets per slide
        # ----------------------------------------------------

        for i in range(
            0,
            len(bullets),
            MAX_BULLETS,
        ):

            chunk = bullets[
                i:i + MAX_BULLETS
            ]

            if len(bullets) > MAX_BULLETS:

                part = (
                    i // MAX_BULLETS
                ) + 1

                total_parts = (
                    len(bullets)
                    + MAX_BULLETS
                    - 1
                ) // MAX_BULLETS

                slide_title = (
                    f"{heading} "
                    f"({part}/{total_parts})"
                )

            else:

                slide_title = heading

            slide_data.append(
                {
                    "title": slide_title,
                    "bullets": chunk,
                }
            )

    # --------------------------------------------------------
    # If sections are empty, use Gemini slides
    # --------------------------------------------------------

    if not slide_data:

        gemini_slides = content.get(
            "slides",
            [],
        )

        if isinstance(
            gemini_slides,
            list,
        ):

            for item in gemini_slides:

                if not isinstance(
                    item,
                    dict,
                ):
                    continue

                title = _clean_text(
                    item.get(
                        "title",
                        "Section",
                    )
                )

                bullets = _split_bullets(
                    item.get(
                        "bullets",
                        [],
                    )
                )

                if bullets:

                    for i in range(
                        0,
                        len(bullets),
                        MAX_BULLETS,
                    ):

                        slide_data.append(
                            {
                                "title": title,
                                "bullets": bullets[
                                    i:i + MAX_BULLETS
                                ],
                            }
                        )

    # --------------------------------------------------------
    # Fallback slide
    # --------------------------------------------------------

    if not slide_data:

        summary = _clean_text(
            content.get(
                "executive_summary",
                "",
            )
        )

        slide_data.append(
            {
                "title": "Overview",
                "bullets": [
                    summary
                    or "No additional information available."
                ],
            }
        )

    # --------------------------------------------------------
    # Sources
    # --------------------------------------------------------

    citations = content.get(
        "citations",
        [],
    )

    if citations:

        sources = []

        for citation in citations:

            if isinstance(
                citation,
                dict,
            ):

                source_title = _clean_text(
                    citation.get(
                        "title",
                        "Source",
                    )
                )

                url = _clean_text(
                    citation.get(
                        "url",
                        "",
                    )
                )

                if url:

                    sources.append(
                        f"{source_title} - {url}"
                    )

                else:

                    sources.append(
                        source_title
                    )

            else:

                sources.append(
                    _clean_text(
                        citation
                    )
                )

        for i in range(
            0,
            len(sources),
            MAX_BULLETS,
        ):

            slide_data.append(
                {
                    "title": "Sources & References",
                    "bullets": sources[
                        i:i + MAX_BULLETS
                    ],
                }
            )

    # --------------------------------------------------------
    # Total slide count
    # --------------------------------------------------------

    total = 1 + len(slide_data)

    # --------------------------------------------------------
    # SLIDE 1
    # --------------------------------------------------------

    _create_title_slide(
        prs,
        content,
        blank_layout,
        1,
        total,
    )

    # --------------------------------------------------------
    # SLIDE 2+
    # --------------------------------------------------------

    for index, item in enumerate(
        slide_data,
        start=2,
    ):

        _create_content_slide(
            prs=prs,
            title=item["title"],
            bullets=item["bullets"],
            layout=blank_layout,
            number=index,
            total=total,
        )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    prs.save(
        output_path
    )

    return str(output_path)