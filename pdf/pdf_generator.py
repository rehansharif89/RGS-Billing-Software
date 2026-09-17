from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.units import inch
from xml.sax.saxutils import escape
import os


def generate_pdf(data, filename):

    # =========================================================
    # DOCUMENT
    # =========================================================

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    elements = []

    # =========================================================
    # COLORS
    # =========================================================

    DARK = colors.HexColor("#1F2937")
    TEXT = colors.HexColor("#374151")
    MUTED = colors.HexColor("#6B7280")
    LIGHT = colors.HexColor("#F3F4F6")
    LIGHTER = colors.HexColor("#F9FAFB")
    BORDER = colors.HexColor("#D1D5DB")
    WHITE = colors.white

    # =========================================================
    # STYLES
    # =========================================================

    company_style = ParagraphStyle(
        "CompanyStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=DARK
    )

    company_info_style = ParagraphStyle(
        "CompanyInfoStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=MUTED
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=DARK
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=TEXT
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=MUTED
    )

    center_style = ParagraphStyle(
        "CenterStyle",
        parent=normal_style,
        alignment=TA_CENTER
    )

    right_style = ParagraphStyle(
        "RightStyle",
        parent=normal_style,
        alignment=TA_RIGHT
    )

    table_header_center_style = ParagraphStyle(
        "TableHeaderCenterStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=DARK
    )

    table_header_left_style = ParagraphStyle(
        "TableHeaderLeftStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=DARK
    )

    table_header_right_style = ParagraphStyle(
        "TableHeaderRightStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        alignment=TA_RIGHT,
        textColor=DARK
    )

    grand_total_style = ParagraphStyle(
        "GrandTotalStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=TA_RIGHT,
        textColor=DARK
    )

    # =========================================================
    # SAFE DATA
    # =========================================================

    business_name = escape(str(data.get("business_name", "")))
    business_address = escape(str(data.get("business_address", "")))
    business_phone = escape(str(data.get("business_phone", "")))
    business_gst = escape(str(data.get("business_gst", "")))

    customer_name = escape(str(data.get("customer_name", "")))
    customer_address = escape(str(data.get("customer_address", "")))
    customer_phone = escape(str(data.get("customer_phone", "")))

    quote_no = escape(str(data.get("quote_no", "")))
    quote_date = escape(str(data.get("quote_date", "")))

    # =========================================================
    # PROFESSIONAL HEADER
    # =========================================================

    logo_path = data.get("logo", "")

    logo_img = ""

    if logo_path and os.path.exists(logo_path):

        try:
            logo_img = Image(
                logo_path,
                width=1.15 * inch,
                height=1.15 * inch
            )

        except Exception:
            logo_img = ""

    # Company information

    company_name = Paragraph(
        business_name,
        company_style
    )

    company_details = Paragraph(
        f"{business_address}<br/>Phone: {business_phone}<br/>GST No: {business_gst}",
        company_info_style
    )

    company = Table(
        [
            [company_name],
            [company_details]
        ],
        colWidths=[410]
    )

    company.setStyle(
        TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ])
    )

    # Header: logo + company information only.
    # Quotation number/date are shown separately below the header.

    header_left = Table(
        [
            [logo_img, company]
        ],
        colWidths=[85, 410]
    )

    header_left.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0)
        ])
    )

    header_table = Table(
        [[header_left]],
        colWidths=[495]
    )

    header_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -1), 1.2, DARK)
        ])
    )

    elements.append(header_table)

    # Compact quotation metadata -- no large QUOTATION heading.
    quote_meta = Table(
        [[
            Paragraph(f"<b>Quotation No:</b> {quote_no}", small_style),
            Paragraph(f"<b>Date:</b> {quote_date}", small_style)
        ]],
        colWidths=[247.5, 247.5]
    )

    quote_meta.setStyle(
        TableStyle([
            ("ALIGN", (0, 0), (0, 0), "LEFT"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )

    elements.append(quote_meta)

    elements.append(Spacer(1, 18))

    # =========================================================
    # CUSTOMER DETAILS
    # =========================================================

    customer_title = Paragraph(
        "CUSTOMER DETAILS",
        section_style
    )

    customer_details = Paragraph(
        f"""
        <b>{customer_name}</b><br/>
        {customer_address}<br/>
        Phone: {customer_phone}
        """,
        normal_style
    )

    customer_table = Table(
        [
            [customer_title],
            [customer_details]
        ],
        colWidths=[495]
    )

    customer_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                LIGHT
            ),

            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.7,
                BORDER
            ),

            (
                "LINEBELOW",
                (0, 0),
                (-1, 0),
                0.5,
                BORDER
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, 0),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                7
            ),

            (
                "TOPPADDING",
                (0, 1),
                (-1, 1),
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 1),
                (-1, 1),
                9
            )
        ])
    )

    elements.append(customer_table)

    elements.append(Spacer(1, 18))

    # =========================================================
    # ITEMS TABLE
    # =========================================================

    table_data = [
        [
            Paragraph("Sl", table_header_center_style),
            Paragraph("Description", table_header_left_style),
            Paragraph("Qty", table_header_center_style),
            Paragraph("Rate", table_header_right_style),
            Paragraph("Total", table_header_right_style)
        ]
    ]

    items = data.get("items", [])

    for item in items:

        description = escape(
            str(item.get("description", ""))
        )

        sl = escape(
            str(item.get("sl", ""))
        )

        qty = escape(
            str(item.get("qty", ""))
        )

        rate = escape(
            str(item.get("rate", ""))
        )

        total = escape(
            str(item.get("total", ""))
        )

        table_data.append(
            [
                Paragraph(sl, center_style),

                Paragraph(
                    description,
                    normal_style
                ),

                Paragraph(
                    qty,
                    center_style
                ),

                Paragraph(
                    f"Rs. {rate}",
                    right_style
                ),

                Paragraph(
                    f"Rs. {total}",
                    right_style
                )
            ]
        )

    items_table = Table(
        table_data,
        colWidths=[35, 235, 55, 85, 85],
        repeatRows=1
    )

    items_table.setStyle(
        TableStyle([

            # Light, readable header

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#E5E7EB")
            ),

            # Clear table borders

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.6,
                colors.HexColor("#B8C0CC")
            ),

            (
                "LINEBELOW",
                (0, 0),
                (-1, 0),
                0.8,
                colors.HexColor("#9CA3AF")
            ),

            # Vertical alignment

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            # Header padding

            (
                "TOPPADDING",
                (0, 0),
                (-1, 0),
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                9
            ),

            # Body padding

            (
                "TOPPADDING",
                (0, 1),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 1),
                (-1, -1),
                8
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            # Alternating row backgrounds

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    WHITE,
                    LIGHTER
                ]
            )
        ])
    )

    elements.append(items_table)

    elements.append(Spacer(1, 15))

    # =========================================================
    # TOTALS
    # =========================================================

    subtotal = Paragraph(
        "<b>Subtotal</b>",
        right_style
    )

    subtotal_value = Paragraph(
        f"Rs. {escape(str(data.get('subtotal', '0')))}",
        right_style
    )

    discount = Paragraph(
        "<b>Discount</b>",
        right_style
    )

    discount_value = Paragraph(
        f"Rs. {escape(str(data.get('discount', '0')))}",
        right_style
    )

    totals_rows = [
        [subtotal, subtotal_value],
        [discount, discount_value]
    ]

    tax_type = str(
        data.get("tax_type", "GST")
    )

    if tax_type.lower() != "none":

        totals_rows.append(
            [
                Paragraph(
                    f"<b>{escape(tax_type)}</b>",
                    right_style
                ),

                Paragraph(
                    f"Rs. {escape(str(data.get('gst_amount', '0')))}",
                    right_style
                )
            ]
        )

    # Grand Total

    totals_rows.append(
        [
            Paragraph(
                "<b>GRAND TOTAL</b>",
                grand_total_style
            ),

            Paragraph(
                f"<b>Rs. {escape(str(data.get('grand_total', '0')))}</b>",
                grand_total_style
            )
        ]
    )

    totals_table = Table(
        totals_rows,
        colWidths=[395, 100]
    )

    totals_table.setStyle(
        TableStyle([

            # Alignment

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "ALIGN",
                (0, 0),
                (0, -1),
                "RIGHT"
            ),

            (
                "ALIGN",
                (1, 0),
                (1, -1),
                "RIGHT"
            ),

            # Padding

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            # Grand total separator

            (
                "LINEABOVE",
                (0, -1),
                (-1, -1),
                1,
                DARK
            ),

            # Grand total background

            (
                "BACKGROUND",
                (0, -1),
                (-1, -1),
                LIGHT
            ),

            # Grand total font

            (
                "FONTNAME",
                (0, -1),
                (-1, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, -1),
                (-1, -1),
                11
            )
        ])
    )

    totals_table.hAlign = "RIGHT"

    elements.append(totals_table)

    elements.append(Spacer(1, 25))

    # =========================================================
    # TERMS & CONDITIONS
    # =========================================================

    terms_title = Paragraph(
        "<b>TERMS & CONDITIONS</b>",
        section_style
    )

    terms_text = str(
        data.get("terms", "")
    )

    terms_text = escape(terms_text)

    terms_paragraph = Paragraph(
        terms_text.replace("\n", "<br/>"),
        normal_style
    )

    terms_table = Table(
        [
            [terms_title],
            [terms_paragraph]
        ],
        colWidths=[495]
    )

    terms_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                LIGHT
            ),

            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.7,
                BORDER
            ),

            (
                "LINEBELOW",
                (0, 0),
                (-1, 0),
                0.5,
                BORDER
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, 0),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                7
            ),

            (
                "TOPPADDING",
                (0, 1),
                (-1, 1),
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 1),
                (-1, 1),
                9
            )
        ])
    )

    elements.append(
        KeepTogether(terms_table)
    )

    elements.append(Spacer(1, 30))

    # =========================================================
    # SIGNATURE
    # =========================================================

    signature_table = Table(
        [
            [
                "",
                Paragraph(
                    "<b>Authorized Signature</b>",
                    center_style
                )
            ],
            [
                "",
                Paragraph(
                    "____________________________",
                    center_style
                )
            ]
        ],
        colWidths=[340, 155]
    )

    signature_table.setStyle(
        TableStyle([

            (
                "ALIGN",
                (1, 0),
                (1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "TEXTCOLOR",
                (1, 0),
                (1, -1),
                MUTED
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3
            )
        ])
    )

    elements.append(signature_table)

    # =========================================================
    # FOOTER
    # =========================================================

    footer_business_name = str(
        data.get("business_name", "")
    )

    footer_quote_no = str(
        data.get("quote_no", "")
    )

    def add_footer(canvas, document):

        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8
        )

        canvas.setFillColor(
            MUTED
        )

        footer_text = (
            f"{footer_business_name}  •  "
            f"Quotation {footer_quote_no}"
        )

        canvas.drawCentredString(
            document.pagesize[0] / 2,
            20,
            footer_text
        )

        canvas.restoreState()

    # =========================================================
    # BUILD PDF
    # =========================================================

    doc.build(
        elements,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )