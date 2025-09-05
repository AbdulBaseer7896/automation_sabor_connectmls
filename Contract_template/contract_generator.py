# import json
# import os
# from datetime import datetime
# from reportlab.lib.pagesizes import letter, inch
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
# from reportlab.lib import colors
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.fonts import addMapping
# from reportlab.pdfgen import canvas

# # Try to register fonts (adjust paths as needed)
# try:
#     pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
#     pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial-Bold.ttf'))
#     addMapping('Arial', 0, 0, 'Arial')
#     addMapping('Arial', 1, 0, 'Arial-Bold')
#     primary_font = 'Arial'
#     bold_font = 'Arial-Bold'
# except:
#     primary_font = 'Helvetica'
#     bold_font = 'Helvetica-Bold'
#     print("Note: Using default fonts as Arial wasn't available")

# def create_header_footer(canvas, doc, json_data):
#     """Create header and footer for each page"""
#     canvas.saveState()
    
#     # Header
#     canvas.setFont(primary_font, 8)
#     canvas.drawRightString(7.5*inch, 10.5*inch, f"Docusign Envelope ID: {json_data.get('docusign_id', 'AA36957E-5678-43F3-B524-A4EBF6685470')}")
#     canvas.drawRightString(7.5*inch, 10.3*inch, datetime.now().strftime("%m-%d-%Y"))
    
#     # Footer
#     canvas.setFont(primary_font, 7)
#     broker_info = json_data.get('broker_info', {})
#     footer_text = f"{broker_info.get('office_name', '')}, {broker_info.get('street_address', '')} {broker_info.get('city_state_zip', '')} Phone: {broker_info.get('phone', '')}"
#     canvas.drawString(0.5*inch, 0.5*inch, footer_text)
    
#     # Page number
#     canvas.drawRightString(7.5*inch, 0.5*inch, f"Page {doc.page} of 11")
    
#     canvas.restoreState()

# def create_contract_pdf(json_data, output_path):
#     # Create document with letter size
#     doc = SimpleDocTemplate(output_path, pagesize=letter,
#                             rightMargin=72, leftMargin=72,
#                             topMargin=90, bottomMargin=72)
    
#     # Container for the 'Flowable' objects
#     elements = []
    
#     # Get sample style sheet
#     styles = getSampleStyleSheet()
    
#     # Create custom styles
#     title_style = ParagraphStyle(
#         'CustomTitle',
#         parent=styles['Heading1'],
#         fontName=bold_font,
#         fontSize=14,
#         spaceAfter=12,
#         alignment=TA_CENTER
#     )
    
#     section_style = ParagraphStyle(
#         'SectionTitle',
#         parent=styles['Heading2'],
#         fontName=bold_font,
#         fontSize=10,
#         spaceAfter=6,
#         spaceBefore=12
#     )
    
#     normal_style = ParagraphStyle(
#         'Normal',
#         parent=styles['Normal'],
#         fontName=primary_font,
#         fontSize=9,
#         spaceAfter=6,
#         alignment=TA_JUSTIFY
#     )
    
#     bold_style = ParagraphStyle(
#         'Bold',
#         parent=styles['Normal'],
#         fontName=bold_font,
#         fontSize=9
#     )
    
#     small_style = ParagraphStyle(
#         'Small',
#         parent=styles['Normal'],
#         fontName=primary_font,
#         fontSize=8
#     )
    
#     # Add title
#     title = Paragraph("PROMULGATED BY THE TEXAS REAL ESTATE COMMISSION (TREC)<br/>ONE TO FOUR FAMILY RESIDENTIAL CONTRACT (RESALE)", title_style)
#     elements.append(title)
    
#     notice = Paragraph("NOTICE: Not For Use For Condominium Transactions", bold_style)
#     elements.append(notice)
#     elements.append(Spacer(1, 0.2*inch))
    
#     # 1. PARTIES
#     parties_section = Paragraph("1. PARTIES:", section_style)
#     elements.append(parties_section)
    
#     parties_text = "The parties to this contract are SECRETARY OF VETERANS AFFAIRS (Seller) and Silverkey investments LLC or Designated entity (Buyer). Seller agrees to sell and convey to Buyer and Buyer agrees to buy from Seller the Property defined below."
#     parties_para = Paragraph(parties_text, normal_style)
#     elements.append(parties_para)
#     elements.append(Spacer(1, 0.1*inch))
    
#     # 2. PROPERTY
#     property_section = Paragraph("2. PROPERTY:", section_style)
#     elements.append(property_section)
    
#     property_text = "The land, improvements and accessories are collectively referred to as the Property (Property)."
#     property_para = Paragraph(property_text, normal_style)
#     elements.append(property_para)
    
#     # A. LAND
#     land_text = f"A. LAND: Lot {json_data.get('Lot', 'N/A')} Block {json_data.get('Block', 'N/A')} {json_data.get('Subdivision_Legal_Name', 'N/A')} Addition, City of San Antonio County of {json_data.get('contry', 'N/A')}, Texas, known as {json_data.get('address', 'N/A')}"
#     land_para = Paragraph(land_text, normal_style)
#     elements.append(land_para)
    
#     # B. IMPROVEMENTS
#     improvements_text = "B. IMPROVEMENTS: The house, garage and all other fixtures and improvements attached to the above-described real property, including without limitation, the following permanently installed and built-in items, if any: all equipment and appliances, balances, screens, shutters, awnings, wall-to-wall carpeting, mirrors, ceiling fans, attic fans, mail boxes, television antennas, mounts and brackets for televisions and speakers, heating and air-conditioning units, security and fire detection equipment, wiring, plumbing and lighting fixtures, chandeliers, water softener system, kitchen equipment, garage door openers, cleaning equipment, shrubbery, landscaping, outdoor cooking equipment, and all other property attached to the above described real property."
#     improvements_para = Paragraph(improvements_text, normal_style)
#     elements.append(improvements_para)
    
#     # C. ACCESSORIES
#     accessories_text = "C. ACCESSORIES: The following described related accessories, if any: window air conditioning units, stove, fireplace screens, curtains and rods, blinds, window shades, draperies and rods, door keys, mailbox keys, above ground pool, swimming pool equipment and maintenance accessories, artificial fireplace logs, security systems that are not fixtures, and controls for: (i) garage doors, (ii) entry gates, and (iii) other improvements and accessories. 'Controls' includes Seller's transferable rights to the (i) software and applications used to access and control improvements or accessories, and (ii) hardware used solely to control improvements or accessories."
#     accessories_para = Paragraph(accessories_text, normal_style)
#     elements.append(accessories_para)
    
#     # D. EXCLUSIONS
#     exclusions_text = "D. EXCLUSIONS: The following improvements and accessories will be retained by Seller and must be removed prior to delivery of possession: N/A"
#     exclusions_para = Paragraph(exclusions_text, normal_style)
#     elements.append(exclusions_para)
    
#     # E. RESERVATIONS
#     reservations_text = "E. RESERVATIONS: Any reservation for oil, gas, or other minerals, water, timber, or other interests is made in accordance with an attached addendum."
#     reservations_para = Paragraph(reservations_text, normal_style)
#     elements.append(reservations_para)
#     elements.append(Spacer(1, 0.1*inch))
    
#     # 3. SALES PRICE
#     sales_section = Paragraph("3. SALES PRICE:", section_style)
#     elements.append(sales_section)
    
#     admin_data = json_data.get('admin_data', {})
    
#     # Create a table for sales price details
#     sales_data = [
#         ["A. Cash portion of Sales Price payable by Buyer at closing ......", f"$ {admin_data.get('sales_price', 'N/A')}"],
#         ["B. Sum of all financing described in the attached: [X] Third Party Financing Addendum,", "$ 135,000.00"],
#         ["C. Sales Price (Sum of A and B) ......", "$ 135,000.00"]
#     ]
    
#     sales_table = Table(sales_data, colWidths=[4.5*inch, 1.5*inch])
#     sales_table.setStyle(TableStyle([
#         ('FONT', (0, 0), (-1, -1), primary_font),
#         ('FONTSIZE', (0, 0), (-1, -1), 9),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#     ]))
    
#     elements.append(sales_table)
#     elements.append(Spacer(1, 0.1*inch))
    
#     # Add page break for the rest of the contract
#     elements.append(PageBreak())
    
#     # 5. EARNEST MONEY AND TERMINATION OPTION
#     earnest_section = Paragraph("5. EARNEST MONEY AND TERMINATION OPTION:", section_style)
#     elements.append(earnest_section)
    
#     # A. DELIVERY OF EARNEST MONEY AND OPTION FEE
#     earnest_a_text = f"A. DELIVERY OF EARNEST MONEY AND OPTION FEE: Within 3 days after the Effective Date, Buyer must deliver to ______ Buyer's Choice ______ (Escrow Agent) at ______ ______ (address): $ {admin_data.get('earnest_money', 'N/A')} ______ as earnest money and ${admin_data.get('option_fee', 'N/A')} ______ as the Option Fee. The earnest money and Option Fee shall be made payable to Escrow Agent and may be paid separately or combined in a single payment."
#     earnest_a_para = Paragraph(earnest_a_text, normal_style)
#     elements.append(earnest_a_para)
    
#     # Continue with other sections as needed...
    
#     # Since the contract is lengthy, we'll add a few more key sections
    
#     # 6. TITLE POLICY AND SURVEY
#     title_section = Paragraph("6. TITLE POLICY AND SURVEY:", section_style)
#     elements.append(title_section)
    
#     title_text = f"A. TITLE POLICY: Seller shall furnish to Buyer at ☑ Seller's Buyer's expense an owner policy of title insurance (Title Policy) issued by ______ {json_data.get('Preferred_Title_Company', 'N/A')} ______ (Title Company) in the amount of the Sales Price, dated at or after closing, insuring Buyer against loss under the provisions of the Title Policy, subject to the promulgated exclusions (including existing building and zoning ordinances) and the following exceptions:"
#     title_para = Paragraph(title_text, normal_style)
#     elements.append(title_para)
    
#     # Continue with other sections...
    
#     # Add signature section at the end
#     elements.append(Spacer(1, 0.3*inch))
    
#     sign_data = [
#         ["Buyer's Signature:", "Date:"],
#         ["", ""],
#         ["Seller's Signature:", "Date:"],
#         ["", ""],
#     ]
    
#     sign_table = Table(sign_data, colWidths=[2.5*inch, 2.5*inch])
#     sign_table.setStyle(TableStyle([
#         ('LINEABOVE', (0, 1), (0, 1), 1, colors.black),
#         ('LINEABOVE', (1, 1), (1, 1), 1, colors.black),
#         ('LINEABOVE', (0, 3), (0, 3), 1, colors.black),
#         ('LINEABOVE', (1, 3), (1, 3), 1, colors.black),
#         ('FONT', (0, 0), (-1, -1), primary_font),
#         ('FONTSIZE', (0, 0), (-1, -1), 10),
#     ]))
    
#     elements.append(sign_table)
    
#     # Build the PDF with header and footer
#     doc.build(elements, onFirstPage=lambda c, d: create_header_footer(c, d, json_data), 
#               onLaterPages=lambda c, d: create_header_footer(c, d, json_data))
    
#     return output_path

# # Example usage
# if __name__ == "__main__":
#     # Sample JSON data (replace with your actual JSON)
#     sample_json = {
#         "contry": "Bexar",
#         "Lot": "36",
#         "Block": "1",
#         "Subdivision_Legal_Name": "HEIGHTS OF WESTCREEK PH 1",
#         "address": "1208 Creek Knoll , San Antonio, Texas 78253-5391",
#         "Preferred_Title_Company": "University Title",
#         "Listing_Associate_Email_Address": "jboggs@kw.com",
#         "broker_info": {
#             "office_name": "Keller Williams Heritage",
#             "office_type": "Realty",
#             "office_id": "KLWM00",
#             "email": "broker@mykwsa.com",
#             "website": "https://www.heritagepropertymanagementsa.com/",
#             "street_address": "1717 N. Loop 1604 E",
#             "city_state_zip": "San Antonio TX, 78232",
#             "phone": "(210) 493-3030"
#         },
#         "admin_data": {
#             "state": "Punjab",
#             "sales_price": "1000",
#             "earnest_money": "2000",
#             "option_fee": "100",
#             "buyer_approval_deadline_days": "",
#             "survey_delivery_deadline_days": ""
#         },
#         "csvFilepath": "CSVstore\\Testing_20250905-161919.csv",
#         "docusign_id": "AA36957E-5678-43F3-B524-A4EBF6685470"
#     }
    
#     # Generate the PDF
#     output_path = "real_estate_contract.pdf"
#     create_contract_pdf(sample_json, output_path)
#     print(f"PDF generated successfully: {output_path}")









import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.pdfgen import canvas

class RealEstateContractGenerator:
    def __init__(self, json_data):
        self.json_data = json_data
        self.story = []
        self.setup_styles()
        
    def setup_styles(self):
        # Try to register fonts
        try:
            pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
            pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial-Bold.ttf'))
            addMapping('Arial', 0, 0, 'Arial')
            addMapping('Arial', 1, 0, 'Arial-Bold')
            self.primary_font = 'Arial'
            self.bold_font = 'Arial-Bold'
        except:
            self.primary_font = 'Helvetica'
            self.bold_font = 'Helvetica-Bold'
        
        # Create custom styles
        styles = getSampleStyleSheet()
        
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=self.bold_font,
            fontSize=14,
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        self.section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontName=self.bold_font,
            fontSize=10,
            spaceAfter=6,
            spaceBefore=12
        )
        
        self.normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontName=self.primary_font,
            fontSize=9,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        self.bold_style = ParagraphStyle(
            'Bold',
            parent=styles['Normal'],
            fontName=self.bold_font,
            fontSize=9
        )
        
        self.small_style = ParagraphStyle(
            'Small',
            parent=styles['Normal'],
            fontName=self.primary_font,
            fontSize=8
        )
        
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontName=self.primary_font,
            fontSize=7,
            alignment=TA_CENTER
        )
    
    def create_header_footer(self, canvas, doc):
        canvas.saveState()
        
        # Header
        canvas.setFont(self.primary_font, 8)
        canvas.drawRightString(7.5*inch, 10.5*inch, f"Docusign Envelope ID: {self.json_data.get('docusign_id', 'AA36957E-5678-43F3-B524-A4EBF6685470')}")
        canvas.drawRightString(7.5*inch, 10.3*inch, datetime.now().strftime("%m-%d-%Y"))
        
        # Footer
        canvas.setFont(self.primary_font, 7)
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', '')}, {broker_info.get('street_address', '')} {broker_info.get('city_state_zip', '')} Phone: {broker_info.get('phone', '')}"
        canvas.drawString(0.5*inch, 0.5*inch, footer_text)
        
        # Page number
        canvas.drawRightString(7.5*inch, 0.5*inch, f"Page {doc.page} of 11")
        
        canvas.restoreState()
    
    def add_title_section(self):
        title = Paragraph("PROMULGATED BY THE TEXAS REAL ESTATE COMMISSION (TREC)<br/>ONE TO FOUR FAMILY RESIDENTIAL CONTRACT (RESALE)", self.title_style)
        self.story.append(title)
        
        notice = Paragraph("NOTICE: Not For Use For Condominium Transactions", self.bold_style)
        self.story.append(notice)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_parties_section(self):
        parties_section = Paragraph("1. PARTIES:", self.section_style)
        self.story.append(parties_section)
        
        parties_text = "The parties to this contract are SECRETARY OF VETERANS AFFAIRS (Seller) and Silverkey investments LLC or Designated entity (Buyer). Seller agrees to sell and convey to Buyer and Buyer agrees to buy from Seller the Property defined below."
        parties_para = Paragraph(parties_text, self.normal_style)
        self.story.append(parties_para)
        self.story.append(Spacer(1, 0.1*inch))
    
    def add_property_section(self):
        property_section = Paragraph("2. PROPERTY:", self.section_style)
        self.story.append(property_section)
        
        property_text = "The land, improvements and accessories are collectively referred to as the Property (Property)."
        property_para = Paragraph(property_text, self.normal_style)
        self.story.append(property_para)
        
        # A. LAND
        land_text = f"A. LAND: Lot {self.json_data.get('Lot', 'N/A')} Block {self.json_data.get('Block', 'N/A')} {self.json_data.get('Subdivision_Legal_Name', 'N/A')} Addition, City of San Antonio County of {self.json_data.get('contry', 'N/A')}, Texas, known as {self.json_data.get('address', 'N/A')}"
        land_para = Paragraph(land_text, self.normal_style)
        self.story.append(land_para)
        
        # B. IMPROVEMENTS
        improvements_text = "B. IMPROVEMENTS: The house, garage and all other fixtures and improvements attached to the above-described real property, including without limitation, the following permanently installed and built-in items, if any: all equipment and appliances, balances, screens, shutters, awnings, wall-to-wall carpeting, mirrors, ceiling fans, attic fans, mail boxes, television antennas, mounts and brackets for televisions and speakers, heating and air-conditioning units, security and fire detection equipment, wiring, plumbing and lighting fixtures, chandeliers, water softener system, kitchen equipment, garage door openers, cleaning equipment, shrubbery, landscaping, outdoor cooking equipment, and all other property attached to the above described real property."
        improvements_para = Paragraph(improvements_text, self.normal_style)
        self.story.append(improvements_para)
        
        # C. ACCESSORIES
        accessories_text = "C. ACCESSORIES: The following described related accessories, if any: window air conditioning units, stove, fireplace screens, curtains and rods, blinds, window shades, draperies and rods, door keys, mailbox keys, above ground pool, swimming pool equipment and maintenance accessories, artificial fireplace logs, security systems that are not fixtures, and controls for: (i) garage doors, (ii) entry gates, and (iii) other improvements and accessories. 'Controls' includes Seller's transferable rights to the (i) software and applications used to access and control improvements or accessories, and (ii) hardware used solely to control improvements or accessories."
        accessories_para = Paragraph(accessories_text, self.normal_style)
        self.story.append(accessories_para)
        
        # D. EXCLUSIONS
        exclusions_text = "D. EXCLUSIONS: The following improvements and accessories will be retained by Seller and must be removed prior to delivery of possession: N/A"
        exclusions_para = Paragraph(exclusions_text, self.normal_style)
        self.story.append(exclusions_para)
        
        # E. RESERVATIONS
        reservations_text = "E. RESERVATIONS: Any reservation for oil, gas, or other minerals, water, timber, or other interests is made in accordance with an attached addendum."
        reservations_para = Paragraph(reservations_text, self.normal_style)
        self.story.append(reservations_para)
        self.story.append(Spacer(1, 0.1*inch))
    
    def add_sales_price_section(self):
        sales_section = Paragraph("3. SALES PRICE:", self.section_style)
        self.story.append(sales_section)
        
        admin_data = self.json_data.get('admin_data', {})
        
        # Create a table for sales price details
        sales_data = [
            ["A. Cash portion of Sales Price payable by Buyer at closing ......", f"$ {admin_data.get('sales_price', 'N/A')}"],
            ["B. Sum of all financing described in the attached: [X] Third Party Financing Addendum,", "$ 135,000.00"],
            ["C. Sales Price (Sum of A and B) ......", "$ 135,000.00"]
        ]
        
        sales_table = Table(sales_data, colWidths=[4.5*inch, 1.5*inch])
        sales_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        self.story.append(sales_table)
        
        note_text = "The term 'Cash portion of the Sales Price' does not include proceeds from borrowing of any kind or selling other real property except as disclosed in this contract."
        note_para = Paragraph(note_text, self.normal_style)
        self.story.append(note_para)
        self.story.append(Spacer(1, 0.1*inch))
    
    def add_leases_section(self):
        leases_section = Paragraph("4. LEASES:", self.section_style)
        self.story.append(leases_section)
        
        leases_text = "Except as disclosed in this contract, Seller is not aware of any leases affecting the Property. After the Effective Date, Seller may not, without Buyer's written consent, create a new lease, amend any existing lease, or convey any interest in the Property. (Check all applicable boxes)"
        leases_para = Paragraph(leases_text, self.normal_style)
        self.story.append(leases_para)
        
        # Create checkboxes for leases
        leases_data = [
            ["[X] A. RESIDENTIAL LEASES: The Property is subject to one or more residential leases and the Addendum Regarding Residential Leases is attached to this contract.", ""],
            ["[ ] B. FIXTURE LEASES: Fixtures on the Property are subject to one or more fixture leases (for example, solar panels, propane tanks, water softener, security system) and the Addendum Regarding Fixture Leases is attached to this contract.", ""],
            ["[ ] C. NATURAL RESOURCE LEASES: 'Natural Resource Lease' means an existing oil and gas, mineral, geothermal, water, wind, or other natural resource lease affecting the Property to which Seller is a party.", ""]
        ]
        
        leases_table = Table(leases_data, colWidths=[6.5*inch, 0.5*inch])
        leases_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        self.story.append(leases_table)
        
        # Natural resource lease options
        resource_data = [
            ["(1) Seller has delivered to Buyer a copy of all the Natural Resource Leases.", ""],
            ["(2) Seller has not delivered to Buyer a copy of all the Natural Resource Leases. Seller shall provide to Buyer a copy of all the Natural Resource Leases within 3 days after the Effective Date. Buyer may terminate the contract within ______ days after the date the Buyer receives all the Natural Resource Leases and the earnest money shall be refunded to Buyer.", ""]
        ]
        
        resource_table = Table(resource_data, colWidths=[6.5*inch, 0.5*inch])
        resource_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        self.story.append(resource_table)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', '')}, {broker_info.get('street_address', '')} {broker_info.get('city_state_zip', '')} Phone: {broker_info.get('phone', '')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())
    
    def add_earnest_money_section(self):
        # Page 2 header
        address = self.json_data.get('address', 'N/A').split(',')[0]  # Get just the street address
        page_header = Paragraph(f"Contract Concerning ______ {address}, San Antonio, ______ Page 2 of 11 {datetime.now().strftime('%m-%d-%Y')}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        earnest_section = Paragraph("5. EARNEST MONEY AND TERMINATION OPTION:", self.section_style)
        self.story.append(earnest_section)
        
        admin_data = self.json_data.get('admin_data', {})
        
        # A. DELIVERY OF EARNEST MONEY AND OPTION FEE
        earnest_a_text = f"A. DELIVERY OF EARNEST MONEY AND OPTION FEE: Within 3 days after the Effective Date, Buyer must deliver to ______ Buyer's Choice ______ (Escrow Agent) at ______ ______ (address): $ {admin_data.get('earnest_money', 'N/A')} ______ as earnest money and ${admin_data.get('option_fee', 'N/A')} ______ as the Option Fee. The earnest money and Option Fee shall be made payable to Escrow Agent and may be paid separately or combined in a single payment."
        earnest_a_para = Paragraph(earnest_a_text, self.normal_style)
        self.story.append(earnest_a_para)
        
        # Subpoints
        earnest_subpoints = [
            ["(1) Buyer shall deliver additional earnest money of $ ______ to Escrow Agent within N/A days after the Effective Date of this contract.", ""],
            ["(2) If the last day to deliver the earnest money, Option Fee, or the additional earnest money falls on a Saturday, Sunday, or legal holiday, the time to deliver the earnest money, Option Fee, or the additional earnest money, as applicable, is extended until the end of the next day that is not a Saturday, Sunday, or legal holiday.", ""],
            ["(3) The amount(s) Escrow Agent receives under this paragraph shall be applied first to the Option Fee, then to the earnest money, and then to the additional earnest money.", ""],
            ["(4) Buyer authorizes Escrow Agent to release and deliver the Option Fee to Seller at any time without further notice to or consent from Buyer, and releases Escrow Agent from liability for delivery of the Option Fee to Seller. The Option Fee will be credited to the Sales Price at closing.", ""]
        ]
        
        for point in earnest_subpoints:
            point_para = Paragraph(point[0], self.normal_style)
            self.story.append(point_para)
        
        # Continue with other sections...
        # Due to the length of the contract, I'll add a few more key sections
        
        # B. TERMINATION OPTION
        earnest_b_text = "B. TERMINATION OPTION: For nominal consideration, the receipt of which Seller acknowledges, and Buyer's agreement to pay the Option Fee within the time required, Seller grants Buyer the unrestricted right to terminate this contract by giving notice of termination to Seller within 10 days after the Effective Date of this contract (Option Period). Notices under this paragraph must be given by 5:00 p.m. (local time where the Property is located) by the date specified. If Buyer gives notice of termination within the time prescribed: (i) the Option Fee will not be refunded and Escrow Agent shall release any Option Fee remaining with Escrow Agent to Seller; and (ii) any earnest money will be refunded to Buyer."
        earnest_b_para = Paragraph(earnest_b_text, self.normal_style)
        self.story.append(earnest_b_para)
        
        # C. FAILURE TO TIMELY DELIVER EARNEST MONEY
        earnest_c_text = "C. FAILURE TO TIMELY DELIVER EARNEST MONEY: If Buyer fails to deliver the earnest money within the time required, Seller may terminate this contract or exercise Seller's remedies under Paragraph 15, or both, by providing notice to Buyer before Buyer delivers the earnest money."
        earnest_c_para = Paragraph(earnest_c_text, self.normal_style)
        self.story.append(earnest_c_para)
        
        # D. FAILURE TO TIMELY DELIVER OPTION FEE
        earnest_d_text = "D. FAILURE TO TIMELY DELIVER OPTION FEE: If no dollar amount is stated as the Option Fee or if Buyer fails to deliver the Option Fee within the time required, Buyer shall not have the unrestricted right to terminate this contract under this paragraph 5."
        earnest_d_para = Paragraph(earnest_d_text, self.normal_style)
        self.story.append(earnest_d_para)
        
        # E. TIME
        earnest_e_text = "E. TIME: Time is of the essence for this paragraph and strict compliance with the time for performance is required."
        earnest_e_para = Paragraph(earnest_e_text, self.normal_style)
        self.story.append(earnest_e_para)
        self.story.append(Spacer(1, 0.1*inch))
        
        # 6. TITLE POLICY AND SURVEY
        title_section = Paragraph("6. TITLE POLICY AND SURVEY:", self.section_style)
        self.story.append(title_section)
        
        title_text = f"A. TITLE POLICY: Seller shall furnish to Buyer at ☑ Seller's Buyer's expense an owner policy of title insurance (Title Policy) issued by ______ {self.json_data.get('Preferred_Title_Company', 'N/A')} ______ (Title Company) in the amount of the Sales Price, dated at or after closing, insuring Buyer against loss under the provisions of the Title Policy, subject to the promulgated exclusions (including existing building and zoning ordinances) and the following exceptions:"
        title_para = Paragraph(title_text, self.normal_style)
        self.story.append(title_para)
        
        # Title policy exceptions
        exceptions = [
            "(1) Restrictive covenants common to the platted subdivision in which the Property is located.",
            "(2) The standard printed exception for standby fees, taxes and assessments.",
            "(3) Liens created as part of the financing described in Paragraph 3.",
            "(4) Utility easements created by the dedication deed or plat of the subdivision in which the Property is located.",
            "(5) Reservations or exceptions otherwise permitted by this contract or as may be approved by Buyer in writing.",
            "(6) The standard printed exception as to marital rights.",
            "(7) The standard printed exception as to waters, tidelands, beaches, streams, and related matters.",
            "(8) The standard printed exception as to discrepancies, conflicts, shortages in area or boundary lines, encroachments or protrusions, or overlapping improvements:",
            "☑ (i) will not be amended or deleted from the title policy; or",
            "☐ (ii) will be amended to read, 'shortages in area' at the expense of Buyer Seller.",
            "(9) The exception or exclusion regarding minerals approved by the Texas Department of Insurance."
        ]
        
        for exception in exceptions:
            exception_para = Paragraph(exception, self.normal_style)
            self.story.append(exception_para)
        
        # Continue with other sections...
        self.story.append(PageBreak())
    
    def add_signature_section(self):
        # Add signature section at the end
        self.story.append(Spacer(1, 0.3*inch))
        
        sign_data = [
            ["Buyer's Signature:", "Date:"],
            ["", ""],
            ["Seller's Signature:", "Date:"],
            ["", ""],
        ]
        
        sign_table = Table(sign_data, colWidths=[2.5*inch, 2.5*inch])
        sign_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 1), (0, 1), 1, colors.black),
            ('LINEABOVE', (1, 1), (1, 1), 1, colors.black),
            ('LINEABOVE', (0, 3), (0, 3), 1, colors.black),
            ('LINEABOVE', (1, 3), (1, 3), 1, colors.black),
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        
        self.story.append(sign_table)
    
    def generate_pdf(self, output_path):
        # Create document with letter size
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=90, bottomMargin=72)
        
        # Add all sections to the story
        self.add_title_section()
        self.add_parties_section()
        self.add_property_section()
        self.add_sales_price_section()
        self.add_leases_section()
        self.add_earnest_money_section()
        self.add_signature_section()
        
        # Build the PDF with header and footer
        doc.build(self.story, onFirstPage=self.create_header_footer, 
                  onLaterPages=self.create_header_footer)
        
        return output_path

# Example usage
if __name__ == "__main__":
    # Sample JSON data (replace with your actual JSON)
    sample_json = {
        "contry": "Bexar",
        "Lot": "36",
        "Block": "1",
        "Subdivision_Legal_Name": "HEIGHTS OF WESTCREEK PH 1",
        "address": "1208 Creek Knoll , San Antonio, Texas 78253-5391",
        "Preferred_Title_Company": "University Title",
        "Listing_Associate_Email_Address": "jboggs@kw.com",
        "broker_info": {
            "office_name": "Keller Williams Heritage",
            "office_type": "Realty",
            "office_id": "KLWM00",
            "email": "broker@mykwsa.com",
            "website": "https://www.heritagepropertymanagementsa.com/",
            "street_address": "1717 N. Loop 1604 E",
            "city_state_zip": "San Antonio TX, 78232",
            "phone": "(210) 493-3030"
        },
        "admin_data": {
            "state": "Punjab",
            "sales_price": "1000",
            "earnest_money": "2000",
            "option_fee": "100",
            "buyer_approval_deadline_days": "",
            "survey_delivery_deadline_days": ""
        },
        "csvFilepath": "CSVstore\\Testing_20250905-161919.csv",
        "docusign_id": "AA36957E-5678-43F3-B524-A4EBF6685470"
    }
    
    # Generate the PDF
    generator = RealEstateContractGenerator(sample_json)
    output_path = "real_estate_contract.pdf"
    generator.generate_pdf(output_path)
    print(f"PDF generated successfully: {output_path}")