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
from io import BytesIO

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
        docusign_id = self.json_data.get('docusign_id', 'AA36957E-5678-43F3-B524-A4E6F6685470')
        canvas.drawRightString(7.5*inch, 10.5*inch, f"Docusign Envelope ID: {docusign_id}")
        
        # Date - use provided date or current date
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        canvas.drawRightString(7.5*inch, 10.3*inch, contract_date)
        
        # Footer
        canvas.setFont(self.primary_font, 7)
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
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
        
        seller = self.json_data.get('seller', 'SECRETARY OF VETERANS AFFAIRS')
        buyer = self.json_data.get('buyer', 'Silverkey investments LLC or Designated entity')
        parties_text = f"The parties to this contract are {seller} (Seller) and {buyer} (Buyer). Seller agrees to sell and convey to Buyer and Buyer agrees to buy from Seller the Property defined below."
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
        lot = self.json_data.get('Lot', '36')
        block = self.json_data.get('Block', '1')
        subdivision = self.json_data.get('Subdivision_Legal_Name', 'HEIGHTS OF WESTCREEK PH 1')
        country = self.json_data.get('contry', 'Bexar')
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253')
        
        land_text = f"A. LAND: Lot {lot} Block {block} {subdivision} Addition, City of San Antonio County of {country}, Texas, known as {address} (address/zip code), or as described on attached exhibit."
        land_para = Paragraph(land_text, self.normal_style)
        self.story.append(land_para)
        
        # B. IMPROVEMENTS
        improvements_text = "B. IMPROVEMENTS: The house, garage and all other fixtures and improvements attached to the above-described real property, including without limitation, the following permanently installed and built-in items, if any: all equipment and appliances, valances, screens, shutters, awnings, wall-to-wall carpeting, mirrors, ceiling fans, attic fans, mail boxes, television antennas, mounts and brackets for televisions and speakers, heating and air-conditioning units, security and fire detection equipment, wiring, plumbing and lighting fixtures, chandeliers, water softener system, kitchen equipment, garage door openers, cleaning equipment, shrubbery, landscaping, outdoor cooking equipment, and all other property attached to the above described real property."
        improvements_para = Paragraph(improvements_text, self.normal_style)
        self.story.append(improvements_para)
        
        # C. ACCESSORIES
        accessories_text = 'C. ACCESSORIES: The following described related accessories, if any: window air conditioning units, stove, fireplace screens, curtains and rods, blinds, window shades, draperies and rods, door keys, mailbox keys, above ground pool, swimming pool equipment and maintenance accessories, artificial fireplace logs, security systems that are not fixtures, and controls for: (i) garage doors, (ii) entry gates, and (iii) other improvements and accessories. "Controls" includes Seller\'s transferable rights to the (i) software and applications used to access and control improvements or accessories, and (ii) hardware used solely to control improvements or accessories.'
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
        sales_price = admin_data.get('sales_price', '135,000.00')
        
        # Create a table for sales price details
        sales_data = [
            ["A. Cash portion of Sales Price payable by Buyer at closing ......", "$ ______"],
            ["B. Sum of all financing described in the attached: ☑ Third Party Financing Addendum,", f"$ {sales_price}"],
            ["C. Sales Price (Sum of A and B) ......", f"$ {sales_price}"]
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
            ["□ A. RESIDENTIAL LEASES: The Property is subject to one or more residential leases and the Addendum Regarding Residential Leases is attached to this contract.", ""],
            ["□ B. FIXTURE LEASES: Fixtures on the Property are subject to one or more fixture leases (for example, solar panels, propane tanks, water softener, security system) and the Addendum Regarding Fixture Leases is attached to this contract.", ""],
            ["□ C. NATURAL RESOURCE LEASES: 'Natural Resource Lease' means an existing oil and gas, mineral, geothermal, water, wind, or other natural resource lease affecting the Property to which Seller is a party.", ""]
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
            ["□ (1) Seller has delivered to Buyer a copy of all the Natural Resource Leases.", ""],
            ["□ (2) Seller has not delivered to Buyer a copy of all the Natural Resource Leases. Seller shall provide to Buyer a copy of all the Natural Resource Leases within 3 days after the Effective Date. Buyer may terminate the contract within ______ days after the date the Buyer receives all the Natural Resource Leases and the earnest money shall be refunded to Buyer.", ""]
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
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())
    
    def generate_pdf(self, output_path):
        # Create document with letter size
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=90, bottomMargin=72)
        
        # Add all sections to the story for the first page
        self.add_title_section()
        self.add_parties_section()
        self.add_property_section()
        self.add_sales_price_section()
        self.add_leases_section() 
        self.add_earnest_money_section() 
        
        # Build the PDF with header and footer
        doc.build(self.story, onFirstPage=self.create_header_footer, 
                  onLaterPages=self.create_header_footer)
        
        return output_path
    





    def add_earnest_money_section(self):
        # Page 2 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 2 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        earnest_section = Paragraph("5. EARNEST MONEY AND TERMINATION OPTION:", self.section_style)
        self.story.append(earnest_section)
        
        admin_data = self.json_data.get('admin_data', {})
        earnest_money = admin_data.get('earnest_money', '1,000.00')
        option_fee = admin_data.get('option_fee', '100.00')
        
        # A. DELIVERY OF EARNEST MONEY AND OPTION FEE
        earnest_a_text = f"A. DELIVERY OF EARNEST MONEY AND OPTION FEE: Within 3 days after the Effective Date, Buyer must deliver to Buyer's Choice (Escrow Agent) at (address): $ {earnest_money} as earnest money and ${option_fee} as the Option Fee. The earnest money and Option Fee shall be made payable to Escrow Agent and may be paid separately or combined in a single payment."
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
    
    def add_title_policy_section(self):
        title_section = Paragraph("6. TITLE POLICY AND SURVEY:", self.section_style)
        self.story.append(title_section)
        
        title_company = self.json_data.get('Preferred_Title_Company', "Buyer's Choice")
        
        # A. TITLE POLICY
        title_a_text = f"A. TITLE POLICY: Seller shall furnish to Buyer at ☑ Seller's☐ Buyer's expense an owner policy of title insurance (Title Policy) issued by {title_company} (Title Company) in the amount of the Sales Price, dated at or after closing, insuring Buyer against loss under the provisions of the Title Policy, subject to the promulgated exclusions (including existing building and zoning ordinances) and the following exceptions:"
        title_a_para = Paragraph(title_a_text, self.normal_style)
        self.story.append(title_a_para)
        
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
        
        # B. COMMITMENT
        title_b_text = "B. COMMITMENT: Within 20 days after the Title Company receives a copy of this contract, Seller shall furnish to Buyer a commitment for title insurance (Commitment) and, at Buyer's expense, legible copies of restrictive covenants and documents evidencing exceptions in the Commitment (Exception Documents) other than the standard printed exceptions. Seller authorizes the Title Company to deliver the Commitment and Exception Documents to Buyer at Buyer's address shown in Paragraph 21. If the Commitment and Exception Documents are not delivered to Buyer within the specified time, the time for delivery will be automatically extended up to 15 days or 3 days before the Closing Date, whichever is earlier. If the Commitment and Exception Documents are not delivered within the time required, Buyer may terminate this contract and the earnest money will be refunded to Buyer."
        title_b_para = Paragraph(title_b_text, self.normal_style)
        self.story.append(title_b_para)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())



    def add_survey_section(self):
        # Page 3 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 3 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # C. SURVEY (Continuation of Section 6)
        survey_section = Paragraph("C. SURVEY: The survey must be made by a registered professional land surveyor acceptable to the Title Company and Buyer's lender(s). (Check one box only)", self.normal_style)
        self.story.append(survey_section)
        
        # Survey options
        survey_options = [
            ["(1) Within 7 days after the Effective Date of this contract, Seller shall furnish to Buyer and Title Company Seller's existing survey of the Property and a Residential Real Property Affidavit or Declaration promulgated by the Texas Department of Insurance (T-47 Affidavit or T-47.1 Declaration). Buyer shall obtain a new survey at Seller's expense no later than 3 days prior to Closing Date if Seller fails to furnish within the time prescribed both the: (i) existing survey; and (ii) affidavit or declaration. If the Title Company or Buyer's lender does not accept the existing survey, or the affidavit or declaration, Buyer shall obtain a new survey at Seller's Buyer's expense no later than 3 days prior to Closing Date.", ""],
            ["(2) Within N/A days after the Effective Date of this contract, Buyer may obtain a new survey at Buyer's expense. Buyer is deemed to receive the survey on the date of actual receipt or the date specified in this paragraph, whichever is earlier. If Buyer fails to obtain the survey, Buyer may not terminate the contract under Paragraph 2B of the Third Party Financing Addendum because the survey was not obtained.", ""],
            ["(3) Within N/A days after the Effective Date of this contract, Seller, at Seller's expense shall furnish a new survey to Buyer.", ""]
        ]
        
        for option in survey_options:
            option_para = Paragraph(option[0], self.normal_style)
            self.story.append(option_para)
            self.story.append(Spacer(1, 0.05*inch))
        
        # D. OBJECTIONS
        objections_section = Paragraph("D. OBJECTIONS:", self.section_style)
        self.story.append(objections_section)
        
        objections_text = "Buyer may object in writing to defects, exceptions, or encumbrances to title: disclosed on the survey other than items 6A(1) through (7) above; disclosed in the Commitment other than items 6A(1) through (9) above; or which prohibit the following use or activity: Buyer must object the earlier of (i) the Closing Date or (ii) 10 days after Buyer receives the Commitment, Exception Documents, and the survey. Buyer's failure to object within the time allowed will constitute a waiver of Buyer's right to object; except that the requirements in Schedule C of the Commitment are not waived by Buyer. Provided Seller is not obligated to incur any expense, Seller shall cure any timely objections of Buyer or any third party lender within 15 days after Seller receives the objections (Cure Period) and the Closing Date will be extended as necessary. If objections are not cured within the Cure Period, Buyer may, by delivering notice to Seller within 5 days after the end of the Cure Period: (i) terminate this contract and the earnest money will be refunded to Buyer; or (ii) waive the objections. If Buyer does not terminate within the time required, Buyer shall be deemed to have waived the objections. If the Commitment or survey is revised or any new Exception Document(s) is delivered, Buyer may object to any new matter revealed in the revised Commitment or survey or new Exception Document(s) within the same time stated in this paragraph to make objections beginning when the revised Commitment, survey, or Exception Document(s) is delivered to Buyer."
        objections_para = Paragraph(objections_text, self.normal_style)
        self.story.append(objections_para)
        self.story.append(Spacer(1, 0.1*inch))
        
        # E. TITLE NOTICES
        title_notices_section = Paragraph("E. TITLE NOTICES:", self.section_style)
        self.story.append(title_notices_section)
        
        # (1) ABSTRACT OR TITLE POLICY
        abstract_text = "(1) ABSTRACT OR TITLE POLICY: Broker advises Buyer to have an abstract of title covering the Property examined by an attorney of Buyer's selection, or Buyer should be furnished with or obtain a Title Policy. If a Title Policy is furnished, the Commitment should be promptly reviewed by an attorney of Buyer's choice due to the time limitations on Buyer's right to object."
        abstract_para = Paragraph(abstract_text, self.normal_style)
        self.story.append(abstract_para)
        
        # (2) MEMBERSHIP IN PROPERTY OWNERS ASSOCIATION(S)
        association_text = "(2) MEMBERSHIP IN PROPERTY OWNERS ASSOCIATION(S): The Property ☐ is ☑ is not subject to mandatory membership in a property owners association(s). If the Property is subject to mandatory membership in a property owners association(s), Seller notifies Buyer under §5.012, Texas Property Code, that, as a purchaser of property in the residential community identified in Paragraph 2A in which the Property is located, you are obligated to be a member of the property owners association(s). Restrictive covenants governing the use and occupancy of the Property and all dedicatory instruments governing the establishment, maintenance, or operation of this residential community have been or will be recorded in the Real Property Records of the county in which the Property is located. Copies of the restrictive covenants and dedicatory instruments may be obtained from the county clerk. You are obligated to pay assessments to the property owners association(s). The amount of the assessments is subject to change. Your failure to pay the assessments could result in enforcement of the association's lien on and the foreclosure of the Property."
        association_para = Paragraph(association_text, self.normal_style)
        self.story.append(association_para)
        
        association_cont_text = "Section 207.003, Property Code, entitles an owner to receive copies of any document that governs the establishment, maintenance, or operation of a subdivision, including, but not limited to, restrictions, bylaws, rules and regulations, and a resale certificate from a property owners' association. A resale certificate contains information including, but not limited to, statements specifying the amount and frequency of regular assessments and the style and cause number of lawsuits to which the property owners' association is a party, other than lawsuits relating to unpaid ad valorem taxes of an individual member of the association. These documents must be made available to you by the property owners' association or the association's agent on your request. If Buyer is concerned about these matters, the TREC promulgated Addendum for Property Subject to Mandatory Membership in a Property Owners Association(s) should be used."
        association_cont_para = Paragraph(association_cont_text, self.normal_style)
        self.story.append(association_cont_para)
        
        # (3) STATUTORY TAX DISTRICTS
        tax_text = "(3) STATUTORY TAX DISTRICTS: If the Property is situated in a utility or other statutorily created district providing water, sewer, drainage, or flood control facilities and services, Chapter 49, Texas Water Code, requires Seller to deliver and Buyer to sign the statutory notice relating to the tax rate, bonded indebtedness, or standby fee of the district prior to final execution of this contract."
        tax_para = Paragraph(tax_text, self.normal_style)
        self.story.append(tax_para)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())

    def add_title_notices_continuation(self):
        # Page 4 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, (Address of Property) Page 4 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Continuation of E. TITLE NOTICES (items 4-12)
        title_notices_cont = [
            "(4) TIDE WATERS: If the Property abuts the tidally influenced waters of the state, §33.135, Texas Natural Resources Code, requires a notice regarding coastal area property to be included in the contract. An addendum containing the notice promulgated by TREC or required by the parties must be used.",
            "(5) ANNEXATION: If the Property is located outside the limits of a municipality, Seller notifies Buyer under §5.011, Texas Property Code, that the Property may now or later be included in the extraterritorial jurisdiction of a municipality and may now or later be subject to annexation by the municipality. Each municipality maintains a map that depicts its boundaries and extraterritorial jurisdiction. To determine if the Property is located within a municipality's extraterritorial jurisdiction or is likely to be located within a municipality's extraterritorial jurisdiction, contact all municipalities located in the general proximity of the Property for further information.",
            "(6) PROPERTY LOCATED IN A CERTIFICATED SERVICE AREA OF A UTILITY SERVICE PROVIDER: Notice required by §13.257, Water Code: The real property, described in Paragraph 2, that you are about to purchase may be located in a certificated water or sewer service area, which is authorized by law to provide water or sewer service to the properties in the certificated area. If your property is located in a certificated area there may be special costs or charges that you will be required to pay before you can receive water or sewer service. There may be a period required to construct lines or other facilities necessary to provide water or sewer service to your property. You are advised to determine if the property is in a certificated area and contact the utility service provider to determine the cost that you will be required to pay and the period, if any, that is required to provide water or sewer service to your property. The undersigned Buyer hereby acknowledges receipt of the foregoing notice at or before the execution of a binding contract for the purchase of the real property described in Paragraph 2 or at closing of purchase of the real property.",
            "(7) PUBLIC IMPROVEMENT DISTRICTS: If the Property is in a public improvement district, Seller must give Buyer written notice as required by §5.014, Property Code. An addendum containing the required notice shall be attached to this contract.",
            "(8) TRANSFER FEES: If the Property is subject to a private transfer fee obligation, §5.205, Property Code, requires Seller to notify Buyer as follows: The private transfer fee obligation may be governed by Chapter 5, Subchapter G of the Texas Property Code.",
            "(9) PROPANE GAS SYSTEM SERVICE AREA: If the Property is located in a propane gas system service area owned by a distribution system retailer, Seller must give Buyer written notice as required by §141.010, Texas Utilities Code. An addendum containing the notice approved by TREC or required by the parties should be used.",
            "(10) NOTICE OF WATER LEVEL FLUCTUATIONS: If the Property adjoins an impoundment of water, including a reservoir or lake, constructed and maintained under Chapter 11, Water Code, that has a storage capacity of at least 5,000 acre-feet at the impoundment's normal operating level, Seller hereby notifies Buyer: 'The water level of the impoundment of water adjoining the Property fluctuates for various reasons, including as a result of: (1) an entity lawfully exercising its right to use the water stored in the impoundment; or (2) drought or flood conditions.'",
            "(11) CERTIFICATE OF MOLD REMEDIATION: If the Property has been remediated for mold, Seller must provide to Buyer each certificate of mold damage remediation issued under §1958.154, Occupations Code, during the 5 years preceding the sale of the Property.",
            "(12) REQUIRED NOTICES: The following notices have been given or are attached to this contract (for example, utility, water, drainage, and public improvement districts):"
        ]
        
        for notice in title_notices_cont:
            notice_para = Paragraph(notice, self.normal_style)
            self.story.append(notice_para)
            self.story.append(Spacer(1, 0.05*inch))
        
        notice_footer = Paragraph("Seller's failure to provide applicable statutory notices may provide Buyer with remedies or rights to terminate the contract.", self.normal_style)
        self.story.append(notice_footer)
        self.story.append(Spacer(1, 0.1*inch))
        
        # 7. PROPERTY CONDITION
        property_condition_section = Paragraph("7. PROPERTY CONDITION:", self.section_style)
        self.story.append(property_condition_section)
        
        # A. ACCESS, INSPECTIONS AND UTILITIES
        access_text = "A. ACCESS, INSPECTIONS AND UTILITIES: Seller shall permit Buyer and Buyer's agents access to the Property at reasonable times. Buyer may have the Property inspected by inspectors selected by Buyer and licensed by TREC or otherwise permitted by law to make inspections. Any hydrostatic testing must be separately authorized by Seller in writing. Seller at Seller's expense shall immediately cause existing utilities to be turned on and shall keep the utilities on during the time this contract is in effect."
        access_para = Paragraph(access_text, self.normal_style)
        self.story.append(access_para)
        
        # B. SELLER'S DISCLOSURE NOTICE
        disclosure_text = "B. SELLER'S DISCLOSURE NOTICE PURSUANT TO §5.008, TEXAS PROPERTY CODE (Notice): (Check one box only)"
        disclosure_para = Paragraph(disclosure_text, self.normal_style)
        self.story.append(disclosure_para)
        
        disclosure_options = [
            ["(1) Buyer has received the Notice.", ""],
            ["(2) Buyer has not received the Notice. Within 7 days after the Effective Date of this contract, Seller shall deliver the Notice to Buyer. If Buyer does not receive the Notice, Buyer may terminate this contract at any time prior to the closing and the earnest money will be refunded to Buyer. If Seller delivers the Notice, Buyer may terminate this contract for any reason within 7 days after Buyer receives the Notice or prior to the closing, whichever first occurs, and the earnest money will be refunded to Buyer.", ""]
        ]
        
        for option in disclosure_options:
            option_para = Paragraph(option[0], self.normal_style)
            self.story.append(option_para)
        
        lead_text = "SELLER'S DISCLOSURE OF LEAD-BASED PAINT AND LEAD-BASED PAINT HAZARDS is required by Federal law for a residential dwelling constructed prior to 1978. Seller is required to furnish the notice under the Texas Property Code"
        lead_para = Paragraph(lead_text, self.normal_style)
        self.story.append(lead_para)
        
        # D. ACCEPTANCE OF PROPERTY CONDITION
        acceptance_text = 'D. ACCEPTANCE OF PROPERTY CONDITION: "As Is" means the present condition of the Property with any and all defects and without warranty except for the warranties of title and the'
        acceptance_para = Paragraph(acceptance_text, self.normal_style)
        self.story.append(acceptance_para)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())



    def add_property_condition_continuation(self):
        # Page 5 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 5 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Continuation of D. ACCEPTANCE OF PROPERTY CONDITION
        acceptance_cont_text = 'warranties in this contract. Buyer\'s agreement to accept the Property As Is under Paragraph 7D(1) or (2) does not preclude Buyer from inspecting the Property under Paragraph 7A, from negotiating repairs or treatments in a subsequent amendment, or from terminating this contract during the Option Period, if any.'
        acceptance_cont_para = Paragraph(acceptance_cont_text, self.normal_style)
        self.story.append(acceptance_cont_para)
        
        # Checkboxes for acceptance options
        acceptance_options = [
            ["(1) Buyer accepts the Property As Is.", ""],
            ["(2) Buyer accepts the Property As Is provided Seller, at Seller's expense, shall complete the following specific repairs and treatments: N/A", ""]
        ]
        
        for option in acceptance_options:
            option_para = Paragraph(option[0], self.normal_style)
            self.story.append(option_para)
        
        note_text = "(Do not insert general phrases, such as 'subject to inspections' that do not identify specific repairs and treatments.)"
        note_para = Paragraph(note_text, self.normal_style)
        self.story.append(note_para)
        
        # E. LENDER REQUIRED REPAIRS AND TREATMENTS
        lender_text = "E. LENDER REQUIRED REPAIRS AND TREATMENTS: Unless otherwise agreed in writing, neither party is obligated to pay for lender required repairs, which includes treatment for wood destroying insects. If the parties do not agree to pay for the lender required repairs or treatments, this contract will terminate and the earnest money will be refunded to Buyer. If the cost of lender required repairs and treatments exceeds 5% of the Sales Price, Buyer may terminate this contract and the earnest money will be refunded to Buyer."
        lender_para = Paragraph(lender_text, self.normal_style)
        self.story.append(lender_para)
        
        # F. COMPLETION OF REPAIRS AND TREATMENTS
        completion_text = "F. COMPLETION OF REPAIRS AND TREATMENTS: Unless otherwise agreed in writing, Seller shall complete all agreed repairs and treatments prior to the Closing Date and obtain any required permits. The repairs and treatments must be performed by persons who are licensed to provide such repairs or treatments or, if no license is required by law, are commercially engaged in the trade of providing such repairs or treatments. Seller shall: (i) provide Buyer with copies of documentation from the repair person(s) showing the scope of work and payment for the work completed; and (ii) at Seller's expense, arrange for the transfer of any transferable warranties with respect to the repairs and treatments to Buyer at closing. If Seller fails to complete any agreed repairs and treatments prior to the Closing Date, Buyer may exercise remedies under Paragraph 15 or extend the Closing Date up to 5 days if necessary for Seller to complete the repairs and treatments."
        completion_para = Paragraph(completion_text, self.normal_style)
        self.story.append(completion_para)
        
        # G. ENVIRONMENTAL MATTERS
        environmental_text = "G. ENVIRONMENTAL MATTERS: Buyer is advised that the presence of wetlands, toxic substances, including asbestos and wastes or other environmental hazards, or the presence of a threatened or endangered species or its habitat may affect Buyer's intended use of the Property. If Buyer is concerned about these matters, an addendum promulgated by TREC or required by the parties should be used."
        environmental_para = Paragraph(environmental_text, self.normal_style)
        self.story.append(environmental_para)
        
        # H. RESIDENTIAL SERVICE CONTRACTS
        service_text = "H. RESIDENTIAL SERVICE CONTRACTS: Buyer may purchase a residential service contract from a provider or administrator licensed by the Texas Department of Licensing and Regulation. If Buyer purchases a residential service contract, Seller shall reimburse Buyer at closing for the cost of the residential service contract in an amount not exceeding $ Buyer should review any residential service contract for the scope of coverage, exclusions and limitations. The purchase of a residential service contract is optional. Similar coverage may be purchased from various companies authorized to do business in Texas."
        service_para = Paragraph(service_text, self.normal_style)
        self.story.append(service_para)
        
        # 8. BROKERS AND SALES AGENTS
        brokers_section = Paragraph("8. BROKERS AND SALES AGENTS:", self.section_style)
        self.story.append(brokers_section)
        
        # A. BROKER OR SALES AGENT DISCLOSURE
        disclosure_text = "A. BROKER OR SALES AGENT DISCLOSURE: Texas law requires a real estate broker or sales agent who is a party to a transaction or acting on behalf of a spouse, parent, child, business entity in which the broker or sales agent owns more than 10%, or a trust for which the broker or sales agent acts as a trustee or of which the broker or sales agent or the broker or sales agent's spouse, parent or child is a beneficiary, to notify the other party in writing before entering into a contract of sale. Disclose if applicable:"
        disclosure_para = Paragraph(disclosure_text, self.normal_style)
        self.story.append(disclosure_para)
        
        # B. BROKERS' FEES
        fees_text = "B. BROKERS' FEES: All obligations of the parties for payment of brokers' fees are contained in separate written agreements."
        fees_para = Paragraph(fees_text, self.normal_style)
        self.story.append(fees_para)
        
        # 9. CLOSING
        closing_section = Paragraph("9. CLOSING:", self.section_style)
        self.story.append(closing_section)
        
        # A. Closing Date
        closing_a_text = "A. The closing of the sale will be on or before 2025 September 15 or within 7 days after objections made under Paragraph 6D have been cured or waived, whichever date is later (Closing Date). If either party fails to close the sale by the Closing Date, the non-defaulting party may exercise the remedies contained in Paragraph 15."
        closing_a_para = Paragraph(closing_a_text, self.normal_style)
        self.story.append(closing_a_para)
        
        # B. At closing
        closing_b_text = "B. At closing:"
        closing_b_para = Paragraph(closing_b_text, self.normal_style)
        self.story.append(closing_b_para)
        
        closing_points = [
            "(1) Seller shall execute and deliver a general warranty deed conveying title to the Property to Buyer and showing no additional exceptions to those permitted in Paragraph 6 and furnish tax statements or certificates showing no delinquent taxes on the Property.",
            "(2) Buyer shall pay the Sales Price in good funds acceptable to the Escrow Agent.",
            "(3) Seller and Buyer shall execute and deliver any notices, statements, certificates, affidavits, releases, loan documents, transfer of any warranties, and other documents reasonably required for the closing of the sale and the issuance of the Title Policy.",
            "(4) There will be no liens, assessments, or security interests against the Property which will not be satisfied out of the sales proceeds unless securing the payment of any loans assumed by Buyer and assumed loans will not be in default.",
            "(5) Private transfer fees (as defined by Chapter 5, Subchapter G of the Texas Property Code)"
        ]
        
        for point in closing_points:
            point_para = Paragraph(point, self.normal_style)
            self.story.append(point_para)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())
    


    def add_closing_continuation(self):
        # Page 6 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 6 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Continuation of Section 9B(5): Private Transfer Fees
        transfer_fees_text = "will be the obligation of Seller unless provided otherwise in this contract. Transfer fees assessed by a property owners' association are governed by the Addendum for Property Subject to Mandatory Membership in a Property Owners Association."
        transfer_fees_para = Paragraph(transfer_fees_text, self.normal_style)
        self.story.append(transfer_fees_para)
        
        # 10. POSSESSION
        possession_section = Paragraph("10. POSSESSION:", self.section_style)
        self.story.append(possession_section)
        
        # A. BUYER'S POSSESSION
        possession_a_text = "A. BUYER'S POSSESSION: Seller shall deliver to Buyer possession of the Property in its present or required condition, ordinary wear and tear excepted: ☑ upon closing and funding according to a temporary residential lease form promulgated by TREC or other written lease required by the parties. Any possession by Buyer prior to closing or by Seller after closing which is not authorized by a written lease will establish a tenancy at sufferance relationship between the parties. Consult your insurance agent prior to change of ownership and possession because insurance coverage may be limited or terminated. The absence of a written lease or appropriate insurance coverage may expose the parties to economic loss."
        possession_a_para = Paragraph(possession_a_text, self.normal_style)
        self.story.append(possession_a_para)
        
        # B. SMART DEVICES
        smart_devices_text = 'B. SMART DEVICES: "Smart Device" means a device that connects to the internet to enable remote use, monitoring, and management of: (i) the Property; (ii) items identified in any Non-Realty Items Addendum; or (iii) items in a Fixture Lease assigned to Buyer. At the time Seller delivers possession of the Property to Buyer, Seller shall:'
        smart_devices_para = Paragraph(smart_devices_text, self.normal_style)
        self.story.append(smart_devices_para)
        
        smart_device_points = [
            "(1) deliver to Buyer written information containing all access codes, usernames, passwords, and applications Buyer will need to access, operate, manage, and control the Smart Devices; and",
            "(2) terminate and remove all access and connections to the improvements and accessories from any of Seller's personal devices including but not limited to phones and computers."
        ]
        
        for point in smart_device_points:
            point_para = Paragraph(point, self.normal_style)
            self.story.append(point_para)
        
        # 11. SPECIAL PROVISIONS
        special_section = Paragraph("11. SPECIAL PROVISIONS:", self.section_style)
        self.story.append(special_section)
        
        special_text = "(This paragraph is intended to be used only for additional informational items. An informational item is a statement that completes a blank in a contract form, discloses factual information, or provides instructions. Real estate brokers and sales agents are prohibited from practicing law and shall not add to, delete, or modify any provision of this contract unless drafted by a party to this contract or a party's attorney.) Buyer may obtain a private loan with no appraisal contingencies"
        special_para = Paragraph(special_text, self.normal_style)
        self.story.append(special_para)
        
        # 12. SETTLEMENT AND OTHER EXPENSES
        settlement_section = Paragraph("12. SETTLEMENT AND OTHER EXPENSES:", self.section_style)
        self.story.append(settlement_section)
        
        # A. The following expenses must be paid at or prior to closing
        settlement_a_text = "A. The following expenses must be paid at or prior to closing:"
        settlement_a_para = Paragraph(settlement_a_text, self.normal_style)
        self.story.append(settlement_a_para)
        
        # (1) Seller shall pay the following expenses (Seller's Expenses)
        seller_expenses_text = "(1) Seller shall pay the following expenses (Seller's Expenses):"
        seller_expenses_para = Paragraph(seller_expenses_text, self.normal_style)
        self.story.append(seller_expenses_para)
        
        seller_points = [
            "(a) releases of existing liens, including prepayment penalties and recording fees; release of Seller's loan liability; tax statements or certificates; preparation of deed; one-half of escrow fee; brokerage fees that Seller has agreed to pay; and other expenses payable by Seller under this contract;",
            "(b) the following amount to be (c) an amount not to exceed $ $ or applied to brokerage fees that Buyer has agreed to pay: % of the Sales Price (check one box only); and to be applied to other Buyer's Expenses."
        ]
        
        for point in seller_points:
            point_para = Paragraph(point, self.normal_style)
            self.story.append(point_para)
        
        # (2) Buyer shall pay the following expenses (Buyer's Expenses)
        buyer_expenses_text = "(2) Buyer shall pay the following expenses (Buyer's Expenses): Appraisal fees; loan application fees; origination charges; credit reports; preparation of loan documents; interest on the notes from date of disbursement to one month prior to dates of first monthly payments; recording fees; copies of easements and restrictions; loan title policy with endorsements required by lender; loan-related inspection fees; photos; amortization schedules; one-half of escrow fee; all prepaid items, including required premiums for flood and hazard insurance, reserve deposits for insurance, ad valorem taxes and special governmental assessments; final compliance inspection; courier fee; repair inspection; underwriting fee; wire transfer fee; expenses incident to any loan; Private Mortgage Insurance Premium (PMI), VA Loan Funding Fee, or FHA Mortgage Insurance Premium (MIP) as required by the lender, brokerage fees that Buyer has agreed to pay; and other expenses payable by Buyer under this contract."
        buyer_expenses_para = Paragraph(buyer_expenses_text, self.normal_style)
        self.story.append(buyer_expenses_para)
        
        # B. If any expense exceeds...
        settlement_b_text = "B. If any expense exceeds an amount expressly stated in this contract for such expense to be paid by a party, that party may terminate this contract unless the other party agrees to pay such excess. Buyer may not pay charges and fees expressly prohibited by FHA, VA, Texas Veterans Land Board or other governmental loan program regulations."
        settlement_b_para = Paragraph(settlement_b_text, self.normal_style)
        self.story.append(settlement_b_para)
        
        # 13. PRORATIONS
        prorations_section = Paragraph("13. PRORATIONS:", self.section_style)
        self.story.append(prorations_section)
        
        prorations_text = "Taxes for the current year, interest, rents, and regular periodic maintenance fees, assessments, and dues (including prepaid items) will be prorated through the Closing Date. The tax proration may be calculated taking into consideration any change in exemptions that will affect the current year's taxes. If taxes for the current year vary from the amount prorated at closing, the parties shall adjust the prorations when tax statements for the current year are available. If taxes are not paid at or prior to closing, Buyer shall pay taxes for the current year."
        prorations_para = Paragraph(prorations_text, self.normal_style)
        self.story.append(prorations_para)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())


    def add_casualty_loss_section(self):
        # Page 7 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 7 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # 14. CASUALTY LOSS
        casualty_section = Paragraph("14. CASUALTY LOSS:", self.section_style)
        self.story.append(casualty_section)
        
        casualty_text = "If any part of the Property is damaged or destroyed by fire or other casualty after the Effective Date of this contract, Seller shall restore the Property to its previous condition as soon as reasonably possible, but in any event by the Closing Date. If Seller fails to do so due to factors beyond Seller's control, Buyer may (a) terminate this contract and the earnest money will be refunded to Buyer (b) extend the time for performance up to 15 days and the Closing Date will be extended as necessary or (c) accept the Property in its damaged condition with an assignment of insurance proceeds, if permitted by Seller's insurance carrier, and receive credit from Seller at closing in the amount of the deductible under the insurance policy. Seller's obligations under this paragraph are independent of any other obligations of Seller under this contract."
        casualty_para = Paragraph(casualty_text, self.normal_style)
        self.story.append(casualty_para)
        
        # 15. DEFAULT
        default_section = Paragraph("15. DEFAULT:", self.section_style)
        self.story.append(default_section)
        
        default_text = "If Buyer fails to comply with this contract, Buyer will be in default, and Seller may (a) enforce specific performance, seek such other relief as may be provided by law, or both, or (b) terminate this contract and receive the earnest money as liquidated damages, thereby releasing both parties from this contract. If Seller fails to comply with this contract, Seller will be in default and Buyer may (a) enforce specific performance, seek such other relief as may be provided by law, or both, or (b) terminate this contract and receive the earnest money, thereby releasing both parties from this contract."
        default_para = Paragraph(default_text, self.normal_style)
        self.story.append(default_para)
        
        # 16. MEDIATION
        mediation_section = Paragraph("16. MEDIATION:", self.section_style)
        self.story.append(mediation_section)
        
        mediation_text = "It is the policy of the State of Texas to encourage resolution of disputes through alternative dispute resolution procedures such as mediation. Any dispute between Seller and Buyer related to this contract which is not resolved through informal discussion will be submitted to a mutually acceptable mediation service or provider. The parties to the mediation shall bear the mediation costs equally. This paragraph does not preclude a party from seeking equitable relief from a court of competent jurisdiction."
        mediation_para = Paragraph(mediation_text, self.normal_style)
        self.story.append(mediation_para)
        
        # 17. ATTORNEY'S FEES
        attorney_section = Paragraph("17. ATTORNEY'S FEES:", self.section_style)
        self.story.append(attorney_section)
        
        attorney_text = "A Buyer, Seller, Listing Broker, Other Broker, or Escrow Agent who prevails in any legal proceeding related to this contract is entitled to recover reasonable attorney's fees and all costs of such proceeding."
        attorney_para = Paragraph(attorney_text, self.normal_style)
        self.story.append(attorney_para)
        
        # 18. ESCROW
        escrow_section = Paragraph("18. ESCROW:", self.section_style)
        self.story.append(escrow_section)
        
        # A. ESCROW
        escrow_a_text = "A. ESCROW: The Escrow Agent is not (i) a party to this contract and does not have liability for the performance or nonperformance of any party to this contract, (ii) liable for interest on the earnest money and (iii) liable for the loss of any earnest money caused by the failure of any financial institution in which the earnest money has been deposited unless the financial institution is acting as Escrow Agent. Escrow Agent may require any disbursement made in connection with this contract to be conditioned on Escrow Agent's collection of good funds acceptable to Escrow Agent."
        escrow_a_para = Paragraph(escrow_a_text, self.normal_style)
        self.story.append(escrow_a_para)
        
        # B. EXPENSES
        escrow_b_text = "B. EXPENSES: At closing, the earnest money must be applied first to any cash down payment, then to Buyer's Expenses and any excess refunded to Buyer. If no closing occurs, Escrow Agent may: (i) require a written release of liability of the Escrow Agent from all parties before releasing any earnest money; and (ii) require payment of unpaid expenses incurred on behalf of a party. Escrow Agent may deduct authorized expenses from the earnest money payable to a party. 'Authorized expenses' means expenses incurred by Escrow Agent on behalf of the party entitled to the earnest money that were authorized by this contract or that party."
        escrow_b_para = Paragraph(escrow_b_text, self.normal_style)
        self.story.append(escrow_b_para)
        
        # C. DEMAND
        escrow_c_text = "C. DEMAND: Upon termination of this contract, either party or the Escrow Agent may send a release of earnest money to each party and the parties shall execute counterparts of the release and deliver same to the Escrow Agent. If either party fails to execute the release, either party may make a written demand to the Escrow Agent for the earnest money. If only one party makes written demand for the earnest money, Escrow Agent shall promptly provide a copy of the demand to the other party. If Escrow Agent does not receive written objection to the demand from the other party within 15 days, Escrow Agent may disburse the earnest money to the party making demand reduced by the amount of unpaid expenses incurred on behalf of the party receiving the earnest money and Escrow Agent may pay the same to the creditors. If Escrow Agent complies with the provisions of this paragraph, each party hereby releases Escrow Agent from all adverse claims related to the disbursal of the earnest money."
        escrow_c_para = Paragraph(escrow_c_text, self.normal_style)
        self.story.append(escrow_c_para)
        
        # D. DAMAGES
        escrow_d_text = "D. DAMAGES: Any party who wrongfully fails or refuses to sign a release acceptable to the Escrow Agent within 7 days of receipt of the request will be liable to the other party for (i) damages; (ii) the earnest money; (iii) reasonable attorney's fees; and (iv) all costs of suit."
        escrow_d_para = Paragraph(escrow_d_text, self.normal_style)
        self.story.append(escrow_d_para)
        
        # E. NOTICES
        escrow_e_text = "E. NOTICES: Escrow Agent's notices will be effective when sent in compliance with Paragraph 21. Notice of objection to the demand will be deemed effective upon receipt by Escrow Agent."
        escrow_e_para = Paragraph(escrow_e_text, self.normal_style)
        self.story.append(escrow_e_para)
        
        # 19. REPRESENTATIONS
        representations_section = Paragraph("19. REPRESENTATIONS:", self.section_style)
        self.story.append(representations_section)
        
        representations_text = "All covenants, representations and warranties in this contract survive closing. If any representation of Seller in this contract is untrue on the Closing Date, Seller will be in default. Unless expressly prohibited by written agreement, Seller may continue to show the Property and receive, negotiate and accept back up offers."
        representations_para = Paragraph(representations_text, self.normal_style)
        self.story.append(representations_para)
        
        # 20. FEDERAL REQUIREMENTS
        federal_section = Paragraph("20. FEDERAL REQUIREMENTS:", self.section_style)
        self.story.append(federal_section)
        
        federal_text = "If Seller is a 'foreign person,' as defined by Internal Revenue Code and its regulations, or if Seller fails to deliver an affidavit or a certificate of non-foreign status to Buyer that Seller is not a 'foreign person,' then Buyer shall withhold from the sales proceeds an amount sufficient to comply with applicable tax law and deliver the same to the Internal Revenue Service together with appropriate tax forms. Internal Revenue Service regulations require filing written reports if currency in excess of specified amounts is received in the transaction."
        federal_para = Paragraph(federal_text, self.normal_style)
        self.story.append(federal_para)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())




    def add_notices_section(self):
        # Page 8 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 8 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # 21. NOTICES
        notices_section = Paragraph("21. NOTICES:", self.section_style)
        self.story.append(notices_section)
        
        notices_text = "All notices from one party to the other must be in writing and are effective when mailed to, hand-delivered at, or transmitted by fax or electronic transmission as follows:"
        notices_para = Paragraph(notices_text, self.normal_style)
        self.story.append(notices_para)
        
        # Create a table for the notice information
        notice_data = [
            ["To Buyer at:", "______", "To Seller at:", "______"],
            ["Phone:", "______", "Phone:", "______"],
            ["E-mail/Fax:", "______", "E-mail/Fax:", "______"],
            ["E-mail/Fax:", "______", "E-mail/Fax:", "______"],
            ["With a copy to Buyer's agent at:", "______", "With a copy to Seller's agent at:", "______"]
        ]
        
        notice_table = Table(notice_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        notice_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        self.story.append(notice_table)
        self.story.append(Spacer(1, 0.1*inch))
        
        # 22. AGREEMENT OF PARTIES
        agreement_section = Paragraph("22. AGREEMENT OF PARTIES:", self.section_style)
        self.story.append(agreement_section)
        
        agreement_text = "This contract contains the entire agreement of the parties and cannot be changed except by their written agreement. Addenda which are a part of this contract are (Check all applicable boxes):"
        agreement_para = Paragraph(agreement_text, self.normal_style)
        self.story.append(agreement_para)
        
        # Create two columns for the addenda checkboxes
        addenda_left = [
            ["☐ Third Party Financing Addendum", ""],
            ["☐ Seller Financing Addendum", ""],
            ["☐ Addendum for Property Subject to Mandatory Membership in a Property Owners Association", ""],
            ["☐ Buyer's Temporary Residential Lease", ""],
            ["☐ Loan Assumption Addendum", ""],
            ["☐ Addendum for Sale of Other Property by Buyer", ""],
            ["☐ Addendum for Reservation of Oil, Gas and Other Minerals", ""],
            ["☐ Addendum for 'Back-Up' Contract", ""],
            ["☐ Addendum for Coastal Area Property", ""],
            ["☐ Addendum for Authorizing Hydrostatic Testing", ""],
            ["☐ Addendum Concerning Right to Terminate Due to Lender's Appraisal", ""],
            ["☐ Environmental Assessment, Threatened or Endangered Species and Wetlands Addendum", ""]
        ]
        
        addenda_right = [
            ["☐ Seller's Temporary Residential Lease", ""],
            ["☐ Short Sale Addendum", ""],
            ["☐ Addendum for Property Located Seaward of the Gulf Intracoastal Waterway", ""],
            ["☐ Addendum for Seller's Disclosure of Information on Lead-based Paint and Lead-based Paint Hazards as Required by Federal Law", ""],
            ["☐ Addendum for Property in a Propane Gas System Service Area", ""],
            ["☐ Addendum Regarding Residential Leases", ""],
            ["☐ Addendum Regarding Fixture Leases", ""],
            ["☐ Addendum containing Notice of Obligation to Pay Improvement District Assessment", ""],
            ["☐ Addendum for Section 1031 Exchange", ""],
            ["☐ Other (list):", "______"],
            ["", "______"],
            ["", "______"]
        ]
        
        # Create tables for both columns
        addenda_left_table = Table(addenda_left, colWidths=[4.5*inch, 0.5*inch])
        addenda_left_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        addenda_right_table = Table(addenda_right, colWidths=[4.5*inch, 0.5*inch])
        addenda_right_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        # Create a two-column layout
        addenda_data = [[addenda_left_table, addenda_right_table]]
        addenda_table = Table(addenda_data, colWidths=[5*inch, 5*inch])
        addenda_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        self.story.append(addenda_table)
        self.story.append(Spacer(1, 0.1*inch))
        
        # 23. CONSULT AN ATTORNEY BEFORE SIGNING
        attorney_section = Paragraph("23. CONSULT AN ATTORNEY BEFORE SIGNING:", self.section_style)
        self.story.append(attorney_section)
        
        attorney_text = "TREC rules prohibit real estate brokers and sales agents from giving legal advice. READ THIS CONTRACT CAREFULLY."
        attorney_para = Paragraph(attorney_text, self.normal_style)
        self.story.append(attorney_para)
        
        # Attorney information table
        attorney_data = [
            ["Buyer's Attorney is:", "______", "Seller's Attorney is:", "______"],
            ["Phone:", "______", "Phone:", "______"],
            ["Fax:", "______", "Fax:", "______"],
            ["E-mail:", "______", "E-mail:", "______"]
        ]
        
        attorney_table = Table(attorney_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        attorney_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        self.story.append(attorney_table)
        
        # Initiated for identification
        initiated_text = "Initialed for identification by Buyer and Seller TREC NO. 20-18"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', 'www.wolf.com')} {self.json_data.get('address', '1208 Creek Knoll')}"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())
        
    def add_page_nine(self):
        # Page 9 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 9 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # EXECUTED section
        executed_text = "EXECUTED the ______ day of ______, 20______ (Effective Date)."
        executed_para = Paragraph(executed_text, self.normal_style)
        self.story.append(executed_para)
        
        note_text = "(BROKER: FILL IN THE DATE OF FINAL ACCEPTANCE.)"
        note_para = Paragraph(note_text, self.normal_style)
        self.story.append(note_para)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Buyer and Seller signature blocks
        buyer_data = [
            ["Buyer:", "8/25/2025"],
            ["", "Silverkey Investments LLC or Designated entity"],
            ["Buyer", ""]
        ]
        
        seller_data = [
            ["Seller:", "SECRETARY OF VETERANS AFFAIRSV"],
            ["Seller", ""]
        ]
        
        # Create a table with two columns for buyer and seller
        signature_data = [
            [Table(buyer_data, colWidths=[1.5*inch, 3*inch]), 
            Table(seller_data, colWidths=[1.5*inch, 3*inch])]
        ]
        
        signature_table = Table(signature_data, colWidths=[4.5*inch, 4.5*inch])
        signature_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # No grid lines
        ]))
        
        self.story.append(signature_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # TREC notice
        trec_text = "The form of this contract has been approved by the Texas Real Estate Commission. TREC forms are intended for use only by trained real estate license holders. No representation is made as to the legal validity or adequacy of any provision in any specific transactions. It is not intended for complex transactions. Texas Real Estate Commission, P.O. Box 12188, Austin, TX 78711-2188, (512) 936-3000 (TREC NO. 20-18). This form replaces TREC NO. 20-17."
        trec_para = Paragraph(trec_text, self.footer_style)
        self.story.append(trec_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', '')} {self.json_data.get('address', '1208 Creek Knoll')} Joel Villanueva"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())

    def add_page_ten(self):
        # Page 10 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 10 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # BROKER INFORMATION section
        broker_header = Paragraph("BROKER INFORMATION<br/>(Print name(s) only. Do not sign)", self.section_style)
        self.story.append(broker_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Broker information table
        broker_data = [
            ["Loaded Realty Company", "9015900", "Poly Properties", ""],
            ["Other Broker Firm", "License No.", "Listing Broker Firm", "License No."],
            ["represents", "☑ Buyer only as Buyer's agent", "represents", "☐ Seller and Buyer as an intermediary"],
            ["", "☐ Seller as Listing Broker's subagent", "", "☐ Seller only as Seller's agent"],
            ["Joel Villanueva", "817205", "Harold Johnson", "0510611"],
            ["Associate's Name", "License No.", "Listing Associate's Name", "License No."],
            ["Loaded Realty Group", "", "Poly Properties", ""],
            ["Team Name", "", "Team Name", ""],
            ["villanuevajoele@gmail.com", "(210)740-5663", "realestate@liberated.net", "(210)473-5578"],
            ["Associate's Email Address", "Phone", "Listing Associate's Email Address", "Phone"],
            ["Carlos Puckerin", "0759746", "Licensed Supervisor of Listing Associate", ""],
            ["Licensed Supervisor of Associate", "License No.", "", "License No."],
            ["825 Town & Country Lane", "(832)856-9022", "8238 Morning Grove", "(210)473-5578"],
            ["Other Broker's Address", "Phone", "Listing Broker's Office Address", "Phone"],
            ["Houston", "TX", "77056", "Converse", "TX", "78109"],
            ["City", "State", "Zip", "City", "State", "Zip"],
            ["", "", "Selling Associate's Name", "License No."],
            ["", "", "Team Name", ""],
            ["", "", "Selling Associate's Email Address", "Phone"],
            ["", "", "Licensed Supervisor of Selling Associate", "License No."],
            ["", "", "Selling Associate's Office Address", ""],
            ["", "", "City", "State", "Zip"]
        ]
        
        # Create the broker table
        broker_table = Table(broker_data, colWidths=[1.5*inch, 1.2*inch, 1.8*inch, 1.2*inch])
        broker_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('SPAN', (0, 0), (0, 0)),  # Span first row
            ('SPAN', (2, 0), (3, 0)),  # Span first row
            ('SPAN', (0, 4), (0, 4)),  # Span Joel Villanueva row
            ('SPAN', (2, 4), (2, 4)),  # Span Harold Johnson row
            ('SPAN', (0, 6), (0, 6)),  # Span Team Name row
            ('SPAN', (2, 6), (3, 6)),  # Span Team Name row
            ('SPAN', (0, 8), (0, 8)),  # Span Email row
            ('SPAN', (2, 8), (2, 8)),  # Span Email row
            ('SPAN', (0, 10), (0, 10)),  # Span Supervisor row
            ('SPAN', (2, 10), (2, 10)),  # Span Supervisor row
            ('SPAN', (0, 12), (0, 12)),  # Span Address row
            ('SPAN', (2, 12), (2, 12)),  # Span Address row
            ('SPAN', (0, 14), (2, 14)),  # Span City/State/Zip row
            ('SPAN', (3, 14), (5, 14)),  # Span City/State/Zip row
        ]))
        
        self.story.append(broker_table)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Disclosure paragraph
        disclosure_text = "Disclosure: Pursuant to a previous, separate agreement, Listing Broker has agreed to pay Other Broker a fee $ or ☒ 3.000% of the Sales Price). This disclosure is for informational purposes and does not change the previous agreement between brokers to pay or share a commission."
        disclosure_para = Paragraph(disclosure_text, self.normal_style)
        self.story.append(disclosure_para)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', '')} {self.json_data.get('address', '1208 Creek Knoll')} Joel Villanueva"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        # Add TREC number at the bottom
        trec_num = Paragraph("TREC NO. 20-18", self.small_style)
        self.story.append(trec_num)

    def add_page_eleven(self):
        # Page 11 header
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        page_header = Paragraph(f"Contract Concerning {address}, San Antonio, Page 11 of 11 {contract_date}", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # OPTION FEE RECEIPT
        option_fee_header = Paragraph("OPTION FEE RECEIPT", self.section_style)
        self.story.append(option_fee_header)
        
        option_fee_text = "Receipt of $ ______ (Option Fee) in the form of ______ is acknowledged."
        option_fee_para = Paragraph(option_fee_text, self.normal_style)
        self.story.append(option_fee_para)
        
        option_fee_data = [
            ["______", "______", "______", "______"],
            ["Escrow Agent", "Buyer's Choice", "", "Date"]
        ]
        
        option_fee_table = Table(option_fee_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        option_fee_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ]))
        
        self.story.append(option_fee_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # EARNEST MONEY RECEIPT
        earnest_header = Paragraph("EARNEST MONEY RECEIPT", self.section_style)
        self.story.append(earnest_header)
        
        earnest_text = "Receipt of $ ______ Earnest Money in the form of ______ is acknowledged."
        earnest_para = Paragraph(earnest_text, self.normal_style)
        self.story.append(earnest_para)
        
        earnest_data = [
            ["______", "______", "______", "______"],
            ["Escrow Agent", "Received by", "Email Address", "Date/Time"],
            ["______", "______", "______", "______"],
            ["Address", "Phone", "", ""],
            ["______", "______", "______", "______"],
            ["City", "State", "Zip", "Fax"]
        ]
        
        earnest_table = Table(earnest_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        earnest_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
            ('SPAN', (2, 2), (3, 2)),  # Span the blank line
            ('SPAN', (2, 3), (3, 3)),  # Span the Address/Phone row
            ('SPAN', (2, 4), (3, 4)),  # Span the City/State/Zip row
        ]))
        
        self.story.append(earnest_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # CONTRACT RECEIPT
        contract_header = Paragraph("CONTRACT RECEIPT", self.section_style)
        self.story.append(contract_header)
        
        contract_text = "Receipt of the Contract is acknowledged."
        contract_para = Paragraph(contract_text, self.normal_style)
        self.story.append(contract_para)
        
        contract_data = [
            ["______", "______", "______", "______"],
            ["Escrow Agent", "Received by", "Email Address", "Date"],
            ["______", "______", "______", "______"],
            ["Address", "Phone", "", ""],
            ["______", "______", "______", "______"],
            ["City", "State", "Zip", "Fax"]
        ]
        
        contract_table = Table(contract_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        contract_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
            ('SPAN', (2, 2), (3, 2)),  # Span the blank line
            ('SPAN', (2, 3), (3, 3)),  # Span the Address/Phone row
            ('SPAN', (2, 4), (3, 4)),  # Span the City/State/Zip row
        ]))
        
        self.story.append(contract_table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # ADDITIONAL EARNEST MONEY RECEIPT
        additional_header = Paragraph("ADDITIONAL EARNEST MONEY RECEIPT", self.section_style)
        self.story.append(additional_header)
        
        additional_text = "Receipt of $ ______ additional Earnest Money in the form of ______ is acknowledged."
        additional_para = Paragraph(additional_text, self.normal_style)
        self.story.append(additional_para)
        
        additional_data = [
            ["______", "______", "______", "______"],
            ["Escrow Agent", "Received by", "Email Address", "Date/Time"],
            ["______", "______", "______", "______"],
            ["Address", "Phone", "", ""],
            ["______", "______", "______", "______"],
            ["City", "State", "Zip", "Fax"]
        ]
        
        additional_table = Table(additional_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        additional_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
            ('SPAN', (2, 2), (3, 2)),  # Span the blank line
            ('SPAN', (2, 3), (3, 3)),  # Span the Address/Phone row
            ('SPAN', (2, 4), (3, 4)),  # Span the City/State/Zip row
        ]))
        
        self.story.append(additional_table)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', '')} {self.json_data.get('address', '1208 Creek Knoll')} Joel Villanueva"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        # Add TREC number at the bottom
        trec_num = Paragraph("TREC NO. 20-18", self.small_style)
        self.story.append(trec_num)
        
        self.story.append(PageBreak())

    def add_page_twelve(self):
        # Page 12 header (Third Party Financing Addendum - Page 1)
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = self.json_data.get('contract_date', datetime.now().strftime("%m-%d-%Y"))
        
        # Addendum header
        addendum_header = Paragraph("PROMULGATED BY THE TEXAS REAL ESTATE COMMISSION (TREC)", self.section_style)
        self.story.append(addendum_header)
        
        addendum_title = Paragraph("THIRD PARTY FINANCING ADDENDUM", self.section_style)
        self.story.append(addendum_title)
        
        to_contract = Paragraph("TO CONTRACT CONCERNING THE PROPERTY AT", self.normal_style)
        self.story.append(to_contract)
        
        property_address = Paragraph(f"{address} San Antonio", self.normal_style)
        self.story.append(property_address)
        
        street_city = Paragraph("(Street Address and City)", self.normal_style)
        self.story.append(street_city)
        
        date_para = Paragraph(contract_date, self.normal_style)
        self.story.append(date_para)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Section 1: TYPE OF FINANCING AND DUTY TO APPLY AND OBTAIN APPROVAL
        section1_header = Paragraph("1. TYPE OF FINANCING AND DUTY TO APPLY AND OBTAIN APPROVAL: Buyer shall apply promptly for all financing described below and make every reasonable effort to obtain approval for the financing, including but not limited to furnishing all information and documents required by Buyer's lender. (Check applicable boxes):", self.normal_style)
        self.story.append(section1_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # A. CONVENTIONAL FINANCING
        conventional_header = Paragraph("A. CONVENTIONAL FINANCING:", self.normal_style)
        self.story.append(conventional_header)
        
        conventional_text = "☐ (1) A first mortgage loan in the principal amount of $ ______ (excluding any financed PMI premium), due in full in ______ year(s), with interest not to exceed ______% per annum for the first ______ year(s) of the loan with Origination Charges as shown on Buyer's Loan Estimate for the loan not to exceed ______% of the loan."
        conventional_para = Paragraph(conventional_text, self.normal_style)
        self.story.append(conventional_para)
        
        conventional_text2 = "☐ (2) A second mortgage loan in the principal amount of $ ______ (excluding any financed PMI premium), due in full in ______ year(s), with interest not to exceed ______% per annum for the first ______ year(s) of the loan with Origination Charges as shown on Buyer's Loan Estimate for the loan not to exceed ______% of the loan."
        conventional_para2 = Paragraph(conventional_text2, self.normal_style)
        self.story.append(conventional_para2)
        self.story.append(Spacer(1, 0.1*inch))
        
        # B. TEXAS VETERANS LOAN
        veterans_header = Paragraph("B. TEXAS VETERANS LOAN: A loan(s) from the Texas Veterans Land Board of $ ______ for a period in the total amount of ______ years at the interest rate established by the Texas Veterans Land Board.", self.normal_style)
        self.story.append(veterans_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # C. FHA INSURED FINANCING
        fha_header = Paragraph("C. FHA INSURED FINANCING: A Section ______ FHA insured loan of not less than $ ______ (excluding any financed MIP), amortizable monthly for not less than ______ years, with interest not to exceed ______% per annum for the first ______ year(s) of the loan with Origination Charges as shown on Buyer's Loan Estimate for the loan not to exceed ______% of the loan.", self.normal_style)
        self.story.append(fha_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # D. VA GUARANTEED FINANCING
        va_header = Paragraph("D. VA GUARANTEED FINANCING: A VA guaranteed loan of not less than $ ______ (excluding any financed Funding Fee), amortizable monthly for not less than ______ years, with interest not to exceed ______% per annum for the first ______ year(s) of the loan with Origination Charges as shown on Buyer's Loan Estimate for the loan not to exceed ______% of the loan.", self.normal_style)
        self.story.append(va_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # E. USDA GUARANTEED FINANCING
        usda_header = Paragraph("E. USDA GUARANTEED FINANCING: A USDA-guaranteed loan of not less than $ ______ (excluding any financed Funding Fee), amortizable monthly for not less than ______ years, with interest not to exceed ______% per annum for the first ______ year(s) of the loan with Origination Charges as shown on Buyer's Loan Estimate for the loan not to exceed ______% of the loan.", self.normal_style)
        self.story.append(usda_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # F. REVERSE MORTGAGE FINANCING
        reverse_header = Paragraph("F. REVERSE MORTGAGE FINANCING: A reverse mortgage loan (also known as a Home Equity Conversion Mortgage loan) in the original principal amount of $ ______ (excluding any financed PMI premium or other costs), with interest not to exceed ______% per annum for the first ______ year(s) of the loan with Origination Charges as shown on Buyer's Loan Estimate for the loan not to exceed ______% of the loan. The reverse mortgage loan will not be an FHA insured loan.", self.normal_style)
        self.story.append(reverse_header)
        self.story.append(Spacer(1, 0.1*inch))
        
        # G. OTHER FINANCING
        other_header = Paragraph("G. OTHER FINANCING: A loan not of a type described above from Futures Funding Inc (name of lender) in the principal amount of $135,000.00 due in ______ year(s), with interest not to exceed 14.000% per annum for the first ______ year(s) of the loan with Origination Charges not to exceed 6.000% of the loan. Buyer ☑ does ☐ does not waive all rights to terminate the contract under Paragraph 2B of this addendum for the loan described in this paragraph.", self.normal_style)
        self.story.append(other_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Section 2: APPROVAL OF FINANCING
        section2_header = Paragraph("2. APPROVAL OF FINANCING: Approval for the financing described above will be deemed to have been obtained when Buyer Approval and Property Approval are obtained. Time is of the essence for this paragraph and strict compliance with the time for performance is required.", self.normal_style)
        self.story.append(section2_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Initialed for identification
        initiated_text = "Initialed for identification by Buyer ______ and Seller ______ TREC NO. 40-11"
        initiated_para = Paragraph(initiated_text, self.small_style)
        self.story.append(initiated_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', '')} {self.json_data.get('address', '1208 Creek Knoll')} Joel Villanueva"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        self.story.append(PageBreak())

    def add_page_thirteen(self):
        # Page 13 header (Third Party Financing Addendum - Page 2)
        address = self.json_data.get('address', '1208 CREEK KNL TX 78253').split(',')[0]
        contract_date = "11-04-12024"  # Specific date from the example
        
        addendum_header = Paragraph(f"Third Party Financing Addendum Concerning {address}, San Antonio, (Address of Property)", self.small_style)
        self.story.append(addendum_header)
        
        page_header = Paragraph(f"{contract_date} Page 2 of 2", self.small_style)
        self.story.append(page_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # A. BUYER APPROVAL
        buyer_approval_header = Paragraph("A. BUYER APPROVAL (Check one box only):", self.normal_style)
        self.story.append(buyer_approval_header)
        
        buyer_approval_text = "☐ This contract is subject to Buyer obtaining Buyer Approval. If Buyer cannot obtain Buyer Approval, Buyer may terminate this contract within 15 days after the Effective Date of the contract by giving Seller: (i) notice of termination; and (ii) a copy of a written statement from the lender setting forth the reason(s) for lender's determination. If Buyer terminates the contract under this provision, this contract will terminate and the earnest money will be refunded to Buyer. If Buyer does not terminate the contract under Paragraph 2A, the contract shall no longer be subject to the Buyer obtaining Buyer Approval. Buyer Approval will be deemed to have been obtained when (i) the terms of the loan(s) described above are available and (ii) lender determines that Buyer has satisfied all of lender's requirements related to Buyer's assets, income and credit history."
        buyer_approval_para = Paragraph(buyer_approval_text, self.normal_style)
        self.story.append(buyer_approval_para)
        
        buyer_approval_text2 = "☐ This contract is not subject to Buyer obtaining Buyer Approval."
        buyer_approval_para2 = Paragraph(buyer_approval_text2, self.normal_style)
        self.story.append(buyer_approval_para2)
        self.story.append(Spacer(1, 0.2*inch))
        
        # B. PROPERTY APPROVAL
        property_approval_header = Paragraph("B. PROPERTY APPROVAL: If Buyer's lender determines that the Property does not satisfy lender's underwriting requirements for the loan (including but not limited to appraisal, insurability, and lender required repairs) Buyer may terminate this contract on or before the 3rd day before the Closing Date by giving Seller: (i) notice of termination; and (ii) a copy of a written statement from the lender setting forth the reason(s) for lender's determination. If Buyer terminates under this paragraph, the earnest money will be refunded to Buyer. If Buyer does not terminate under this paragraph, Property Approval is deemed to have been obtained.", self.normal_style)
        self.story.append(property_approval_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # 3. SECURITY
        security_header = Paragraph("3. SECURITY: If required by Buyer's lender, each note for the financing described above must be secured by vendor's and deed of trust liens.", self.normal_style)
        self.story.append(security_header)
        self.story.append(Spacer(1, 0.2*inch))
        
        # 4. FHA/VA REQUIRED PROVISION
        fha_va_header = Paragraph("4. FHA/VA REQUIRED PROVISION: If the financing described above involves FHA insured or VA financing, it is expressly agreed that, notwithstanding any other provision of this contract, the purchaser (Buyer) shall not be obligated to complete the purchase of the Property described herein or to incur any penalty by forfeiture of earnest money deposits or otherwise: (i) unless the Buyer has been given in accordance with HUD/FHA or VA requirements a written statement issued by the Federal Housing Commissioner, Department of Veterans Affairs, or a Direct Endorsement Lender setting forth the appraised value of the Property of not less than $ ______ or (ii) if the contract purchase price or cost exceeds the reasonable value of the Property established by the Department of Veterans Affairs. The 3-day notice of termination requirement in Paragraph 2B does not apply to this Paragraph 4.", self.normal_style)
        self.story.append(fha_va_header)
        
        # A, B, C subsections
        subsection_a = Paragraph("A. The Buyer shall have the privilege and option of proceeding with consummation of the contract without regard to the amount of the appraised valuation or the reasonable value established by the Department of Veterans Affairs.", self.normal_style)
        self.story.append(subsection_a)
        
        subsection_b = Paragraph("B. If FHA financing is involved, the appraised valuation is arrived at to determine the maximum mortgage the Department of Housing and Urban Development will insure. HUD does not warrant the value or the condition of the Property. The Buyer should satisfy himself/herself that the price and the condition of the Property are acceptable.", self.normal_style)
        self.story.append(subsection_b)
        
        subsection_c = Paragraph("C. If VA financing is involved and if Buyer elects to complete the purchase at an amount in excess of the reasonable value established by the VA, Buyer shall pay such excess amount in cash from a source which Buyer agrees to disclose to the VA and which Buyer represents will not be from borrowed funds except as approved by VA. If VA reasonable value of the Property is less than the Sales Prices, Seller may reduce the Sales Price to an amount equal to the VA reasonable value and the sale will be closed at the lower Sales Price with proportionate adjustments to the down payment and the loan amount.", self.normal_style)
        self.story.append(subsection_c)
        self.story.append(Spacer(1, 0.2*inch))
        
        # 5. AUTHORIZATION TO RELEASE INFORMATION
        auth_header = Paragraph("5. AUTHORIZATION TO RELEASE INFORMATION:", self.normal_style)
        self.story.append(auth_header)
        
        auth_a = Paragraph("A. Buyer authorizes Buyer's lender to furnish to Seller or Buyer or their representatives information relating to the status of the approval for the financing.", self.normal_style)
        self.story.append(auth_a)
        
        auth_b = Paragraph("B. Seller and Buyer authorize Buyer's lender, title company, and Escrow Agent to disclose and furnish a copy of the closing disclosures and settlement statements to the parties' respective brokers and sales agents provided under Broker Information.", self.normal_style)
        self.story.append(auth_b)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Signature section
        date_para = Paragraph("8/25/2025", self.normal_style)
        self.story.append(date_para)
        
        buyer_data = [
            ["Buyer:", "Silverkey investments LLC or Designated entity"],
            ["Buyer", ""]
        ]
        
        seller_data = [
            ["Seller:", "SECRETARY OF VETERANS AFFAIRSV"],
            ["Seller", ""]
        ]
        
        # Create a table with two columns for buyer and seller
        signature_data = [
            [Table(buyer_data, colWidths=[1.5*inch, 3*inch]), 
            Table(seller_data, colWidths=[1.5*inch, 3*inch])]
        ]
        
        signature_table = Table(signature_data, colWidths=[4.5*inch, 4.5*inch])
        signature_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), self.primary_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ]))
        
        self.story.append(signature_table)
        self.story.append(Spacer(1, 0.2*inch))
        
        # TREC notice
        trec_text = "This form has been approved by the Texas Real Estate Commission for use with similarly approved or promulgated contract forms. Such approval relates to this form only. TREC forms are intended for use only by trained real estate license holders. No representation is made as to the legal validity or adequacy of any provision in any specific transactions. It is not intended for complex transactions. Texas Real Estate Commission, P.O. Box 12188, Austin, TX 78711-2188, (512) 936-3000 TREC No. 40-11. This form replaces TREC No. 40-10."
        trec_para = Paragraph(trec_text, self.footer_style)
        self.story.append(trec_para)
        
        # Add footer information
        broker_info = self.json_data.get('broker_info', {})
        footer_text = f"{broker_info.get('office_name', 'Loaded Realty Company')}, {broker_info.get('street_address', '825 Town & Country Ln Houston TX 77024')} Phone: {broker_info.get('phone', '2107405653')} Fax: {broker_info.get('fax', '')} {self.json_data.get('address', '1208 Creek Knoll')} Joel Villanueva"
        footer_para = Paragraph(footer_text, self.footer_style)
        self.story.append(footer_para)
        
        # Add TREC number at the bottom
        trec_num = Paragraph("TREC NO. 40-11", self.small_style)
        self.story.append(trec_num)

    # Update the generate_pdf method to include the new pages
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
        self.add_title_policy_section()
        self.add_survey_section()
        self.add_title_notices_continuation()
        self.add_property_condition_continuation()
        self.add_closing_continuation()
        self.add_casualty_loss_section()
        self.add_notices_section()
        self.add_page_nine()
        self.add_page_ten()
        self.add_page_eleven()  # Add page 11
        self.add_page_twelve()  # Add page 12
        self.add_page_thirteen()  # Add page 13
        
        # Build the PDF with header and footer
        doc.build(self.story, onFirstPage=self.create_header_footer, 
                onLaterPages=self.create_header_footer)
        
        return output_path

# Example usage:
if __name__ == "__main__":
    # Sample data structure that matches the image
    sample_data = {
        "docusign_id": "AA36957E-5678-43F3-B524-A4E6F6685470",
        "contract_date": "11-04-2024",
        "seller": "SECRETARY OF VETERANS AFFAIRS",
        "buyer": "Silverkey investments LLC or Designated entity",
        "Lot": "36",
        "Block": "1",
        "Subdivision_Legal_Name": "HEIGHTS OF WESTCREEK PH 1",
        "contry": "Bexar",
        "address": "1208 CREEK KNL TX 78253",
        "admin_data": {
            "sales_price": "135,000.00"
        },
        "broker_info": {
            "office_name": "Loaded Realty Company",
            "street_address": "825 Town & Country Ln Houston TX 77024",
            "phone": "2107405653",
            "fax": "www.wolf.com"
        }
    }
    
    # Generate PDF
    generator = RealEstateContractGenerator(sample_data)
    generator.generate_pdf("real_estate_contract_page1-13.pdf")
    # generator.add_earnest_money_section("real_estate_contract_page2.pdf")