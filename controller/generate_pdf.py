from flask import request, jsonify, render_template
import base64
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
import uuid
from app import app
from model.DataBase_model import get_all_json , get_filtered_properties




import json
import os

from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.pdfgen import canvas


from playwright.sync_api import sync_playwright
import os


def img_to_base64(path):
    with open(path, "rb") as img_file:
        return "data:image/png;base64," + base64.b64encode(img_file.read()).decode()

main_logo_b64 = img_to_base64(r"D:\Outfield\Automation_sabor_connectmls\static\images\main_logo.png")
small_logo_b64 = img_to_base64(r"D:\Outfield\Automation_sabor_connectmls\static\images\small_logo.png")



# If you want to add a real logo, use this version
def RealEstateContractGenerator(property_data):
    main_logo_path = r"D:\Outfield\\Automation_sabor_connectmls\\static\\images\\main_logo.png"
    small_logo_path = r"D:\Outfield\\Automation_sabor_connectmls\\static\\images\\small_logo.png"
    # HTML content with logo placeholder
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Texas Real Estate Contract</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
                font-size: 11px;
                line-height: 1.2;
            }}

            body {{
                padding: 8px;
                color: #333;
                max-width: 8.5in;
                margin: 0 auto;
                background-color: #f9f9f9;
            }}

            .container {{
                background: white;
                padding: 15px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border: 2px solid black;
            }}

            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 5px;
                padding-bottom: 5px;
                border-bottom: 1px solid #1E5B94;
            }}

            .big_logo {{
                height: auto;
                width: 120px;
            }}

            .small_logo {{
                height: auto;
                width: 80px;
            }}

            .main-title_1 {{
                text-align: center;
                color: black;
                margin: 0;
                font-size: 9px;
            }}

            .main-title_2 {{
                text-align: center;
                color: black;
                margin: 0;
                font-size: 11px;
                font-weight: bold;
            }}

            .section {{
                margin: 8px 0;
            }}

            .user_input {{
                color: #1976D2;
                font-weight: bold;
            }}

            .subsection {{
                margin: 4px 10px;
                display: flex;
            }}

            .sub_subsection {{
                margin-left: 5px;
            }}

            .text-input {{
                border-bottom: 1px solid #999;
                display: inline-block;
                min-width: 150px;
                padding: 0 3px;
            }}


            /* Container and overall */
            .notices-container {{
                font-family: Arial, Helvetica, sans-serif;
                max-width: 1000px;
                margin: 24px auto;
                padding: 20px;
                box-sizing: border-box;
            }}

            /* Title and description */
            .section-title {{
                font-weight: 700;
                font-size: 18px;
                margin-bottom: 8px;
            }}

            .section-desc {{
                margin: 0 0 16px 0;
                line-height: 1.3;
                color: #222;
            }}

            /* 2-column layout */
            .notice-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 28px;
                align-items: start;
            }}

            /* Column card (visually not boxed, but useful for spacing) */
            .notice-col {{
                min-width: 0;
            }}

            /* Header of each column (To Buyer at:, To Seller at:) */
            .col-header {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 8px;
                font-weight: 600;
            }}

            /* Label above line */
            .field-label {{
                display: block;
                margin-bottom: 6px;
                font-size: 13px;
                color: #111;
            }}

            /* Horizontal line used to emulate blank signature/line area */
            .line {{
                border-bottom: 1px solid #000;
                height: 20px;
                /* controls vertical spacing / "line height" */
                margin-bottom: 12px;
            }}

            /* smaller single-line entry (like Phone:) */
            .small-line {{
                width: 70%;
                border-bottom: 1px solid #000;
                height: 18px;
                display: inline-block;
                vertical-align: middle;
                margin-left: 8px;
            }}

            /* stacked rows inside a column */
            .field-row {{
                margin-bottom: 10px;
            }}

            /* "With a copy to ..." text (slightly smaller) */
            .copy-note {{
                margin-top: 8px;
                font-size: 13px;
                font-weight: 600;
            }}

            /* Agent sub-block (label + line) */
            .agent-block {{
                margin-top: 6px;
            }}

            /* small print spacing to mimic the image layout */
            .two-lines {{
                margin-bottom: 6px;
            }}

            /* responsive fallback: stack columns on narrow screens */
            @media (max-width: 640px) {{
                .notice-grid {{
                    grid-template-columns: 1fr;
                }}
            }}







            /* Executed box */
            .executed-box {{
                border: 2px solid #000;
                padding: 10px;
                margin-top: 40px;
                font-weight: 600;
                font-size: 14px;
                line-height: 1.4;
            }}

            /* inline blank lines */
            .small-inline {{
                width: 40px;
                display: inline-block;
            }}

            .large-inline {{
                width: 160px;
                display: inline-block;
            }}

            /* signature area */
            .signature-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 60px;
                margin-top: 40px;
                font-size: 14px;
            }}

            .signature-col {{
                text-align: left;
            }}

            .signed-by {{
                display: flex;
                align-items: center;
                gap: 6px;
                margin-bottom: 6px;
            }}

            .sig-label {{
                font-size: 12px;
                font-weight: 500;
            }}

            .sig-line {{
                flex: 1;
            }}

            .party-name {{
                font-weight: 600;
                margin: 4px 0;
            }}

            .sig-date {{
                margin: 4px 0 12px 0;
                font-size: 13px;
            }}

            .party-line {{
                border-bottom: 1px solid #000;
                height: 18px;
                margin: 12px 0 4px 0;
            }}

            .role {{
                font-size: 13px;
                font-weight: 500;
                text-align: center;
            }}

            .total-center {{
                text-align: center;
            }}



            .col-header {{
                display: flex;
                justify-content: space-between;
                /* pushes spans apart */
                align-items: center;
                /* vertically centers them */
            }}




        h3 {{
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 10px;
        }}

        .line {{
        margin: 10px 0;
        }}

        .line input {{
        border: none;
        border-bottom: 1px solid #000;
        width: 250px;
        padding: 2px;
        }}

        .row {{
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
        }}

        .row div {{
        flex: 1;
        margin: 0 5px;
        }}

        label {{
        display: block;
        font-size: 14px;
        margin-bottom: 2px;
        }}

        .address {{
        margin-top: 8px;
        }}

        .address input {{
        width: 100%;
        border: none;
        border-bottom: 1px solid #000;
        padding: 2px;
        }}
        </style>
    </head>

    <body>
        <div style="font-size: 10px;">
            Docusign Envelope ID: AA36957E-5678-43F3-B524-A4E6F66854708888888
        </div>
        <div class="container">
            <p style="text-align: end; margin-bottom: 5px;">11-04-2024</p>
            <div class="header">
                <img class="big_logo" src="{main_logo_b64}" alt="TREC Logo">
                <div>
                    <div class="main-title_1">
                        PROMULGATED BY THE TEXAS REAL ESTATE COMMISSION (TREC)
                    </div>
                    <div class="main-title_2">
                        ONE TO FOUR FAMILY RESIDENTIAL CONTRACT (RESALE)
                    </div>
                    <div class="main-title_1">
                        NOTICE: Not For Use For Condominium Transactions
                    </div>
                </div>
                <img class="big_logo" src="{small_logo_b64}" alt="TREC Logo">
            </div>

            <div class="section">
                <p><strong>1. PARTIES:</strong> The parties to this contract are <span
                        class="text-input user_input">SECRETARY OF VETERANS AFFAIRS</span> (Seller)
                    and <span class="text-input user_input">Silverkey investments LLC or Designated entity</span> (Buyer).
                    Seller agrees to sell and convey to Buyer and Buyer agrees to buy from Seller the Property defined
                    below.</p>
            </div>

            <div class="section">
                <p><strong>2. PROPERTY:</strong> The land, improvements and accessories are collectively referred to as the
                    Property.</p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        LAND: Lot <span class="text-input user_input">{property_data["Lot"]}</span>, Block <span
                            class="text-input user_input">{property_data["Block"]}</span><br>
                        <span class="text-input user_input">{property_data["Subdivision_Legal_Name"]}</span> Addition, City of <span
                            class="text-input user_input">{property_data["admin_data"]["state"]}</span><br>
                        County of <span class="text-input user_input">{property_data["contry"]}</span>, Texas, known as <span
                            class="text-input user_input">{property_data["address"]}</span>
                        (address/zip code), or as described on attached exhibit.
                    </div>
                </div>
                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        IMPROVEMENTS: The house, garage and all other fixtures and improvements attached to the
                        above-described real property, including without limitation, the following <strong> permanently
                            installed and built-in items</strong>, if any: all equipment and appliances, valances, screens,
                        shutters, awnings, wall-to-wall carpeting, mirrors, ceiling fans, attic fans, mail boxes, television
                        antennas, mounts and brackets for televisions and speakers, heating and air-conditioning units,
                        security and fire detection equipment, wiring, plumbing and lighting fixtures, chandeliers, water
                        softener system, kitchen equipment, garage door openers, cleaning equipment, shrubbery, landscaping,
                        outdoor cooking equipment, and all other property attached to the above described real property.
                    </div>
                </div>
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        ACCESSORIES: The following described related accessories, if any: window air conditioning units,
                        stove, fireplace screens, curtains and rods, blinds, window shades, draperies and rods, door keys,
                        mailbox keys, above ground pool, swimming pool equipment and maintenance accessories, artificial
                        fireplace logs, security systems that are not fixtures, and controls for: (i) garage doors, (ii)
                        entry gates, and (iii) other improvements and accessories. "Controls" includes Seller's transferable
                        rights to the (i) software and applications used to access and control improvements or accessories,
                        and (ii) hardware used solely to control improvements or accessories.
                    </div>
                </div>
                <div class="subsection">
                    <span>D.</span>
                    <div class="sub_subsection">
                        EXCLUSIONS: The following improvements and accessories will be retained by Seller and must be
                        removed prior to delivery of possession: <span class="text-input user_input"> N/A </span>
                    </div>
                </div>
                <div class="subsection">
                    <span>E.</span>
                    <div class="sub_subsection">
                        RESERVATIONS: Any reservation for oil, gas, or other minerals, water, timber, or other interests is
                        made in accordance with an attached addendum.
                    </div>
                </div>
            </div>

            <div class="section">
                <p><strong>3. SALES PRICE:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        Cash portion of Sales Price payable by Buyer at closing .................$...................
                        The term "Cash portion of the Sales Price" does not include proceeds from borrowing of any kind or
                        selling other real property except as disclosed in this contract.
                    </div>
                </div>
                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        Sum of all financing described in the attached: ☒ Third Party Financing Addendum, ☐ Loan Assumption
                        Addendum,☐ Seller Financing Addendum .................$ <span
                            class="text-input user_input">{property_data["admin_data"]["sales_price"]}</span>
                    </div>
                </div>
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        Sales Price (Sum of A and B).................$ <span class="text-input user_input">{property_data["admin_data"]["sales_price"]}</span>
                    </div>
                </div>
            </div>

            <div class="section">
                <p><strong>4. LEASES:</strong> Except as disclosed in this contract, Seller is not aware of any leases
                    affecting the Property. After the Effective Date, Seller may not, without Buyer's written consent,
                    create a new lease, amend any existing lease, or convey any interest in the Property. (Check all
                    applicable boxes)</p>
                <div class="subsection">
                    <span>☐&nbsp;A.</span>
                    <div class="sub_subsection">
                        RESIDENTIAL LEASES: The Property is subject to one or more residential leases and the Addendum
                        Regarding Residential Leases is attached to this contract.
                    </div>
                </div>
                <div class="subsection">
                    <span>☐&nbsp;B.</span>
                    <div class="sub_subsection">
                        FIXTURE LEASES: Fixtures on the Property are subject to one or more fixture leases (for example,
                        solar panels, propane tanks, water softener, security system) and the Addendum Regarding Fixture
                        Leases is attached to this contract.
                    </div>
                </div>
                <div class="subsection">
                    <span>☐&nbsp;C.</span>
                    <div class="sub_subsection">
                        NATURAL RESOURCE LEASES: "Natural Resource Lease" means an existing oil and gas, mineral,
                        geothermal, water, wind, or other natural resource lease affecting the Property to which Seller is a
                        party.
                    </div>
                </div>
                <div class="subsection">
                    <span>☐&nbsp;1.</span>
                    <div class="sub_subsection">
                        Seller has delivered to Buyer a copy of all the Natural Resource Leases.
                    </div>
                </div>
                <div class="subsection">
                    <span>☐&nbsp;2.</span>
                    <div class="sub_subsection">
                        Seller has not delivered to Buyer a copy of all the Natural Resource Leases. Seller shall provide to
                        Buyer a copy of all the Natural Resource Leases within 3 days after the Effective Date. Buyer may
                        terminate the contract within days after the date the Buyer receives all the Natural Resource Leases
                        and the earnest money shall be refunded to Buyer.
                    </div>
                </div>
            </div>
        </div>




        <div class="container">
            <div class="section">
                <p><strong>5. EARNEST MONEY AND TERMINATION OPTION:</strong></p>
            </div>

            <div class="section">
                <!-- <p><strong>2. PROPERTY:</strong> The land, improvements and accessories are collectively referred to as the
                    Property.</p> -->
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        DELIVERY OF EARNEST MONEY AND OPTION FEE: Within 3 days after the Effective Date, Buyer must
                        deliver to <span class="text-input user_input">Buyer's Choice</span> (Escrow Agent) at (address):
                        <span class="text-input user_input">$ {property_data["admin_data"]["earnest_money"]}</span> as earnest money and <span
                            class="text-input user_input">${property_data["admin_data"]["option_fee"]}</span> as
                        the Option Fee. The earnest money and Option Fee shall be made payable to Escrow Agent and may be
                        paid separately or combined in a single payment.
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(1)</span>
                        <div class="sub_subsection">
                            Buyer shall deliver additional earnest money of $ ____________________ to Escrow Agent within
                            <span class="text-input user_input">N/A</span> days after the Effective Date of this
                            contract.

                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(2)</span>
                        <div class="sub_subsection">
                            If the last day to deliver the earnest money, Option Fee, or the additional earnest money falls
                            on a Saturday, Sunday, or legal holiday, the time to deliver the earnest money, Option Fee, or
                            the additional earnest money, as applicable, is extended until the end of the next day that is
                            not a Saturday, Sunday, or legal holiday.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(3)</span>
                        <div class="sub_subsection">
                            The amount(s) Escrow Agent receives under this paragraph shall be applied first to the Option
                            Fee, then to the earnest money, and then to the additional earnest money.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(4)</span>
                        <div class="sub_subsection">
                            Buyer authorizes Escrow Agent to release and deliver the Option Fee to Seller at any time
                            without further notice to or consent from Buyer, and releases Escrow Agent from liability for
                            delivery of the Option Fee to Seller. The Option Fee will be credited to the Sales Price at
                            closing.
                        </div>
                    </div>
                </div>

            </div>



            <div class="section">
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        FAILURE TO TIMELY DELIVER EARNEST MONEY: If Buyer fails to deliver the earnest money within the time
                        required, Seller may terminate this contract or exercise Seller's remedies under Paragraph 15 or
                        both by providing notice to Buyer before Buver delivers the earnest money
                    </div>
                </div>
            </div>


            <div class="section">
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        <strong>TERMINATION OPTION:</strong> For nominal consideration, the receipt of which Seller
                        acknowledges,
                        and Buyer's agreement to pay the Option Fee within the time required, Seller grants Buyer the
                        unrestricted right to terminate this contract by giving notice of termination to Seller within <span
                            class="text-input user_input">{property_data["admin_data"]["buyer_approval_deadline_days"]}</span>
                        days after the Effective Date of this contract (Option Period). Notices under this paragraph must be
                        given by 5:00 p.m. (local time where the Property is located) by the date specified. If Buyer gives
                        notice of termination within the time prescribed: (i) the Option Fee will not be refunded and Escrow
                        Agent shall release any Option Fee remaining with Escrow Agent to Seller; and (ii) any earnest money
                        will be refunded to Buyer.
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="subsection">
                    <span>D.</span>
                    <div class="sub_subsection">
                        FAILURE TO TIMELY DELIVER OPTION FEE: If no dollar amount is stated as the Option Fee or if
                        Buyer fails to deliver the Option Fee within the time required, Buyer shall not have the
                        unrestricted right to terminate this contract under this paragraph 5.
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="subsection">
                    <span>E.</span>
                    <div class="sub_subsection">
                        TIME: <strong>Time is of the essence for this paragraph and strict compliance with the time for
                            performance is required.</strong>
                    </div>
                </div>
            </div>

            <div class="section">
                <p><strong>6. TITLE POLICY AND SURVEY:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        Cash portion of Sales Price payable by Buyer at closing .................$...................
                        The term "Cash portion of the Sales Price" does not include proceeds from borrowing of any kind or
                        selling other real property except as disclosed in this contract.
                    </div>
                </div>
                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        Sum of all financing described in the attached: ☒ Third Party Financing Addendum, ☐ Loan Assumption
                        Addendum,☐ Seller Financing Addendum .................$ <span
                            class="text-input user_input">135,000.00</span>
                    </div>
                </div>
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        Sales Price (Sum of A and B).................$ <span class="text-input user_input">135,000.00</span>
                    </div>
                </div>
            </div>

            <div class="section">
                <p><strong>4. LEASES:</strong> Except as disclosed in this contract, Seller is not aware of any leases
                    affecting the Property. After the Effective Date, Seller may not, without Buyer's written consent,
                    create a new lease, amend any existing lease, or convey any interest in the Property. (Check all
                    applicable boxes)</p>
                <div class="subsection">
                    <span>☐&nbsp;A.</span>
                    <div class="sub_subsection">
                        RESIDENTIAL LEASES: The Property is subject to one or more residential leases and the Addendum
                        Regarding Residential Leases is attached to this contract.
                    </div>
                </div>
                <div class="subsection">
                    <span>☐&nbsp;B.</span>
                    <div class="sub_subsection">
                        FIXTURE LEASES: Fixtures on the Property are subject to one or more fixture leases (for example,
                        solar panels, propane tanks, water softener, security system) and the Addendum Regarding Fixture
                        Leases is attached to this contract.
                    </div>
                </div>
                <div class="subsection">
                    <span>☐&nbsp;C.</span>
                    NATURAL RESOURCE LEASES: "Natural Resource Lease" means an existing oil and gas, mineral,
                    geothermal, water, wind, or other natural resource lease affecting the Property to which Seller is a
                    party.
                </div>
                <div class="subsection">
                    <span>☐&nbsp;1.</span>
                    <div class="sub_subsection">
                        Seller has delivered to Buyer a copy of all the Natural Resource Leases.
                    </div>
                </div>
                <div class="subsection">
                    <span>☐&nbsp;2.</span>
                    <div class="sub_subsection">
                        Seller has not delivered to Buyer a copy of all the Natural Resource Leases. Seller shall provide to
                        Buyer a copy of all the Natural Resource Leases within 3 days after the Effective Date. Buyer may
                        terminate the contract within days after the date the Buyer receives all the Natural Resource Leases
                        and the earnest money shall be refunded to Buyer.
                    </div>
                </div>
            </div>




            <div class="section">
                <p><strong>5. EARNEST MONEY AND TERMINATION OPTION:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        DELIVERY OF EARNEST MONEY AND OPTION FEE: Within 3 days after the Effective Date, Buyer must deliver
                        to <span class="text-input user_input"> Buyer's Choice</span> (Escrow Agent) at (address): <span
                            class="text-input user_input">$ 1,000.00</span> as earnest money and <span
                            class="text-input user_input">$ 100.00</span> as the Option
                        Fee. The earnest money and Option Fee shall be made payable to Escrow Agent and may be paid
                        separately or combined in a single payment.
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>(1)</span>
                        <div class="sub_subsection">
                            to Escrow Agent within
                            (1) Buyer shall deliver additional earnest money of $
                            <span class="text-input user_input">N/A </span>days after the Effective Date of this contract.
                            (2) If the last day to deliver the earnest money, Option Fee, or the additional earnest money
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(2)</span>
                        <div class="sub_subsection">
                            If the last day to deliver the earnest money, Option Fee, or the additional earnest money falls
                            on a Saturday, Sunday, or legal holiday, the time to deliver the earnest money, Option Fee, or
                            the additional earnest money, as applicable, is extended until the end of the next day that is
                            not a Saturday, Sunday, or legal holiday.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(3)</span>
                        <div class="sub_subsection">
                            The amount(s) Escrow Agent receives under this paragraph shall be applied first to the Option
                            Fee, then to the earnest money, and then to the additional earnest money.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(4)</span>
                        <div class="sub_subsection">
                            Buyer authorizes Escrow Agent to release and deliver the Option Fee to Seller at any time
                            without further notice to or consent from Buyer, and releases Escrow Agent from liability for
                            delivery of the Option Fee to Seller. The Option Fee will be credited to the Sales Price at
                            closing.
                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        TERMINATION OPTION: For nominal consideration, the receipt of which Seller acknowledges,
                        and Buyer's agreement to pay the Option Fee within the time required, Seller grants Buyer the
                        days after the Effective Date of this contract (Option Period). Notices under this paragraph must be
                        given by 5:00 p.m. (local time where the Property is located) by the date specified. If Buyer gives
                        notice of termination within the time prescribed: (i) the Option Fee will not be refunded and Escrow
                        Agent shall release any Option Fee remaining with Escrow Agent to Seller; and (ii) any earnest money
                        will be refunded to Buyer.
                    </div>
                </div>
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        FAILURE TO TIMELY DELIVER EARNEST MONEY: If Buyer fails to deliver the earnest money within the time
                        required, Seller may terminate this contract or exercise Seller's remedies under Paragraph 15, or
                        both, by providing notice to Buyer before Buyer delivers the earnest money.
                    </div>
                </div>
                <div class="subsection">
                    <span>D.</span>
                    <div class="sub_subsection">
                        FAILURE TO TIMELY DELIVER OPTION FEE: If no dollar amount is stated as the Option Fee or if
                        Buyer fails to deliver the Option Fee within the time required, Buyer shall not have the
                        unrestricted right to terminate this contract under this paragraph 5.
                    </div>
                </div>
                <div class="subsection">
                    <span>E.</span>
                    <div class="sub_subsection">
                        TIME: <strong> Time is of the essence for this paragraph and strict compliance with the time for
                            performance is required.</strong>
                    </div>
                </div>
            </div>




            <div class="section">
                <p><strong>6. TITLE POLICY AND SURVEY:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        TITLE POLICY: Seller shall furnish to Buyer at ☑ Seller's Buyer's expense an owner policy of title
                        insurance (Title Policy) issued by <span class="text-input user_input"> Buyer's Choice</span>
                        (Title Company)
                        in the amount of the Sales Price, dated at or after closing, insuring Buyer against loss under the
                        provisions of the Title Policy, subject to the promulgated exclusions (including existing building
                        and zoning ordinances) and the following exceptions:
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>(1)</span>
                        <div class="sub_subsection">
                            Restrictive covenants common to the platted subdivision in which the Property is located.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(2)</span>
                        <div class="sub_subsection">
                            The standard printed exception for standby fees, taxes and assessments.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(3)</span>
                        <div class="sub_subsection">
                            Liens created as part of the financing described in Paragraph 3.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(4)</span>
                        <div class="sub_subsection">
                            Utility easements created by the dedication deed or plat of the subdivision in which the
                            Property is located.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(5)</span>
                        <div class="sub_subsection">
                            Reservations or exceptions otherwise permitted by this contract or as may be approved by Buyer
                            in writing.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(6)</span>
                        <div class="sub_subsection">
                            The standard printed exception as to marital rights.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(7)</span>
                        <div class="sub_subsection">
                            The standard printed exception as to waters, tidelands, beaches, streams, and related matters.
                        </div>
                    </div>
                </div>
                <div class="subsection">
                    <div class="subsection">
                        <span>(8)</span>
                        <div class="sub_subsection">
                            The standard printed exception as to discrepancies, conflicts, shortages in area or boundary
                            lines, encroachments or protrusions, or overlapping improvements:
                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>☐</span>
                        <div class="sub_subsection">
                            (i) will not be amended or deleted from the title policy; or

                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>☐</span>
                        <div class="sub_subsection">
                            (ii) will be amended to read, "shortages in area" at the expense of ☐ Buyer ☐ Seller.

                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>(9)</span>
                        <div class="sub_subsection">
                            The exception or exclusion regarding minerals approved by the Texas Department

                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        COMMITMENT: Within 20 days after the Title Company receives a copy of this contract, Seller
                        shall furnish to Buyer a commitment for title insurance (Commitment) and, at Buyer's expense,
                        legible copies of restrictive covenants and documents evidencing exceptions in the Commitment
                        (Exception Documents) other than the standard printed exceptions. Seller authorizes the Title
                        Company to deliver the Commitment and Exception Documents to Buyer at Buyer's address shown in
                        Paragraph 21. If the Commitment and Exception Documents are not delivered to Buyer within the
                        specified time, the time for delivery will be automatically extended up to 15 days or 3 days before
                        the Closing Date, whichever is earlier. If the Commitment and Exception Documents are not delivered
                        within the time required, Buyer may terminate this contract and the earnest money will be refunded
                        to Buyer.er.
                    </div>
                </div>
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        SURVEY: The survey must be made by a registered professional land surveyor acceptable to the Title
                        Company and Buyer's lender(s). (Check one box only)
                    </div>
                </div>



                <div class="subsection">
                    <span>☐</span>
                    <div class="subsection">
                        <span>(1)</span>
                        <div class="sub_subsection">
                            Within <span class="text-input user_input">7</span> days after the Effective Date of this
                            contract, Seller shall furnish to Buyer and Title
                            Company Seller's existing survey of the Property and a Residential Real Property Affidavit or
                            Declaration promulgated by the Texas Department of Insurance (T-47 Affidavit or T-47.1
                            Declaration).
                            Buyer shall obtain a new survey at Seller's expense no later than 3 days prior to Closing Date
                            if
                            Seller fails to furnish within the time prescribed both the: (i) existing survey; and (ii)
                            affidavit
                            or declaration. If the Title Company or Buyer's lender does not accept the existing survey, or
                            the
                            affidavit or declaration, Buyer shall obtain a new survey at Seller's ☐ Buyer's expense no later
                            than 3 days prior to Closing Date.
                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <span>☐</span>
                    <div class="subsection">
                        <span>(2)</span>
                        <div class="sub_subsection">
                            Within <span class="text-input user_input">N/A </span> days after the Effective Date of this
                            contract, Buyer may obtain a new survey at Buyer's
                            expense. Buyer is deemed to receive the survey on the date of actual receipt or the date
                            specified
                            in this paragraph, whichever is earlier. If Buyer fails to obtain the survey, Buyer may not
                            terminate the contract under Paragraph 2B of the Third Party Financing Addendum because the
                            survey
                            was not obtained. </div>
                    </div>
                </div>

                <div class="subsection">
                    <span>☐</span>
                    <div class="subsection">
                        <span>(3)</span>
                        <div class="sub_subsection">
                            Within <span class="text-input user_input">N/A </span> days after the Effective Date of this
                            contract, Seller, at Seller's expense shall furnish
                            a new survey to Buyer. </div>
                    </div>
                </div>




                <div class="subsection">
                    <span>D.</span>
                    <div class="sub_subsection">
                        OBJECTIONS: Buyer may object in writing to defects, exceptions, or encumbrances to title: disclosed
                        on the survey other than items 6A(1) through (7) above; disclosed in the Commitment other than items
                        6A(1) through (9) above; or which prohibit the following use or
                        activity:_______________________________________________________________________________________________________________
                        Buyer must object the earlier of (i) the Closing Date or (ii) <span
                            class="text-input user_input">10</span> days after Buyer receives the
                        Commitment, Exception Documents, and the survey. Buyer's failure to object within the time allowed
                        will constitute a waiver of Buyer's right to object; except that the requirements in Schedule C of
                        the Commitment are not waived by Buyer. Provided Seller is not obligated to incur any expense,
                        Seller shall cure any timely objections of Buyer or any third party lender within 15 days after
                        Seller receives the objections (Cure Period) and the Closing Date will be extended as necessary. If
                        objections are not cured within the Cure Period, Buyer may, by delivering notice to Seller within 5
                        days after the end of the Cure Period: (i) terminate this contract and the earnest money will be
                        refunded to Buyer; or (ii) waive the objections. If Buyer does not terminate within the time
                        required, Buyer shall be deemed to have waived the objections. If the Commitment or survey is
                        revised or any new Exception Document(s) is delivered, Buyer may object to any new matter revealed
                        in the revised Commitment or survey or new Exception Document(s) within the same time stated in this
                        paragraph to make objections beginning when the revised Commitment, survey, or Exception Document(s)
                        is delivered to Buyer.
                    </div>
                </div>
                <div class="subsection">
                    <span>E.</span>
                    <div class="sub_subsection">
                        TITLE NOTICES:
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>(1)</span>
                        <div class="sub_subsection">
                            <strong>ABSTRACT OR TITLE POLICY:</strong> Broker advises Buyer to have an abstract of title
                            covering the
                            Property examined by an attorney of Buyer's selection, or Buyer should be furnished with or
                            obtain a Title Policy. If a Title Policy is furnished, the Commitment should be promptly
                            reviewed by an attorney of Buyer's choice due to the time limitations on Buyer's right to
                            object.
                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>(2)</span>
                        <div class="sub_subsection">
                            <strong>MEMBERSHIP IN PROPERTY OWNERS ASSOCIATION(S):</strong> The Property is ☐ is not subject
                            to mandatory
                            membership in a property owners association(s). If the Property is subject to mandatory
                            membership in a property owners association(s), Seller notifies Buyer under §5.012, Texas
                            Property Code, that, as a purchaser of property in the residential community identified in
                            Paragraph 2A in which the Property is located, <strong> you are obligated to be a member of the
                                property
                                owners association(s). Restrictive covenants governing the use and occupancy of the Property
                                and
                                all dedicatory instruments governing the establishment, maintenance, or operation of this
                                residential community have been or will be recorded in the Real Property Records of the
                                county
                                in which the Property is located. Copies of the restrictive covenants and dedicatory
                                instruments
                                may be obtained from the county clerk. You are obligated to pay assessments to the property
                                owners association(s). The amount of the assessments is subject to change. Your failure to
                                pay
                                the assessments could result in enforcement of the association's lien on and the foreclosure
                                of
                                the Property.</strong>
                            Section 207.003, Property Code, entitles an owner to receive copies of any document that governs
                            the establishment, maintenance, or operation of a subdivision, including, but not limited to,
                            restrictions, bylaws, rules and regulations, and a resale certificate from a property owners'
                            association. A resale certificate contains information including, but not limited to, statements
                            specifying the amount and frequency of regular assessments and the style and cause number of
                            lawsuits to which the property owners' association is a party, other than lawsuits relating to
                            unpaid ad valorem taxes of an individual member of the association. These documents must be made
                            available to you by the property owners' association or the association's agent on your request.
                            <strong>If Buyer is concerned about these matters, the TREC promulgated Addendum for Property
                                Subject to
                                Mandatory Membership in a Property Owners Association(s) should be used. </strong>
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>(3)</span>
                        <div class="sub_subsection">
                            <strong>STATUTORY TAX DISTRICTS:</strong> If the Property is situated in a utility or other
                            statutorily
                            created district providing water, sewer, drainage, or flood control facilities and services,
                            Chapter 49, Texas Water Code, requires Seller to deliver and Buyer to sign the statutory notice
                            relating to the tax rate, bonded indebtedness, or standby fee of the district prior to final
                            execution of this contract. -Initial
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>(4)</span>
                        <div class="sub_subsection">
                            TIDE WATERS: If the Property abuts the tidally influenced waters of the state, §33.135,
                            Texas Natural Resources Code, requires a notice regarding coastal area property to be
                            included in the contract. An addendum containing the notice promulgated by TREC or
                            required by the parties must be used.
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>(5)</span>
                        <div class="sub_subsection">
                            ANNEXATION: If the Property is located outside the limits of a municipality, Seller notifies
                            Buyer under §5.011, Texas Property Code, that the Property may now or later be included in
                            the extraterritorial jurisdiction of a municipality and may now or later be subject to
                            annexation by the municipality. Each municipality maintains a map that depicts it
                            boundaries and extraterritorial jurisdiction. To determine if the Property is located within a
                            municipality's extraterritorial jurisdiction or is likely to be located within a municipality's
                            extraterritorial jurisdiction, contact all municipalities located in the general proximity of
                            the
                            Property for further information.
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>(6)</span>
                        <div class="sub_subsection">
                            PROPERTY LOCATED IN A CERTIFICATED SERVICE AREA OF A UTILITY SERVICE PROVIDER:
                            Notice required by §13.257, Water Code: The real property, described in Paragraph 2, that
                            you are about to purchase may be located in a certificated water or sewer service area,
                            which is authorized by law to provide water or sewer service to the properties in the
                            certificated area. If your property is located in a certificated area there may be special costs
                            or charges that you will be required to pay before you can receive water or sewer service.
                            There may be a period required to construct lines or other facilities necessary to provide
                            water or sewer service to your property. You are advised to determine if the property is in a
                            certificated area and contact the utility service provider to determine the cost that you will
                            be required to pay and the period, if any, that is required to provide water or sewer service
                            to your property. The undersigned Buyer hereby acknowledges receipt of the foregoing
                            notice at or before the execution of a binding contract for the purchase of the real property
                            described in Paragraph 2 or at closing of purchase of the real property.
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(7)</span>
                        <div class="sub_subsection">
                            PUBLIC IMPROVEMENT DISTRICTS: If the Property is in a public improvement district, Seller
                            must give Buyer written notice as required by §5.014, Property Code. An addendum
                            containing the required notice shall be attached to this contract.
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(8)</span>
                        <div class="sub_subsection">
                            containing the required notice shall be attached to this contract.
                            TRANSFER FEES: If the Property is subject to a private transfer fee obligation, §5.205,
                            Property Code, requires Seller to notify Buyer as follows: The private transfer fee
                            obligation
                            may be governed by Chapter 5, Subchapter G of the Texas Property Code.
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(9)</span>
                        <div class="sub_subsection">
                            PROPANE GAS SYSTEM SERVICE AREA: If the Property is located in a propane gas system
                            service area owned by a distribution system retailer, Seller must give Buyer written notice
                            as required by §141.010, Texas Utilities Code. An addendum containing the notice approved
                            by TREC or required by the parties should be used.
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>(10)</span>
                        <div class="sub_subsection">
                            (10) NOTICE OF WATER LEVEL FLUCTUATIONS: If the Property adjoins an impoundment of
                            water, including a reservoir or lake, constructed and maintained under Chapter 11, Water
                            Code, that has a storage capacity of at least 5,000 acre-feet at the impoundment's normal
                            operating level, Seller hereby notifies Buyer: "The water level of the impoundment of water
                            adjoining the Property fluctuates for various reasons, including as a result of: (1) an
                            entity
                            lawfully exercising its right to use the water stored in the impoundment; or (2) drought or
                            flood conditions."
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(11)</span>
                        <div class="sub_subsection">
                            CERTIFICATE OF MOLD REMEDIATION: If the Property has been remediated for mold, Seller
                            must provide to Buyer each certificate of mold damage remediation issued under
                            §1958.154, Occupations Code, during the 5 years preceding the sale of the Property.
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(12)</span>
                        <div class="sub_subsection">
                            REQUIRED NOTICES: The following notices have been given or are attached to this
                            contract (for example, utility, water, drainage, and public improvement
                            districts):_________________________________________________________________________________________________
                            <br>____________________________________________________________________________________________________________
                        </div>
                    </div>
                </div>
            </div>










            <div class="section">
                <p><strong>7. PROPERTY CONDITION:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        ACCESS, INSPECTIONS AND UTILITIES: Seller shall permit Buyer and Buyer's agents access
                        to the Property at reasonable times. Buyer may have the Property inspected by inspectors
                        selected by Buyer and licensed by TREC or otherwise permitted by law to make inspections.
                        Any hydrostatic testing must be separately authorized by Seller in writing. Seller at Seller's
                        expense shall immediately cause existing utilities to be turned on and shall keep the utilities
                        on during the time this contract is in effect.
                    </div>
                </div>


                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        SELLER'S DISCLOSURE NOTICE PURSUANT TO §5.008, TEXAS PROPERTY CODE (Notice):
                        (Check one box only)
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>☐ </span>
                        <div class="subsection">
                            <span>(1)</span>
                            <div class="sub_subsection">
                                Buyer has received the Notice.
                            </div>
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>☐ </span>
                        <div class="subsection">
                            <span>(2)</span>
                            <div class="sub_subsection">
                                Buyer has not received the Notice. Within <span class="text-input user_input">7</span> days
                                after the Effective Date of this
                                contract, Seller shall deliver the Notice to Buyer. If Buyer does not receive the Notice,
                                Buyer may terminate this contract at any time prior to the closing and the earnest money
                                will be refunded to Buyer. If Seller delivers the Notice, Buyer may terminate this contract
                                for any reason within 7 days after Buyer receives the Notice or prior to the closing,
                                whichever first occurs, and the earnest money will be refunded to Buyer. </div>
                        </div>
                    </div>
                </div>




                <div class="subsection">
                    <div class="subsection">
                        <span>☐ </span>
                        <div class="subsection">
                            <span>(3)</span>
                            <div class="sub_subsection">
                                The Seller is not required to furnish the notice under the Texas Property Code. </div>
                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        FAILURE TO TIMELY DELIVER EARNEST MONEY: If Buyer fails to deliver the earnest money within the time
                        SELLER'S DISCLOSURE OF LEAD-BASED PAINT AND LEAD-BASED PAINT HAZARDS is required
                        by Federal law for a residential dwelling constructed prior to 1978.
                    </div>
                </div>
                <div class="subsection">
                    <span>D.</span>
                    <div class="sub_subsection">
                        ACCEPTANCE OF PROPERTY CONDITION: "As Is" means the present condition of the Property
                        with any and all defects and without warranty except for the warranties of title and the warranties
                        in this contract. Buyer's agreement to accept the Property As Is under Paragraph
                        7D(1) or (2) does not preclude Buyer from inspecting the Property under Paragraph 7A, from
                        negotiating repairs or treatments in a subsequent amendment, or from terminating this
                        contract during the Option Period, if any. <br>

                    </div>

                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>☐ </span>
                        <div class="subsection">
                            <span>(1)</span>
                            <div class="sub_subsection">
                                Buyer accepts the Property As Is.
                            </div>
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>☐ </span>
                        <div class="subsection">
                            <span>(2)</span>
                            <div class="sub_subsection">
                                Buyer accepts the Property As Is provided Seller, at Seller's expense, shall complete the
                                following specific repairs and treatments: <span class="text-input user_input">N/A</span>
                                _____________________________________________________________________________________________________
                                <br>
                                ____________________________________________________________________________________________________
                                (Do not insert general phrases, such as "subject to inspections" that do not identify
                                specific
                                repairs and treatments.)
                            </div>
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <span>E.</span>
                    <div class="sub_subsection">
                        LENDER REQUIRED REPAIRS AND TREATMENTS: Unless otherwise agreed in writing, neither
                        party is obligated to pay for lender required repairs, which includes treatment for wood
                        destroying insects. If the parties do not agree to pay for the lender required repairs or
                        treatments, this contract will terminate and the earnest money will be refunded to Buyer. If
                        the cost of lender required repairs and treatments exceeds 5% of the Sales Price, Buyer may
                        terminate this contract and the earnest money will be refunded to Buyer.
                    </div>
                </div>

                <div class="subsection">
                    <span>F.</span>
                    <div class="sub_subsection">
                        COMPLETION OF REPAIRS AND TREATMENTS: Unless otherwise agreed in writing, Seller shall
                        complete all agreed repairs and treatments prior to the Closing Date and obtain any required
                        permits. The repairs and treatments must be performed by persons who are licensed to
                        provide such repairs or treatments or, if no license is required by law, are commercially
                        engaged in the trade of providing such repairs or treatments. Seller shall: (i) provide Buyer
                        with copies of documentation from the repair person(s) showing the scope of work and
                        payment for the work completed; and (ii) at Seller's expense, arrange for the transfer of any
                        transferable warranties with respect to the repairs and treatments to Buyer at closing. If Seller
                        fails to complete any agreed repairs and treatments prior to the Closing Date, Buyer may
                        exercise remedies under Paragraph 15 or extend the Closing Date up to 5 days if necessary for
                        Seller to complete the repairs and treatments.
                    </div>
                </div>


                <div class="subsection">
                    <span>G.</span>
                    <div class="sub_subsection">
                        ENVIRONMENTAL MATTERS: Buyer is advised that the presence of wetlands, toxic substances,
                        including asbestos and wastes
                        threatened or endangered species or its habitat may affect Buyer's intended use of the
                        Property. If Buyer is concerned about these matters, an addendum promulgated by TREC or
                        required by the parties should be used.
                    </div>
                </div>



                <div class="subsection">
                    <span>H.</span>
                    <div class="sub_subsection">
                        RESIDENTIAL SERVICE CONTRACTS: Buyer may purchase a residential service contract from a
                        provider or administrator licensed by the Texas Department of Licensing and Regulation. If
                        Buyer purchases a residential service contract, Seller shall reimburse Buyer at closing for the
                        cost of the residential service contract in an amount not exceeding $
                        should review any residential service contract for the scope of coverage, exclusions and
                        limitations. <strong> The purchase of a residential service contract is optional. Similar coverage
                            may be purchased from various companies authorized to do business in Texas.</strong>
                    </div>
                </div>
            </div>








            <div class="section">
                <p><strong>8. BROKERS AND SALES AGENTS:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        BROKER OR SALES AGENT DISCLOSURE: Texas law requires a real estate broker or sales
                        agent who is a party to a transaction or acting on behalf of a spouse, parent, child, business
                        entity in which the broker or sales agent owns more than 10%, or a trust for which the broker
                        or sales agent acts as a trustee or of which the broker or sales agent or the broker or sales
                        agent's spouse, parent or child is a beneficiary, to notify the other party in writing before
                        entering into a contract of sale. Disclose if applicable:
                        ____________________________________________________________________________________________________________
                        <br> ______________________________________________________________________________
                    </div>
                </div>


                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        BROKERS' FEES: All obligations of the parties for payment of brokers' fees are contained in
                        separate written agreements.
                    </div>
                </div>
            </div>




            <div class="section">
                <p><strong>9. CLOSING:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        The closing of the sale will be on or before <span class="text-input user_input">September 15 ,
                            2025</span> or within 7 days
                        after objections made under Paragraph 6D have been cured or waived, whichever date is later
                        (Closing Date). If either party fails to close the sale by the Closing Date, the non-defaulting
                        party may exercise the remedies contained in Paragraph 15.
                    </div>
                </div>


                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        At closing:
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(1)</span>
                        <div class="sub_subsection">
                            Seller shall execute and deliver a general warranty deed conveying title to the Property to
                            Buyer and showing no additional exceptions to those permitted in Paragraph 6 and furnish
                            tax statements or certificates showing no delinquent taxes on the Property.
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(2)</span>
                        <div class="sub_subsection">
                            Buyer shall pay the Sales Price in good funds acceptable to the Escrow Agent.
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <span>(3)</span>
                        <div class="sub_subsection">
                            Seller and Buyer shall execute and deliver any notices, statements, certificates, affidavits,
                            releases, loan documents, transfer of any warranties, and other documents reasonably
                            required for the closing of the sale and the issuance of the Title Policy.
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(4)</span>
                        <div class="sub_subsection">
                            There will be no liens, assessments, or security interests against the Property which will
                            not be satisfied out of the sales proceeds unless securing the payment of any loans
                            assumed by Buyer and assumed loans will not be in default.
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(5)</span>
                        <div class="sub_subsection">
                            Private transfer fees (as defined by Chapter 5, Subchapter G of the Texas Property Code) will be
                            the obligation of Seller unless provided otherwise in this contract. Transfer fees
                            assessed by a property owners' association are governed by the Addendum for Property
                            Subject to Mandatory Membership in a Property Owners Association.
                        </div>
                    </div>
                </div>
            </div>






            <div class="section">
                <p><strong>10. POSSESSION:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        BUYER'S POSSESSION: Seller shall deliver to Buyer possession of the Property in its present or
                        required condition, ordinary wear and tear excepted: ☐ upon closing and funding ☐ according
                        to a temporary residential lease form promulgated by TREC or other written lease required by
                        the parties. Any possession by Buyer prior to closing or by Seller after closing which is not
                        authorized by a written lease will establish a tenancy at sufferance relationship between the
                        parties. <strong> Consult your insurance agent prior to change of ownership and possession
                            because insurance coverage may be limited or terminated. The absence of a written
                            lease or appropriate insurance coverage may expose the parties to economic loss.</strong>
                    </div>
                </div>


                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        SMART DEVICES: "Smart Device" means a device that connects to the internet to enable
                        remote use, monitoring, and management of: (i) the Property; (ii) items identified in any Non-
                        Realty Items Addendum; or (iii) items in a Fixture Lease assigned to Buyer. At the time Seller
                    </div>


                    <div class="subsection">
                        <div class="subsection">
                            <span>(1)</span>
                            <div class="sub_subsection">
                                deliver to Buyer written information containing all access codes, usernames, passwords,
                                and applications Buyer will need to access, operate, manage, and control the Smart
                                Devices; and
                            </div>
                        </div>
                    </div>



                    <div class="subsection">
                        <div class="subsection">
                            <span>(2)</span>
                            <div class="sub_subsection">
                                terminate and remove all access and connections to the improvements and accessories
                                from any of Seller's personal devices including but not limited to phones and computers.
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class="section">
                <p><strong>11. SPECIAL PROVISIONS:</strong> </p>
                <div class="subsection">
                    <p>(This paragraph is intended to be used only for additional
                        informational
                        items. An informational item is a statement that completes a blank in a contract form, discloses
                        factual information, or provides instructions. Real estate brokers and sales agents are prohibited
                        from practicing law and shall not add to, delete, or modify any provision of this contract unless
                        drafted by a party to this contract or a party's attorney.) <span class="text-input user_input">
                            Buyer
                            may obtain a private loan with no appraisal
                            contingencies</span> </p>
                </div>

            </div>



            <div class="section">
                <p><strong>12. SETTLEMENT AND OTHER EXPENSES:</strong></p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        The following expenses must be paid at or prior to closing:
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <span>(1)</span>
                        <div class="sub_subsection">
                            Seller shall pay the following expenses (Seller's Expenses):
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <div class="subsection">
                        <div class="subsection">
                            <span>(a)</span>
                            <div class="sub_subsection">
                                releases of existing liens, including prepayment penalties and recording fees; release of
                                Seller's loan liability; tax statements or certificates; preparation of deed; one-half of
                                escrow fee; brokerage fees that Seller has agreed to pay; and other expenses payable
                                by Seller under this contract;
                            </div>
                        </div>
                    </div>
                </div>

                <div class="subsection">
                    <div class="subsection">
                        <div class="subsection">
                            <span>(b)</span>
                            <div class="sub_subsection">
                                the following amount to be applied to brokerage fees that Buyer has agreed to pay: ☐
                                $_____________ or ☐ $_____________
                                % of the Sales Price (check one box only); and
                            </div>
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <div class="subsection">
                            <span>(c)</span>
                            <div class="sub_subsection">
                                an amount not to exceed
                                $_____________ to be applied to other Buyer's Expenses.
                            </div>
                        </div>
                    </div>
                </div>



                <div class="subsection">
                    <div class="subsection">
                        <span>(2)</span>
                        <div class="sub_subsection">
                            Buyer shall pay the following expenses (Buyer's Expenses): Appraisal fees; loan application
                            fees; origination charges; credit reports; preparation of loan documents; interest on the
                            notes from date of disbursement to one month prior to dates of first monthly payments;
                            recording fees; copies of easements and restrictions; loan title policy with endorsements
                            required by lender; loan-related inspection fees; photos; amortization schedules; one-half
                            of escrow fee; all prepaid items, including required premiums for flood and hazard
                            insurance, reserve deposits for insurance, ad valorem taxes and special governmental
                            assessments; final compliance inspection; courier fee; repair inspection; underwriting fee;
                            wire transfer fee; expenses incident to any loan; Private Mortgage Insurance Premium
                            (PMI), VA Loan Funding Fee, or FHA Mortgage Insurance Premium (MIP) as required by the
                            lender; brokerage fees that Buyer has agreed to pay; and other expenses payable by Buyer
                            under this contract.
                        </div>
                    </div>
                </div>


                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        If any expense exceeds an amount expressly stated in this contract for such expense to be
                        paid by a party, that party may terminate this contract unless the other party agrees to pay
                        such excess. Buyer may not pay charges and fees expressly prohibited by FHA, VA, Texas
                        Veterans Land Board or other governmental loan program regulations.
                    </div>
                </div>


            </div>




            <div class="section">
                <p><strong>13. PRORATIONS:</strong> </p>
                <div class="subsection">
                    <p>Taxes for the current year, interest, rents, and regular periodic maintenance
                        fees, assessments, and dues (including prepaid items) will be prorated through the Closing Date.
                        The tax proration may be calculated taking into consideration any change in exemptions that will
                        affect the
                        current year's taxes. If taxes for the current year vary from the amount prorated at closing, the
                        parties shall
                        adjust the prorations when tax statements for the current year are available. If taxes are not paid
                        at or prior to
                        closing, Buyer shall pay taxes for the current year.
                    </p>
                </div>
            </div>


            <div class="section">
                <p><strong>14. CASUALTY LOSS:</strong> </p>
                <div class="subsection">
                    <p>If any part of the Property is damaged or destroyed by fire or other casualty
                        after the Effective Date of this contract, Seller shall restore the Property to its previous
                        condition
                        as soon as reasonably possible, but in any event by the Closing Date. If Seller fails to do so due
                        to
                        factors beyond Seller's control, Buyer may (a) terminate this contract and the earnest money will
                        be refunded to Buyer (b) extend the time for performance up to 15 days and the Closing Date will
                        be extended as necessary or (c) accept the Property in its damaged condition with an assignment
                        of insurance proceeds, if permitted by Seller's insurance carrier, and receive credit from Seller at
                        closing in the amount of the deductible under the insurance policy. Seller's obligations under this
                        paragraph are independent of any other obligations of Seller under this contract.
                    </p>
                </div>
            </div>


            <div class="section">
                <p><strong>15. DEFAULT:</strong> </p>
                <div class="subsection">
                    <p>If Buyer fails to comply with this contract, Buyer will be in default, and Seller may (a)
                        enforce specific performance, seek such other relief as may be provided by law, or both, or (b)
                        terminate this contract and receive the earnest money as liquidated damages, thereby releasing
                        both parties from this contract. If Seller fails to comply with this contract, Seller will be in
                        default
                        and Buyer may (a) enforce specific performance, seek such other relief as may be provided by
                        law, or both, or (b) terminate this contract and receive the earnest money, thereby releasing both
                        parties from this contract.
                    </p>
                </div>
            </div>



            <div class="section">
                <p><strong>16. MEDIATION:</strong> </p>
                <div class="subsection">
                    <p>It is the policy of the State of Texas to encourage resolution of disputes through
                        alternative dispute resolution procedures such as mediation. Any dispute between Seller and
                        Buyer related to this contract which is not resolved through informal discussion will be
                        submitted to a mutually acceptable mediation service or provider. The parties to the mediation
                        shall bear the mediation costs equally. This paragraph does not preclude a party from seeking
                        equitable relief from a court of competent jurisdiction.
                    </p>
                </div>
            </div>



            <div class="section">
                <p><strong>17. ATTORNEY'S FEES:</strong> </p>
                <div class="subsection">
                    <p>A Buyer, Seller, Listing Broker, Other Broker, or Escrow Agent who prevails
                        in any legal proceeding related to this contract is entitled to recover reasonable attorney's fees
                        and all costs of such proceeding.
                    </p>
                </div>
            </div>




            <div class="section">
                <p><strong>18. ESCROW:</strong> </p>
                <div class="subsection">
                    <span>A.</span>
                    <div class="sub_subsection">
                        ESCROW: The Escrow Agent is not (i) a party to this contract and does not have liability for the
                        performance or nonperformance of any party to this contract, (ii) liable for interest on the
                        earnest money and (iii) liable for the loss of any earnest money caused by the failure of any
                        financial institution in which the earnest money has been deposited unless the financial
                        institution is acting as Escrow Agent. Escrow Agent may require any disbursement made in
                        connection with this contract to be conditioned on Escrow Agent's collection of good funds
                        acceptable to Escrow Agent.
                    </div>
                </div>
                <div class="subsection">
                    <span>B.</span>
                    <div class="sub_subsection">
                        EXPENSES: At closing, the earnest money must be applied first to any cash down payment,
                        then to Buyer's Expenses and any excess refunded to Buyer. If no closing occurs, Escrow Agent
                        may: (i) require a written release of liability of the Escrow Agent from all parties before
                        releasing any earnest money; and (ii) require payment of unpaid expenses incurred on behalf
                        of a party. Escrow Agent may deduct authorized expenses from the earnest money payable to a
                        party. "Authorized expenses" means expenses incurred by Escrow Agent on behalf of the party
                        entitled to the earnest money that were authorized by this contract or that party.
                    </div>
                </div>
                <div class="subsection">
                    <span>C.</span>
                    <div class="sub_subsection">
                        DEMAND: Upon termination of this contract, either party or the Escrow Agent may send a
                        release of earnest money to each party and the parties shall execute counterparts of the
                        release and deliver same to the Escrow Agent. If either party fails to execute the release, either
                        party may make a written demand to the Escrow Agent for the earnest money. If only one
                        party makes written demand for the earnest money, Escrow Agent shall promptly provide a
                        copy of the demand to the other party. If Escrow Agent does not receive written objection to
                        the demand from the other party within 15 days, Escrow Agent may disburse the earnest
                        money to the party making demand reduced by the amount of unpaid expenses incurred on
                        behalf of the party receiving the earnest money and Escrow Agent may pay the same to the
                        creditors. If Escrow Agent complies with the provisions of this paragraph, each party hereby
                        releases Escrow Agent from all adverse claims related to the disbursal of the earnest money.
                    </div>
                </div>
                <div class="subsection">
                    <span>D.</span>
                    <div class="sub_subsection">
                        DAMAGES: Any party who wrongfully fails or refuses to sign a release acceptable to the Escrow
                        Agent within 7 days of receipt of the request will be liable to the other party for (i) damages;
                        (ii) the earnest money; (iii) reasonable attorney's fees; and (iv) all costs of suit.
                    </div>
                </div>
                <div class="subsection">
                    <span>E.</span>
                    <div class="sub_subsection">
                        NOTICES: Escrow Agent's notices will be effective when sent in compliance with Paragraph 21.
                        Notice of objection to the demand will be deemed effective upon receipt by Escrow Agent.
                    </div>
                </div>

            </div>


            <div class="section">
                <p><strong>19. REPRESENTATIONS:</strong> </p>
                <div class="subsection">
                    <p>All covenants, representations and warranties in this contract survive
                        closing. If any representation of Seller in this contract is untrue on the Closing Date, Seller will
                        be
                        in default. Unless expressly prohibited by written agreement, Seller may continue to show the
                        Property and receive, negotiate and accept back up offers.
                    </p>
                </div>
            </div>



            <div class="section">
                <p><strong>20. FEDERAL REQUIREMENTS:</strong> </p>
                <div class="subsection">
                    <p>and its regulations, or if Seller fails to deliver an affidavit or a certificate of non-foreign
                        status to
                        Buyer that Seller is not a "foreign person," then Buyer shall withhold from the sales proceeds an
                        amount sufficient to comply with applicable tax law and deliver the same to the Internal Revenue
                        Service together with appropriate tax forms. Internal Revenue Service regulations require filing
                        written reports if currency in excess of specified amounts is received in the transaction.
                    </p>
                </div>
            </div>





            <div class="section">
                <p><strong>21. NOTICES:</strong> </p>
                <div class="subsection">
                    <p>
                        All notices from one party to the other must be in writing and are effective when
                        mailed to, hand-delivered at, or transmitted by fax or electronic transmission as follows:
                    </p>
                </div>


                <div class="notices-container">

                    <div class="notice-grid">
                        <!-- LEFT COLUMN: Buyer -->
                        <div class="notice-col" aria-labelledby="buyer-heading">
                            <div class="col-header" id="buyer-heading">
                                <span>To Buyer at:</span>
                            </div>

                            <div class="field-row">
                                <!-- <label class="field-label">Address:</label> -->
                                <div class="line"></div>
                                <div class="line"></div>
                            </div>

                            <div class="field-row">
                                <label class="field-label">Phone:
                                    <span class="small-line" aria-hidden="true"></span>
                                </label>
                            </div>

                            <div class="field-row">
                                <label class="field-label">E-mail/Fax:
                                    <div class="small-line" style="width:90%; display:block;" aria-hidden="true"></div>
                                </label>
                            </div>

                            <div class="copy-note">With a copy to Buyer's agent at:</div>
                            <div class="agent-block">
                                <div class="field-label two-lines">Agent name / Office:</div>
                                <div class="line"></div>
                                <div class="field-label two-lines">E-mail/Fax:</div>
                                <div class="line" style="width:80%;"></div>
                            </div>
                        </div>

                        <!-- RIGHT COLUMN: Seller -->
                        <div class="notice-col" aria-labelledby="seller-heading">
                            <div class="col-header" id="seller-heading">
                                <span>To Seller at:</span>
                            </div>

                            <div class="field-row">
                                <!-- <label class="field-label">Address:</label> -->
                                <div class="line"></div>
                                <div class="line"></div>
                            </div>

                            <div class="field-row">
                                <label class="field-label">Phone:
                                    <span class="small-line" aria-hidden="true"></span>
                                </label>
                            </div>

                            <div class="field-row">
                                <label class="field-label">E-mail/Fax:
                                    <div class="small-line" style="width:90%; display:block;" aria-hidden="true"></div>
                                </label>
                            </div>

                            <div class="copy-note">With a copy to Seller's agent at:</div>
                            <div class="agent-block">
                                <div class="field-label two-lines">Agent name / Office:</div>
                                <div class="line"></div>
                                <div class="field-label two-lines">E-mail/Fax:</div>
                                <div class="line" style="width:80%;"></div>
                            </div>
                            <!-- </div> -->
                        </div>
                    </div>
                </div>







            </div>









            <div class="section">
                <p><strong>22. AGREEMENT OF PARTIES:</strong> </p>
                <div class="subsection">
                    <p>
                        This contract contains the entire agreement of the parties and
                        cannot be changed except by their written agreement. Addenda which are a part of this contract
                        are (Check all applicable boxes):
                    </p>
                </div>


                <div class="notices-container">

                    <div class="notice-grid">
                        <!-- LEFT COLUMN: Buyer -->
                        <div class="notice-col" aria-labelledby="buyer-heading">
                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp;Third Party Financing Addendum</span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Seller Financing Addendum </span>
                            </div>

                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp;Addendum for Property Subject to
                                    Mandatory Membership in a Property
                                    Owners Association </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp;Buyer's Temporary Residential Lease </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Loan Assumption Addendum </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum for Sale of Other Property by
                                    Buyer </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum for Reservation of Oil, Gas
                                    and Other Minerals </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum for "Back-Up" Contract </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp;Addendum for Coastal Area Property </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp;Addendum for Authorizing Hydrostatic
                                    Testing </span>
                            </div>



                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp;Seller's Temporary Residential Lease</span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Short Sale Addendum</span>
                            </div>



                        </div>

                        <!-- RIGHT COLUMN: Seller -->
                        <div class="notice-col" aria-labelledby="seller-heading">
                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum for Property Located Seaward
                                    of the Gulf Intracoastal Waterway
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum for Seller's Disclosure of
                                    Information on Lead-based Paint and
                                    Lead-based Paint Hazards as Required by
                                    Federal Law
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum for Property in a Propane Gas
                                    System Service Area
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum Regarding Residential Leases
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum Regarding Fixture Leases
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum containing Notice of Obligation
                                    to Pay Improvement District Assessment
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Addendum for Section 1031 Exchange
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp;
                                </span>
                            </div>


                            <div class="col-header" id="buyer-heading">
                                <span>☐&nbsp;&nbsp;&nbsp; Other (list):
                                </span>
                            </div>


                            <div class="field-row">
                                <div class="line"></div>
                                <div class="line"></div>
                            </div>

                        </div>
                    </div>
                </div>







            </div>




            <div class="section">
                <p><strong>23. CONSULT AN ATTORNEY BEFORE SIGNING:</strong> </p>
                <div class="subsection">
                    <p>
                        TREC rules prohibit real estate brokers and sales
                        agents from giving legal advice. READ THIS CONTRACT CAREFULLY.
                    </p>
                </div>


                <div class="notices-container">

                    <div class="notice-grid">
                        <!-- LEFT COLUMN: Buyer -->
                        <div class="notice-col" aria-labelledby="buyer-heading">
                            <div class="col-header" id="buyer-heading">
                                <span>Buyer's
                                    Attorney is:</span>
                            </div>

                            <div class="field-row">
                                <!-- <label class="field-label">Address:</label> -->
                                <div class="line"></div>
                                <div class="line"></div>
                            </div>

                            <div class="field-row">
                                <label class="field-label">Phone:
                                    <!-- <div class="line"></div> -->
                                    <span class="small-line" aria-hidden="true"></span>
                                </label>
                            </div>

                            <div class="field-row">
                                <label class="field-label">Fax:
                                    <span class="small-line" aria-hidden="true"></span>
                                    <!-- <div class="line"></div> -->
                                    <!-- <div class="small-line" style="width:90%; display:block;" aria-hidden="true"></div> -->
                                </label>
                            </div>

                            <div class="field-row">
                                <label class="field-label">E-mail:
                                    <span class="small-line" aria-hidden="true"></span>
                                    <!-- <div class="line"></div> -->
                                    <!-- <div class="small-line" style="width:90%; display:block;" aria-hidden="true"></div> -->
                                </label>
                            </div>

                        </div>

                        <!-- RIGHT COLUMN: Seller -->
                        <div class="notice-col" aria-labelledby="seller-heading">
                            <div class="col-header" id="seller-heading">
                                <span>Seller's
                                    Attorney is:</span>
                            </div>

                            <div class="field-row">
                                <!-- <label class="field-label">Address:</label> -->
                                <div class="line"></div>
                                <div class="line"></div>
                            </div>

                            <div class="field-row">
                                <label class="field-label">Phone:
                                    <span class="small-line" aria-hidden="true"></span>
                                </label>
                            </div>
                            <div class="field-row">
                                <label class="field-label">Fax:
                                    <span class="small-line" aria-hidden="true"></span>
                                    <!-- <div class="line"></div> -->
                                    <!-- <div class="small-line" style="width:90%; display:block;" aria-hidden="true"></div> -->
                                </label>
                            </div>

                            <div class="field-row">
                                <label class="field-label">E-mail:
                                    <span class="small-line" aria-hidden="true"></span>
                                    <!-- <div class="line"></div> -->
                                    <!-- <div class="small-line" style="width:90%; display:block;" aria-hidden="true"></div> -->
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>





            <!-- Executed Section -->
            <div class="executed-box">
                <p class="total-center">
                    EXECUTED the <span class="line small-inline"></span> day of
                    <span class="line large-inline"></span>, 20<span class="line small-inline"></span>
                    (Effective Date).<br />
                    (BROKER: FILL IN THE DATE OF FINAL ACCEPTANCE.)
                </p>
            </div>

            <div class="signature-grid">
                <div class="signature-col">
                    <div class="signed-by">
                        <span class="sig-label">Signed by:</span>
                        <div class="line sig-line"></div>
                    </div>
                    <p class="party-name">
                        Buyer Silverkey Investments LLC or Designated entity
                    </p>
                    <p class="sig-date">8/25/2025</p>
                    <div class="line party-line"></div>
                    <p class="role">Buyer</p>
                </div>

                <div class="signature-col">
                    <p class="party-name">
                        Seller SECRETARY OF VETERANS AFFAIRS
                    </p>
                    <div class="line party-line"></div>
                    <p class="role">Seller</p>
                </div>
            </div>






            <div class="">
                <p class="total-center"><strong>BROKER INFORMATION</strong> <br> (Print name(s) only. Do not sign) </p>

                <div class="notices-container">

                    <div class="notice-grid">
                        <!-- LEFT COLUMN: Buyer -->
                        <div class="notice-col col-header" aria-labelledby="buyer-heading">
                            <div style="display: block;">
                                <div class="col-header" id="buyer-heading">
                                    <span class="text-input user_input">Loaded Realty Company</span>
                                    <span class="text-input user_input" style="text-align: end;">9015900</span>
                                </div>
                                <div class="col-header" id="buyer-heading">
                                    <span>Other Broker Firm</span>
                                    <span>License No.</span>
                                </div>
                            </div>
                        </div>



                        <!-- <div class="notice-col col-header" style="display: block;" aria-labelledby="buyer-heading"> -->
                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Poly Properties</span>
                                <span class="text-input user_input" style="text-align: end;"> </span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Listing Broker Firm</span>
                                <span>License No.</span>
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="">represents</span>
                                <div style="display: block; ">
                                    <div style="margin-bottom: 10px;">☐ Buyer only as Buyer's agent</div>
                                    <div>☐ Seller as Listing Broker's subagent</div>
                                </div>
                            </div>
                        </div>



                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="">represents</span>
                                <div style="display: block; ">
                                    <div style="margin-bottom: 10px;">☐ Seller and Buyer as an intermediary</div>
                                    <div>☐ Seller only as Seller's agent</div>
                                </div>
                            </div>
                        </div>




                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Joel Villanueva</span>
                                <span class="text-input user_input" style="text-align: end;">817205</span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Associate's Name</span>
                                <span>License No.</span>
                            </div>
                        </div>




                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Harold Johnson</span>
                                <span class="text-input user_input" style="text-align: end;">0510611</span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Listing Associate's Name</span>
                                <span>License No.</span>
                            </div>
                        </div>






                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Loaded Realty Group</span>
                                <!-- <span class="text-input user_input" style="text-align: end;">0510611</span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Team Name</span>
                                <!-- <span>License No.</span> -->
                            </div>
                        </div>
                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Poly Properties</span>
                                <!-- <span class="text-input user_input" style="text-align: end;">0510611</span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Team Name</span>
                                <!-- <span>License No.</span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">villanuevajoele@gmail.com</span>
                                <span class="text-input user_input" style="text-align: end;">(210)740-5663</span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Associate's Email Address</span>
                                <span>Phone</span>
                            </div>
                        </div>



                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">realestate@liberated.net</span>
                                <span class="text-input user_input" style="text-align: end;">(210)473-5578</span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Listing Associate's Email Addresss</span>
                                <span>Phone</span>
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Carlos Puckerin</span>
                                <span class="text-input user_input" style="text-align: end;">0759746</span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Licensed Supervisor of Associate</span>
                                <span>License No.</span>
                            </div>
                        </div>



                        <div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span class="text-input user_input">Carlos Puckerin</span> -->
                                <!-- <span class="text-input user_input" style="text-align: end;">0759746</span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Licensed Supervisor of Listing Associate</span>
                                <span>License No.</span>
                            </div>
                        </div>



                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">825 Town & Country Lane</span>
                                <span class="text-input user_input" style="text-align: end;">(832)856-9022</span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Other Broker's Address</span>
                                <span>Phone</span>
                            </div>
                        </div>




                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">8238 Morning Grove</span>
                                <span class="text-input user_input" style="text-align: end;">(210)473-5578</span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Listing Broker's Office Address</span>
                                <span>Phone</span>
                            </div>
                        </div>



                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Houston</span>
                                <span class="text-input user_input" style="text-align: end;">TX / 77056</span>
                                <!-- <span class="text-input user_input" style="text-align: end;">77056</span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>City</span>
                                <span>State / zip</span>
                                <!-- <span>Zip</span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input">Houston</span>
                                <span class="text-input user_input" style="text-align: end;">TX / 78109</span>
                                <!-- <span class="text-input user_input" style="text-align: end;">77056</span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>City</span>
                                <span>State / zip</span>
                                <!-- <span>Zip</span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span></span>
                                <span></span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Selling Associate's Name</span>
                                <span>License No.</span>
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span>Selling Associate's Name</span>
                                <span>License No.</span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input"></span>
                                <!-- <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Team Name</span>
                                <!-- <span>License No.</span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span>Selling Associate's Email Address</span>
                                <span>Phone</span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Selling Associate's Email Address</span>
                                <span>Phone</span>
                            </div>
                        </div>






                        <div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span>Selling Associate's Email Address</span>
                                <span>Phone</span> -->
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Licensed Supervisor of Selling Associate</span>
                                <span>License No.</span>
                            </div>
                        </div>


                        <div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span>Selling Associate's Email Address</span>
                                <span>Phone</span> -->
                            </div>
                        </div>

                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input"></span>
                                <!-- <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>Selling Associate's Office Address</span>
                                <!-- <span>License No.</span> -->
                            </div>
                        </div>




                        <div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span> -->
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <!-- <span>Selling Associate's Email Address</span>
                                <span>Phone</span> -->
                            </div>
                        </div>




                        <div>
                            <div class="col-header" id="buyer-heading">
                                <span class="text-input user_input"></span>
                                <span class="text-input user_input" style="text-align: end;"></span>
                            </div>
                            <div class="col-header" id="buyer-heading">
                                <span>City</span>
                                <span>State / Zip</span>
                            </div>
                        </div>


                    </div>
                    </div>
                        <div>
                            Disclosure: Pursuant to a previous, separate agreement, Listing Broker has agreed to pay Other
                            Broker a fee(☐ $________ or ☐ <span class="user_input text-input">3.00%</span>of the Sales
                            Price). This disclosure is for informational purposes and does not
                            change the previous agreement between brokers to pay or share a commission.

                        </div>


            </div>
        </div>


        </div>

    </body>

    </html>
        """

    # Replace placeholder with current date
    from datetime import datetime
    current_date = datetime.now().strftime("%B %d, %Y")
    html_content = html_content.replace("[Date]", current_date)

    # Launch Playwright and generate PDF
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Set the HTML content
        page.set_content(html_content)
        
        # Generate PDF
        page.pdf(
            path="page1.pdf",
            format="A4",
            display_header_footer=False,
            margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
            print_background=True
        )
        
        browser.close()
    
    print(f"Contract PDF with logo created successfully: contract_with_logo.pdf")


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        # Get property data from request
        property_data = request.get_json()
        if not property_data:
            return jsonify({'status': 'error', 'message': 'No property data received'}), 400

        # Generate a unique document ID
        document_id = str(uuid.uuid4())[:8].upper()
        print("this is the document id == " , document_id)
        property_data["document_id"] = document_id
        print("this is the property data == = " , property_data)

        # Generate PDF using the new class
        pdf_generator = RealEstateContractGenerator(property_data)

        # Instead of saving to disk, write PDF into memory
        pdf_buffer = BytesIO()
        pdf_generator.generate_pdf(pdf_buffer)
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()

        # Convert to base64 for frontend
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

        filename = f"Property_Agreement_{property_data.get('address','Property').replace(' ', '_').replace(',', '')}.pdf"

        return jsonify({
            'status': 'success',
            'message': 'PDF generated successfully',
            'pdf': pdf_base64,
            'filename': filename
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



import math



@app.route("/generate-pdf-page")
def generate_pdf_page():
    try:
        # Get query parameters for initial page load
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Get filtered and paginated data
        properties, total_count = get_filtered_properties(
            collection_name="properties",
            search=search,
            page=page,
            per_page=per_page
        )
        
        # Calculate total pages
        total_pages = math.ceil(total_count / per_page) if per_page > 0 else 1
        
        return render_template(
            "generate_pdf.html", 
            properties=properties,
            current_page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_count=total_count,
            search=search
        )
    except Exception as e:
        return render_template("error.html", error=str(e))