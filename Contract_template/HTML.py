# # # Requires: pip install weasyprint
# # from weasyprint import HTML

# # def create_html_based_pdf():
# #     html_content = """
# #     <!DOCTYPE html>
# #     <html>
# #     <head>
# #         <style>
# #             body { font-family: Arial, sans-serif; }
# #             h1 { color: darkblue; text-align: center; }
# #             table { width: 100%; border-collapse: collapse; }
# #             th, td { border: 1px solid black; padding: 8px; text-align: left; }
# #             th { background-color: #f2f2f2; }
# #             .footer { text-align: center; margin-top: 20px; }
# #         </style>
# #     </head>
# #     <body>
# #         <h1>PDF Created with WeasyPrint</h1>
# #         <p>This PDF was generated from HTML content.</p>
        
# #         <table>
# #             <tr>
# #                 <th>Product</th>
# #                 <th>Price</th>
# #                 <th>Quantity</th>
# #             </tr>
# #             <tr>
# #                 <td>Laptop</td>
# #                 <td>$999.99</td>
# #                 <td>10</td>
# #             </tr>
# #             <tr>
# #                 <td>Mouse</td>
# #                 <td>$19.99</td>
# #                 <td>25</td>
# #             </tr>
# #             <tr>
# #                 <td>Keyboard</td>
# #                 <td>$49.99</td>
# #                 <td>15</td>
# #             </tr>
# #         </table>
        
# #         <div class="footer">
# #             <p>Generated with Python and WeasyPrint</p>
# #         </div>
# #     </body>
# #     </html>
# #     """
    
# #     HTML(string=html_content).write_pdf("weasyprint_example.pdf")
# #     print("WeasyPrint PDF created successfully!")


# # create_html_based_pdf()


# # from playwright.sync_api import sync_playwright

# # html_content = "<h1>Hello Contract</h1><p>Generated with Playwright PDF export.</p>"

# # with sync_playwright() as p:
# #     browser = p.chromium.launch()
# #     page = browser.new_page()
# #     page.set_content(html_content)
# #     page.pdf(path="playwright_contract.pdf", format="A4")
# #     browser.close()
# # print("Playwright PDF created successfully!")



# from playwright.sync_api import sync_playwright

# html_content = """
# <!DOCTYPE html>
# <html>
# <head>
#     <style>
#         @page { size: A4; margin: 40px; }
#         body { font-family: Arial, sans-serif; color: #333; }
#         header { text-align: center; margin-bottom: 20px; }
#         header img { width: 150px; }
#         h1 { color: darkblue; margin: 10px 0; }
#         .summary {
#             background: #f0f6ff;
#             border: 1px solid #cce0ff;
#             padding: 10px;
#             border-radius: 6px;
#             margin-bottom: 20px;
#         }
#         table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
#         th, td { border: 1px solid #666; padding: 8px; text-align: left; }
#         th { background-color: #0b5394; color: #fff; }
#         .signatures { display: flex; justify-content: space-between; margin-top: 50px; }
#         .sig-block { width: 45%; text-align: center; }
#         .sig-line { margin-top: 60px; border-top: 1px solid #333; }
#         footer { text-align: center; font-size: 10pt; color: #777; margin-top: 50px; }
#     </style>
# </head>
# <body>
#     <header>
#         <img src="https://picsum.photos/seed/companylogo/400/150" alt="Company Logo">
#         <h1>Service Agreement</h1>
#     </header>

#     <div class="summary">
#         <p>This Service Agreement ("Agreement") is entered into between
#         <strong>Acme Co.</strong> ("Provider") and <strong>Beta LLC</strong> ("Client"), 
#         effective as of <strong>September 8, 2025</strong>.</p>
#     </div>

#     <table>
#         <tr><th>Term</th><th>Details</th></tr>
#         <tr><td>Services</td><td>Managed hosting and technical support</td></tr>
#         <tr><td>Fees</td><td>USD 12,000 annually, payable monthly</td></tr>
#         <tr><td>Duration</td><td>12 months from Effective Date</td></tr>
#         <tr><td>Termination</td><td>30 days written notice by either party</td></tr>
#     </table>

#     <div class="signatures">
#         <div class="sig-block">
#             <div class="sig-line"></div>
#             <p>Authorized Signature (Acme Co.)</p>
#         </div>
#         <div class="sig-block">
#             <div class="sig-line"></div>
#             <p>Authorized Signature (Beta LLC)</p>
#         </div>
#     </div>

#     <footer>
#         Acme Co. • 123 Business Road • City, Country • www.example.com
#     </footer>
# </body>
# </html>
# """

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.set_content(html_content)
#     page.pdf(path="contract_playwright.pdf", format="A4")
#     browser.close()
# print("Contract PDF created successfully!")










from playwright.sync_api import sync_playwright
import os

def create_contract_pdf():
    # HTML content for the contract
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0;
                padding: 0;
                color: #333;
                line-height: 1.6;
            }
            .container {
                width: 90%;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #1E5B94;
                padding-bottom: 20px;
            }
            .logo-placeholder {
                width: 200px;
                height: 80px;
                background-color: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                border: 1px dashed #ccc;
                color: #666;
                font-style: italic;
            }
            .company-info {
                text-align: right;
            }
            .contract-title {
                text-align: center;
                color: #1E5B94;
                margin: 30px 0;
                font-size: 24px;
                font-weight: bold;
            }
            .contract-content {
                margin: 20px 0;
            }
            .clause {
                margin-bottom: 15px;
            }
            .clause-title {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .signature-section {
                margin-top: 60px;
                display: flex;
                justify-content: space-between;
            }
            .signature-box {
                width: 45%;
                border-top: 1px solid #333;
                padding-top: 10px;
                margin-top: 60px;
            }
            .signature-label {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .date-label {
                margin-top: 20px;
            }
            .footer {
                margin-top: 50px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }
            .highlight {
                background-color: #fff9e6;
                padding: 15px;
                border-left: 4px solid #ffcc00;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo-placeholder">Company Logo</div>
                <div class="company-info">
                    <div>Company Name</div>
                    <div>123 Business Street</div>
                    <div>City, State 12345</div>
                    <div>Phone: (123) 456-7890</div>
                </div>
            </div>
            
            <div class="contract-title">SERVICE AGREEMENT CONTRACT</div>
            
            <div class="contract-content">
                <div class="clause">
                    <div class="clause-title">1. PARTIES</div>
                    <div>This Agreement is made between <strong>Company Name</strong> ("Service Provider") and <strong>Client Name</strong> ("Client").</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">2. SERVICES</div>
                    <div>The Service Provider agrees to provide the following services: [Description of services to be provided].</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">3. TERM</div>
                    <div>This Agreement shall commence on [Start Date] and shall continue until [End Date] unless terminated earlier in accordance with this Agreement.</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">4. COMPENSATION</div>
                    <div>Client agrees to pay Service Provider the amount of [Amount] for the services rendered, payable as follows: [Payment terms].</div>
                </div>
                
                <div class="highlight">
                    <strong>Important:</strong> This is a legally binding contract. Please read it carefully before signing.
                </div>
                
                <div class="clause">
                    <div class="clause-title">5. CONFIDENTIALITY</div>
                    <div>Both parties agree to maintain the confidentiality of any proprietary information received from the other party.</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">6. GOVERNING LAW</div>
                    <div>This Agreement shall be governed by and construed in accordance with the laws of [State/Country].</div>
                </div>
            </div>
            
            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-label">Service Provider Signature</div>
                    <div class="date-label">Date: ________________________</div>
                </div>
                
                <div class="signature-box">
                    <div class="signature-label">Client Signature</div>
                    <div class="date-label">Date: ________________________</div>
                </div>
            </div>
            
            <div class="footer">
                <p>This document constitutes the entire agreement between the parties and supersedes all prior discussions, negotiations, and agreements.</p>
                <p>Generated on [Date]</p>
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
            path="professional_contract.pdf",
            format="A4",
            display_header_footer=False,
            margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
            print_background=True
        )
        
        browser.close()
    
    print("Professional contract PDF created successfully: professional_contract.pdf")

# If you want to add a real logo, use this version
def create_contract_with_logo(logo_path):
    # Read the logo and convert to base64
    import base64
    
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode('utf-8')
            logo_html = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 80px;">'
    else:
        logo_html = '<div class="logo-placeholder">Company Logo</div>'
    
    # HTML content with logo placeholder
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 0;
                padding: 0;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                width: 90%;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #1E5B94;
                padding-bottom: 20px;
            }}
            .logo-placeholder {{
                width: 200px;
                height: 80px;
                background-color: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                border: 1px dashed #ccc;
                color: #666;
                font-style: italic;
            }}
            .company-info {{
                text-align: right;
            }}
            .contract-title {{
                text-align: center;
                color: #1E5B94;
                margin: 30px 0;
                font-size: 24px;
                font-weight: bold;
            }}
            .contract-content {{
                margin: 20px 0;
            }}
            .clause {{
                margin-bottom: 15px;
            }}
            .clause-title {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .signature-section {{
                margin-top: 60px;
                display: flex;
                justify-content: space-between;
            }}
            .signature-box {{
                width: 45%;
                border-top: 1px solid #333;
                padding-top: 10px;
                margin-top: 60px;
            }}
            .signature-label {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .date-label {{
                margin-top: 20px;
            }}
            .footer {{
                margin-top: 50px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
            .highlight {{
                background-color: #fff9e6;
                padding: 15px;
                border-left: 4px solid #ffcc00;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                {logo_html}
                <div class="company-info">
                    <div>Company Name</div>
                    <div>123 Business Street</div>
                    <div>City, State 12345</div>
                    <div>Phone: (123) 456-7890</div>
                </div>
            </div>
            
            <div class="contract-title">SERVICE AGREEMENT CONTRACT</div>
            
            <div class="contract-content">
                <div class="clause">
                    <div class="clause-title">1. PARTIES</div>
                    <div>This Agreement is made between <strong>Company Name</strong> ("Service Provider") and <strong>Client Name</strong> ("Client").</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">2. SERVICES</div>
                    <div>The Service Provider agrees to provide the following services: [Description of services to be provided].</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">3. TERM</div>
                    <div>This Agreement shall commence on [Start Date] and shall continue until [End Date] unless terminated earlier in accordance with this Agreement.</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">4. COMPENSATION</div>
                    <div>Client agrees to pay Service Provider the amount of [Amount] for the services rendered, payable as follows: [Payment terms].</div>
                </div>
                
                <div class="highlight">
                    <strong>Important:</strong> This is a legally binding contract. Please read it carefully before signing.
                </div>
                
                <div class="clause">
                    <div class="clause-title">5. CONFIDENTIALITY</div>
                    <div>Both parties agree to maintain the confidentiality of any proprietary information received from the other party.</div>
                </div>
                
                <div class="clause">
                    <div class="clause-title">6. GOVERNING LAW</div>
                    <div>This Agreement shall be governed by and construed in accordance with the laws of [State/Country].</div>
                </div>
            </div>
            
            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-label">Service Provider Signature</div>
                    <div class="date-label">Date: ________________________</div>
                </div>
                
                <div class="signature-box">
                    <div class="signature-label">Client Signature</div>
                    <div class="date-label">Date: ________________________</div>
                </div>
            </div>
            
            <div class="footer">
                <p>This document constitutes the entire agreement between the parties and supersedes all prior discussions, negotiations, and agreements.</p>
                <p>Generated on [Date]</p>
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
            path="contract_with_logo.pdf",
            format="A4",
            display_header_footer=False,
            margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
            print_background=True
        )
        
        browser.close()
    
    print(f"Contract PDF with logo created successfully: contract_with_logo.pdf")

if __name__ == "__main__":
    # Create basic contract
    create_contract_pdf()
    
    # Create contract with logo (if you have a logo image)
    # Replace 'logo.png' with the path to your logo file
    create_contract_with_logo("logo.png")