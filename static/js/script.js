document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const dropzone = document.getElementById('csvDropzone');
    
    // Show selected file name
    fileInput.addEventListener('change', function(e) {
        if (this.files.length) {
            fileName.textContent = `Selected file: ${this.files[0].name}`;
            fileName.className = 'text-success fw-bold';
        }
    });
    
    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropzone.classList.add('bg-light');
    }
    
    function unhighlight() {
        dropzone.classList.remove('bg-light');
    }
    
    dropzone.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        
        if (files.length) {
            fileName.textContent = `Selected file: ${files[0].name}`;
            fileName.className = 'text-success fw-bold';
        }
    }
    
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});



async function generatePDF(propertyId) {
    try {
        const response = await fetch('/generate-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                address: "123 Main St", 
                Lot: "45", 
                Block: "A", 
                Subdivision_Legal_Name: "Sunset Estates",
                Preferred_Title_Company: "ABC Title",
                Listing_Associate_Email_Address: "agent@example.com",
                broker_info: {
                    office_name: "Best Realty",
                    office_type: "Brokerage",
                    office_id: "BR123",
                    email: "broker@example.com",
                    website: "www.bestrealty.com",
                    phone: "555-1234",
                    street_address: "456 Market St",
                    city_state_zip: "Houston, TX 77001"
                }
            }) // <-- you must pass real property data here
        });

        const result = await response.json();

        if (result.status === 'success') {
            // Convert base64 back to Blob for download
            const pdfBlob = atob(result.pdf);
            const byteArray = new Uint8Array(pdfBlob.length);
            for (let i = 0; i < pdfBlob.length; i++) {
                byteArray[i] = pdfBlob.charCodeAt(i);
            }
            const blob = new Blob([byteArray], { type: 'application/pdf' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = result.filename;
            link.click();
        } else {
            alert("Error: " + result.message);
        }

    } catch (error) {
        console.error("Error generating PDF:", error);
    }
}


// function saveChanges() {
//     console.log("this is the save changes function")
//     const propertyId = document.getElementById('propertyId').value;
//     const formData = {
//         address: document.getElementById('address').value,
//         Lot: document.getElementById('lot').value,
//         Block: document.getElementById('block').value,
//         Subdivision_Legal_Name: document.getElementById('subdivision').value,
//         contry: document.getElementById('country').value,
//         Preferred_Title_Company: document.getElementById('titleCompany').value,
//         Listing_Associate_Email_Address: document.getElementById('email').value,
//         broker_info: {
//             office_name: document.getElementById('officeName').value,
//             office_type: document.getElementById('officeType').value,
//             office_id: document.getElementById('officeId').value,
//             email: document.getElementById('brokerEmail').value,
//             website: document.getElementById('website').value,
//             phone: document.getElementById('phone').value,
//             street_address: document.getElementById('streetAddress').value,
//             city_state_zip: document.getElementById('cityStateZip').value
//         }
//     };

//     // document.getElementById('loadingMessage').textContent = 'Saving Changes';
//     // $('#loadingModal').modal('show');

//     $.ajax({
//         url: '/api/update-property/' + propertyId,
//         type: 'PUT',
//         contentType: 'application/json',
//         data: JSON.stringify(formData),
//         success: function(response) {
//             $('#loadingModal').modal('hide');
//             if (response.status === 'success') {
//                 showAlert('Changes saved successfully!', 'success');
//                 // document.getElementById('loadingMessage').textContent = 'Saving Changes';
//                 // $('#loadingModal').modal('hidden');
//             } else {
//                 showAlert('Error saving changes: ' + response.message, 'danger');
//             }
//         },
//         error: function(xhr, status, error) {
//             $('#loadingModal').modal('hide');
//             showAlert('Error saving changes: ' + error, 'danger');
//         }
//     });
// }

// function saveAndDownload() {
//     const propertyId = document.getElementById('propertyId').value;
//     const formData = {
//         address: document.getElementById('address').value,
//         Lot: document.getElementById('lot').value,
//         Block: document.getElementById('block').value,
//         Subdivision_Legal_Name: document.getElementById('subdivision').value,
//         contry: document.getElementById('country').value,
//         Preferred_Title_Company: document.getElementById('titleCompany').value,
//         Listing_Associate_Email_Address: document.getElementById('email').value,
//         broker_info: {
//             office_name: document.getElementById('officeName').value,
//             office_type: document.getElementById('officeType').value,
//             office_id: document.getElementById('officeId').value,
//             email: document.getElementById('brokerEmail').value,
//             website: document.getElementById('website').value,
//             phone: document.getElementById('phone').value,
//             street_address: document.getElementById('streetAddress').value,
//             city_state_zip: document.getElementById('cityStateZip').value
//         }
//     };

//     // document.getElementById('loadingMessage').textContent = 'Saving Changes and Generating PDF';
//     // $('#loadingModal').modal('show');

//     $.ajax({
//         url: '/api/update-property/' + propertyId,
//         type: 'PUT',
//         contentType: 'application/json',
//         data: JSON.stringify(formData),
//         success: function(response) {
//             if (response.status === 'success') {
//                 generateAndDownloadPDF(propertyId, formData);
//                 // document.getElementById('loadingMessage').textContent = 'Saving Changes and Generating PDF';
//                 // $('#loadingModal').modal('hide');
//             } else {
//                 $('#loadingModal').modal('hide');
//                 showAlert('Error saving changes: ' + response.message, 'danger');
//             }
//         },
//         error: function(xhr, status, error) {
//             $('#loadingModal').modal('hide');
//             showAlert('Error saving changes: ' + error, 'danger');
//         }
//     });
// }

// function generateAndDownloadPDF(propertyId, propertyData) {
//     $.ajax({
//         url: '/generate-pdf',
//         type: 'POST',
//         contentType: 'application/json',
//         data: JSON.stringify({ ...propertyData, _id: propertyId }),
//         success: function(response) {
//             $('#loadingModal').modal('hide');
//             if (response.status === 'success') {
//                 const link = document.createElement('a');
//                 link.href = 'data:application/pdf;base64,' + response.pdf;
//                 link.download = response.filename;
//                 document.body.appendChild(link);
//                 link.click();
//                 document.body.removeChild(link);
//                 showAlert('PDF generated successfully!', 'success');
//             } else {
//                 showAlert('Error generating PDF: ' + response.message, 'danger');
//             }
//         },
//         error: function(xhr, status, error) {
//             $('#loadingModal').modal('hide');
//             showAlert('Error generating PDF: ' + error, 'danger');
//         }
//     });
// }


function saveChanges() {
    console.log("this is the save changes function")
    const propertyId = document.getElementById('propertyId').value;
    const formData = {
        address: document.getElementById('address').value,
        Lot: document.getElementById('lot').value,
        Block: document.getElementById('block').value,
        Subdivision_Legal_Name: document.getElementById('subdivision').value,
        contry: document.getElementById('country').value,
        Preferred_Title_Company: document.getElementById('titleCompany').value,
        Listing_Associate_Email_Address: document.getElementById('email').value,
        broker_info: {
            office_name: document.getElementById('officeName').value,
            office_type: document.getElementById('officeType').value,
            office_id: document.getElementById('officeId').value,
            email: document.getElementById('brokerEmail').value,
            website: document.getElementById('website').value,
            phone: document.getElementById('phone').value,
            street_address: document.getElementById('streetAddress').value,
            city_state_zip: document.getElementById('cityStateZip').value
        },
        admin_data: {
            sales_price: document.getElementById('salesPrice').value,
            earnest_money: document.getElementById('earnestMoney').value,
            option_fee: document.getElementById('optionFee').value,
            buyer_approval_deadline_days: document.getElementById('buyerApprovalDeadline').value,
            survey_delivery_deadline_days: document.getElementById('surveyDeliveryDeadline').value
        }
    };

    $.ajax({
        url: '/api/update-property/' + propertyId,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            if (response.status === 'success') {
                showAlert('Changes saved successfully!', 'success');
            } else {
                showAlert('Error saving changes: ' + response.message, 'danger');
            }
        },
        error: function(xhr, status, error) {
            showAlert('Error saving changes: ' + error, 'danger');
        }
    });
}

function saveAndDownload() {
    const propertyId = document.getElementById('propertyId').value;
    const formData = {
        address: document.getElementById('address').value,
        Lot: document.getElementById('lot').value,
        Block: document.getElementById('block').value,
        Subdivision_Legal_Name: document.getElementById('subdivision').value,
        contry: document.getElementById('country').value,
        Preferred_Title_Company: document.getElementById('titleCompany').value,
        Listing_Associate_Email_Address: document.getElementById('email').value,
        broker_info: {
            office_name: document.getElementById('officeName').value,
            office_type: document.getElementById('officeType').value,
            office_id: document.getElementById('officeId').value,
            email: document.getElementById('brokerEmail').value,
            website: document.getElementById('website').value,
            phone: document.getElementById('phone').value,
            street_address: document.getElementById('streetAddress').value,
            city_state_zip: document.getElementById('cityStateZip').value
        },
        admin_data: {
            sales_price: document.getElementById('salesPrice').value,
            earnest_money: document.getElementById('earnestMoney').value,
            option_fee: document.getElementById('optionFee').value,
            buyer_approval_deadline_days: document.getElementById('buyerApprovalDeadline').value,
            survey_delivery_deadline_days: document.getElementById('surveyDeliveryDeadline').value
        }
    };

    $.ajax({
        url: '/api/update-property/' + propertyId,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            if (response.status === 'success') {
                generateAndDownloadPDF(propertyId, formData);
            } else {
                showAlert('Error saving changes: ' + response.message, 'danger');
            }
        },
        error: function(xhr, status, error) {
            showAlert('Error saving changes: ' + error, 'danger');
        }
    });
}




function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);

    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// ✅ Only one document.ready
$(document).ready(function() {
    const saveBtn = document.getElementById("saveBtn");
    const saveBtnLarge = document.getElementById("saveBtnLarge");
    const saveDownloadBtn = document.getElementById("saveDownloadBtn");

    if (saveBtn) saveBtn.addEventListener("click", saveChanges);
    if (saveBtnLarge) saveBtnLarge.addEventListener("click", saveChanges);
    if (saveDownloadBtn) saveDownloadBtn.addEventListener("click", saveAndDownload);

    $('#propertyForm').on('submit', function(e) {
        e.preventDefault();
        saveChanges();
    });
});




// Delete button handler
$('.delete-item').on('click', function() {
    const id = $(this).data('id');
    if (confirm('Are you sure you want to delete this record?')) {
        $.ajax({
            url: '/api/delete-property/' + id,
            type: 'DELETE',
            success: function(response) {
                if (response.status === 'success') {
                    showAlert('Record deleted successfully!', 'success');
                    location.reload(); // reload table to reflect changes
                } else {
                    showAlert('Error: ' + response.message, 'danger');
                }
            },
            error: function(xhr, status, error) {
                showAlert('Error deleting record: ' + error, 'danger');
            }
        });
    }
});
