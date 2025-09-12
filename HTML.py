
from playwright.sync_api import sync_playwright
import os

# If you want to add a real logo, use this version
def create_contract_with_logo(logo_path):
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
            margin: 4px 0;
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
    </style>
</head>


<body>
    <div style="font-size: 10px;">
        Docusign Envelope ID: AA36957E-5678-43F3-B524-A4E6F66854708888888
    </div>
    <div class="container">
        <p style="text-align: end; margin-bottom: 5px;">11-04-2024</p>
        <div class="header">
            <img class="big_logo" src="static\images\main_logo.png" alt="TREC Logo">
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
            <img class="small_logo" src="static\images\small_logo.png" alt="TREC Logo">
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
                    LAND: Lot <span class="text-input user_input">36</span>, Block <span
                        class="text-input user_input">1</span><br>
                    <span class="text-input user_input">HEIGHTS OF WESTCREEK PH 1</span> Addition, City of <span
                        class="text-input user_input">San Antonio</span><br>
                    County of <span class="text-input user_input">Bexar</span>, Texas, known as <span
                        class="text-input user_input">1208 CREEK KNL TX 78253</span>
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
                    <span class="text-input user_input">$ 1,000.00</span> as earnest money and <span
                        class="text-input user_input">$ 1,00.00</span> as
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
                        class="text-input user_input">10</span>
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

if __name__ == "__main__":
    create_contract_with_logo("logo.png")