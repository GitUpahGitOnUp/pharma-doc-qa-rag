"""
Generates the two fictional sample PDFs used to test the pipeline.

All companies, people, product codes, and numbers in these files are invented.

  supplier-package-a.pdf  digital PDF, 9 pages, 7 documents
  supplier-package-b.pdf  scanned-style PDF (images only, no text layer),
                          7 pages, 6 documents; exercises the OCR path

Requires: pip install reportlab pdf2image pillow  (and poppler for pdf2image)
"""
import os
import random

from PIL import Image, ImageFilter
from pdf2image import convert_from_path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=styles["Heading3"], spaceBefore=8, spaceAfter=4)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=10, leading=14)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8, textColor=colors.grey)


def header(company, address, doc_title, doc_no):
    return [
        Paragraph(f"<b>{company}</b>", BODY),
        Paragraph(address, SMALL),
        Spacer(1, 10),
        Paragraph(doc_title, H1),
        Paragraph(f"Document No.: {doc_no}", BODY),
        Spacer(1, 8),
    ]


def table(rows, widths=None):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EEF5")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def p(text):
    return Paragraph(text, BODY)


def signature(name, title, date):
    return [Spacer(1, 18), p("Approved by:"), p(f"<b>{name}</b>, {title}"), p(f"Date: {date}")]


# --------------------------------------------------------------------------
# Package A: Northbridge Closure Systems (stoppers) -> Meridian Biologics
# --------------------------------------------------------------------------
NB = "Northbridge Closure Systems, Inc."
NB_ADDR = "4100 Harbor Point Drive, Wilmington, DE 19801, USA"


def package_a():
    s = []
    # p0 Cover Letter
    s += [p(NB), Paragraph(NB_ADDR, SMALL), Spacer(1, 14),
          p("12 March 2025"), Spacer(1, 8),
          p("To: Supplier Quality Department, Meridian Biologics"),
          p("From: Customer Quality, Northbridge Closure Systems, Inc."),
          p("Re: Supplier Documentation Package for Item NCS-2210 Grey Stopper, 20 mm"),
          Spacer(1, 10), p("Dear Supplier Quality Team,"),
          p("Please find enclosed the supplier documentation package for Item NCS-2210 Grey "
            "Stopper, 20 mm, Lot NB-24-55871. This package includes the following documents:"),
          p("1. Certificate of Quality<br/>2. Packaging Component Specification<br/>"
            "3. Animal Origin Statement<br/>4. Compliance Bulletin<br/>"
            "5. Vendor Qualification Record<br/>6. Certificate of Processing"),
          p("Please contact us with any questions regarding this package."),
          Spacer(1, 10), p("Regards,"), p("Dana Whitfield"),
          p("Customer Quality Manager, Northbridge Closure Systems, Inc."), PageBreak()]

    # p1-2 Certificate of Quality (2 pages)
    s += header(NB, NB_ADDR, "Certificate of Quality", "COQ-NB-24-55871")
    s += [table([["Field", "Value"],
                 ["Product", "NCS-2210 Grey Stopper, 20 mm"],
                 ["Batch / Lot No.", "NB-24-55871"],
                 ["Certificate Number", "CQ-7714032-0005"],
                 ["Certificate Date", "4 March 2025"],
                 ["Manufacture Date", "18 February 2025"],
                 ["Expiry Date", "17 February 2028"],
                 ["Quantity Released", "250,000 units"]], [2.2 * inch, 3.8 * inch]),
          Spacer(1, 10), Paragraph("Test Results (Part 1 of 2)", H2),
          table([["Test", "Specification", "Result"],
                 ["Flange diameter", "19.80 - 20.20 mm", "20.02 mm"],
                 ["Plug height", "7.40 - 7.80 mm", "7.61 mm"],
                 ["Hardness (Shore A)", "45 +/- 5", "46"],
                 ["Visual inspection", "No defects (AQL 0.65)", "Pass"]],
                [2.2 * inch, 2.2 * inch, 1.6 * inch]),
          Spacer(1, 6), p("Continued on next page."), PageBreak()]
    s += [Paragraph("Certificate of Quality - continued (CQ-7714032-0005)", H2),
          Paragraph("Test Results (Part 2 of 2)", H2),
          table([["Test", "Specification", "Result"],
                 ["Endotoxin", "< 0.5 EU/stopper", "< 0.1 EU/stopper"],
                 ["Bioburden", "< 10 CFU/stopper", "2 CFU/stopper"],
                 ["Particulates (>= 10 um)", "<= 20 per stopper", "6 per stopper"],
                 ["Fragmentation", "Per USP <381>", "Pass"]],
                [2.2 * inch, 2.2 * inch, 1.6 * inch]),
          Spacer(1, 8),
          p("This lot was manufactured and tested in accordance with the current approved "
            "specification and is released for shipment.")]
    s += signature("Priya Raman", "Quality Assurance Manager", "4 March 2025") + [PageBreak()]

    # p3 Packaging Component Specification
    s += header(NB, NB_ADDR, "Packaging Component Specification", "PCS-2210-REV03")
    s += [Paragraph("1. Scope", H2),
          p("This specification defines the packaging configuration for NCS-2210 Grey "
            "Stopper, 20 mm, shipped ready-to-sterilize."),
          Paragraph("2. Primary Packaging", H2),
          table([["Component", "Material / Grade", "Specification / Standard"],
                 ["Inner bag", "Low-density polyethylene, 75 um", "PKG-SPEC-104"],
                 ["Bag closure", "Polypropylene twist tie", "PKG-SPEC-109"],
                 ["Desiccant sachet", "Silica gel, 5 g", "PKG-SPEC-121"]],
                [1.6 * inch, 2.4 * inch, 2.0 * inch]),
          Paragraph("3. Secondary Packaging", H2),
          table([["Component", "Material / Grade", "Specification / Standard"],
                 ["Outer bag", "Polyethylene, 100 um", "PKG-SPEC-105"],
                 ["Shipping carton", "Corrugated fiberboard, double wall", "PKG-SPEC-140"],
                 ["Label", "Thermal transfer, lot and expiry", "PKG-SPEC-150"]],
                [1.6 * inch, 2.4 * inch, 2.0 * inch]),
          Paragraph("4. Revision History", H2),
          table([["Rev", "Date", "Change"],
                 ["01", "May 2021", "Initial release"],
                 ["02", "Aug 2023", "Desiccant sachet added"],
                 ["03", "Jan 2025", "Outer bag thickness increased to 100 um"]],
                [0.8 * inch, 1.4 * inch, 3.8 * inch]), PageBreak()]

    # p4 Animal Origin Statement
    s += header(NB, NB_ADDR, "Animal Origin Statement", "NCS-AOS-2025-004")
    s += [p("Product: NCS-2210 Grey Stopper, 20 mm"), Spacer(1, 6),
          p("Northbridge Closure Systems, Inc. confirms that the product listed above "
            "contains no materials derived from animal or human sources. No animal-derived "
            "or human-derived raw materials, processing aids, or lubricants are used in "
            "manufacture."),
          Paragraph("Regulatory Basis", H2),
          p("This statement is provided in support of EMA/410/01 rev. 3 and 21 CFR Part 211 "
            "supplier documentation requirements.")]
    s += signature("Priya Raman", "Quality Assurance Manager", "1 March 2025") + [PageBreak()]

    # p5 Compliance Bulletin
    s += header(NB, NB_ADDR, "Compliance Bulletin", "TB-2210-07")
    s += [Paragraph("Table of Contents", H2),
          p("1. Chemical Composition &nbsp; 2. Physical Properties &nbsp; 3. Regulatory Compliance"),
          Paragraph("1. Chemical Composition", H2),
          p("NCS-2210 Grey is a bromobutyl rubber formulation with a fluoropolymer film "
            "coating on the product-contact surface. The formulation is free of natural "
            "rubber latex."),
          Paragraph("2. Physical Properties", H2),
          table([["Property", "Typical Value"],
                 ["Hardness (Shore A)", "46"],
                 ["Density", "1.28 g/cm3"],
                 ["Compression set", "22%"]], [3 * inch, 3 * inch]),
          Paragraph("3. Regulatory Compliance", H2),
          p("NCS-2210 Grey Stopper complies with USP &lt;381&gt;, USP &lt;87&gt;, "
            "EP 3.2.9, and ISO 8362-2.")]
    s += [PageBreak()]

    # p6-7 Vendor Qualification Record (2 pages)
    s += header(NB, NB_ADDR, "Vendor Qualification Record", "VQR-NCS-2025")
    s += [table([["Field", "Value"],
                 ["Vendor Name", NB],
                 ["Qualification Status", "Approved"],
                 ["Approved For", "Elastomeric closures for parenteral products"],
                 ["Initial Qualification", "June 2019"],
                 ["Last Requalification", "January 2025"]], [2.2 * inch, 3.8 * inch]),
          Paragraph("Certifications", H2),
          table([["Certification", "Certificate Number", "Expiry"],
                 ["ISO 9001:2015", "QMS-NB-2023-0412", "30 Sep 2026"],
                 ["ISO 15378:2017", "PPM-NB-2024-0088", "31 Mar 2027"],
                 ["ISO 14001:2015", "EMS-NB-2022-0190", "31 Dec 2025"]],
                [2 * inch, 2.2 * inch, 1.8 * inch]),
          Spacer(1, 6), p("Sub-supplier information continues on next page."), PageBreak()]
    s += [Paragraph("Vendor Qualification Record - continued (VQR-NCS-2025)", H2),
          Paragraph("Approved Sub-Suppliers", H2),
          table([["Sub-Supplier", "Material / Service", "Status"],
                 ["Calloway Polymers Ltd.", "Bromobutyl rubber (BIIR)", "Approved"],
                 ["Fenmore Films GmbH", "Fluoropolymer coating film", "Approved"],
                 ["Ridgeline Packaging Co.", "Polyethylene bags", "Approved"]],
                [2.2 * inch, 2.4 * inch, 1.4 * inch]),
          Paragraph("Performance Metrics (2024)", H2),
          table([["Metric", "Target", "Actual"],
                 ["On-time delivery", ">= 95%", "97.8%"],
                 ["Lot acceptance rate", ">= 99%", "99.6%"],
                 ["Open CAPAs", "0", "0"]], [2.2 * inch, 1.8 * inch, 2 * inch]),
          PageBreak()]

    # p8 Certificate of Processing
    s += header("Clearwater Sterilization Services, LLC",
                "88 Industrial Parkway, Columbus, OH 43219, USA",
                "Certificate of Processing", "CP-CSS-2025-0219")
    s += [table([["Field", "Value"],
                 ["Customer", NB],
                 ["Product", "NCS-2210 Grey Stopper, 20 mm, Lot NB-24-55871"],
                 ["Sterilization Mode", "Gamma radiation (Cobalt-60)"],
                 ["Process Run ID", "GRX-2025-0447B"],
                 ["Validated Dose Range", "25.0 kGy (min) - 45.0 kGy (max)"],
                 ["Processing Date", "27 February 2025"]], [2.2 * inch, 3.8 * inch]),
          Paragraph("Dosimetry Summary", H2),
          table([["Dosimeter Location", "Measured Dose"],
                 ["Minimum dose position", "27.3 kGy"],
                 ["Maximum dose position", "41.8 kGy"]], [3 * inch, 3 * inch]),
          Spacer(1, 6),
          p("All measured doses fall within the validated range. Processing conforms "
            "to ISO 11137-1.")]
    s += signature("Marcus Lee", "Sterilization Operations Lead", "28 February 2025")
    return s


# --------------------------------------------------------------------------
# Package B: Halvorsen Bioprocess (single-use flow kits), scanned
# --------------------------------------------------------------------------
HB = "Halvorsen Bioprocess AB"
HB_ADDR = "Kvarnvagen 12, 752 28 Uppsala, Sweden"


def package_b():
    s = []
    # p0 Material Description Sheet
    s += header(HB, HB_ADDR, "Material Description Sheet: FlowLine Single-Use Kits", "MDS-FL-2024-02")
    s += [Paragraph("Materials of Construction", H2),
          table([["Component", "Material"],
                 ["Tubing", "Platinum-cured silicone"],
                 ["Connectors", "Polycarbonate"],
                 ["Mixing chamber", "Polypropylene"],
                 ["Pressure sensor housing", "Polysulfone"]], [3 * inch, 3 * inch]),
          Paragraph("Physical Properties", H2),
          table([["Property", "Value"],
                 ["Operating temperature", "+4 C to +37 C"],
                 ["Maximum operating pressure", "3.0 bar"],
                 ["Kit weight", "0.85 kg"]], [3 * inch, 3 * inch]),
          Paragraph("Sterilization Compatibility", H2),
          p("Supplied gamma-irradiated. Not suitable for autoclaving."), PageBreak()]

    # p1 Certificate of Quality - Low Flow kit
    for kit, lot, cert, date in [("FlowLine Low Flow Kit", "HB-77310", "HQ-2024-1183", "9 October 2024"),
                                 ("FlowLine High Flow Kit", "HB-77452", "HQ-2024-1207", "16 October 2024")]:
        s += header(HB, HB_ADDR, "Certificate of Quality", cert)
        s += [table([["Field", "Value"],
                     ["Product", kit],
                     ["Lot Number", lot],
                     ["Certificate Date", date],
                     ["Expiry Date", "36 months from manufacture"]], [2.2 * inch, 3.8 * inch]),
              Paragraph("Test Results", H2),
              table([["Test", "Specification", "Result"],
                     ["Sterility", "Sterile", "Pass"],
                     ["Endotoxin", "< 0.25 EU/mL", "< 0.05 EU/mL"],
                     ["Leak test", "No leak at 3.0 bar", "Pass"]],
                    [2.2 * inch, 2.2 * inch, 1.6 * inch])]
        s += signature("Elin Bergqvist", "QA Release Officer", date) + [PageBreak()]

    # p3-4 Packaging Component Specification (2 pages)
    s += header(HB, HB_ADDR, "Packaging Component Specification", "PCS-FL-011")
    s += [Paragraph("Scope", H2),
          p("Packaging configuration for FlowLine Single-Use Kits."),
          Paragraph("Primary Packaging", H2),
          table([["Component", "Material / Grade"],
                 ["Blister tray", "PETG, 0.8 mm"],
                 ["Lid", "Medical-grade Tyvek"]], [3 * inch, 3 * inch]),
          Spacer(1, 6), p("Continued on next page."), PageBreak()]
    s += [Paragraph("Packaging Component Specification - continued (PCS-FL-011)", H2),
          Paragraph("Secondary Packaging", H2),
          table([["Component", "Material / Grade"],
                 ["Outer pouch", "Polyethylene / nylon laminate"],
                 ["Shipping box", "Corrugated cardboard"]], [3 * inch, 3 * inch]),
          Paragraph("Revision History", H2),
          table([["Rev", "Date", "Change"],
                 ["A", "Mar 2022", "Initial release"],
                 ["B", "Jul 2024", "Lid material changed to Tyvek"]],
                [0.8 * inch, 1.4 * inch, 3.8 * inch]), PageBreak()]

    # p5 BSE/TSE Declaration
    s += header(HB, HB_ADDR, "BSE/TSE Declaration", "BSE-FL-2024")
    s += [p("Halvorsen Bioprocess AB declares that FlowLine Single-Use Kits contain no "
            "materials of animal origin (bovine, ovine, caprine, or porcine)."),
          p("This declaration is based on a BSE/TSE risk assessment in accordance with "
            "EMA/410/01 rev. 3. Assessment reference: TSE-RA-2024-FL-003.")]
    s += signature("Elin Bergqvist", "QA Release Officer", "2 September 2024") + [PageBreak()]

    # p6 Chain of Custody
    s += header(HB, HB_ADDR, "Global Chain of Custody", "COC-FL-2024")
    s += [p("Prepared by: Supply Chain Quality, Halvorsen Bioprocess AB"),
          Paragraph("Assemblies Covered", H2),
          p("FlowLine Low Flow Kit; FlowLine High Flow Kit"),
          Paragraph("Supply Chain Steps", H2),
          p("1. Raw material receipt and incoming inspection (Uppsala, Sweden)<br/>"
            "2. Component molding and tubing extrusion (Uppsala, Sweden)<br/>"
            "3. Cleanroom assembly and packaging (Tallinn, Estonia)<br/>"
            "4. Gamma sterilization (contract sterilizer, Germany)<br/>"
            "5. Distribution to end customer"),
          Paragraph("Traceability Statement", H2),
          p("Each kit carries a unique lot number traceable to raw material lots, "
            "assembly date, and cleanroom operator records.")]
    return s


def build(path, story):
    SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                      topMargin=0.7 * inch, bottomMargin=0.7 * inch,
                      title="Fictional sample document", author="Sample data generator").build(story)


def make_scanned(src, dst, seed=7):
    """Rasterize each page and add slight skew and blur so it reads like a scan."""
    rng = random.Random(seed)
    pages = []
    for img in convert_from_path(src, dpi=150):
        img = img.convert("L").rotate(rng.uniform(-0.8, 0.8), expand=False, fillcolor=255)
        img = img.filter(ImageFilter.GaussianBlur(0.4))
        pages.append(img.convert("RGB"))
    pages[0].save(dst, save_all=True, append_images=pages[1:], resolution=150)


if __name__ == "__main__":
    build(os.path.join(HERE, "supplier-package-a.pdf"), package_a())
    tmp = os.path.join(HERE, "_package-b-digital.pdf")
    build(tmp, package_b())
    make_scanned(tmp, os.path.join(HERE, "supplier-package-b.pdf"))
    os.remove(tmp)
    print("Wrote supplier-package-a.pdf and supplier-package-b.pdf")
