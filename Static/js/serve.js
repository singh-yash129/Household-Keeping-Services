
function addPincode(event) {
    if (event.key === "Enter") {
        event.preventDefault(); 

        const pincodeInput = document.getElementById("services-pincode");
        const pincodeValue = pincodeInput.value.trim();


        if (pincodeValue.length === 6 && !document.getElementById(pincodeValue)) {
            const pincodeList = document.getElementById("pincode-list");

        
            const pincodeItem = document.createElement("div");
            pincodeItem.classList.add("pincode-item");
            pincodeItem.id = pincodeValue;

            const pincodeText = document.createElement("span");
            pincodeText.textContent = pincodeValue;

            const removeIcon = document.createElement("span");
            removeIcon.classList.add("remove-pincode");
            removeIcon.innerHTML = "&times;";
            removeIcon.onclick = () => {
                pincodeItem.remove();
                updatePincodeInput(); 
            };

            pincodeItem.appendChild(pincodeText);
            pincodeItem.appendChild(removeIcon);
            pincodeList.appendChild(pincodeItem);

       
            updatePincodeInput();


            pincodeInput.value = "";
        } else {
            alert("Please enter a valid 6-digit pincode.");
        }
    }
}

function updatePincodeInput() {
    const pincodeItems = document.querySelectorAll("#pincode-list .pincode-item");
    const pincodes = Array.from(pincodeItems).map(item => item.id);
    document.getElementById("pincode-input").value = pincodes.join(','); 
}


function previewBrandLogo(event) {
    const preview = document.getElementById("brand-logo-preview");
    if (event.target.files[0]) {
        preview.src = URL.createObjectURL(event.target.files[0]);
        preview.style.display = "block";
    } else {
        preview.style.display = "none";
        preview.src = ""; 
    }
}

function addWorkImagePreview(event) {
    const files = event.target.files;
    const previewContainer = document.getElementById("work-images-preview");

    Array.from(files).forEach((file) => {
        if (file) {
            const imgWrapper = document.createElement("div");
            imgWrapper.className = "img-wrapper";

            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.className = "work-image";

            const removeBtn = document.createElement("span");
            removeBtn.innerHTML = "&times;";
            removeBtn.className = "remove-btn";
            removeBtn.onclick = () => previewContainer.removeChild(imgWrapper);

            imgWrapper.appendChild(img);
            imgWrapper.appendChild(removeBtn);
            previewContainer.appendChild(imgWrapper);
        }
    });
}
