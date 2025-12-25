const tabs = document.querySelectorAll('.tab');
const steps = document.querySelectorAll('.step');
const lines = document.querySelectorAll('.line');
const tabContents = document.querySelectorAll('.tab-content');
let currentStep = 0;


function switchTab(step) {
    tabs.forEach((tab, index) => {
        if (index === step) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    steps.forEach((stepElement, index) => {
        if (index <= step) {
            stepElement.classList.add('active');
        } else {
            stepElement.classList.remove('active');
        }
    });

    lines.forEach((line, index) => {
        if (index < step) {
            line.classList.add('active');
        } else {
            line.classList.remove('active');
        }
    });

    tabContents.forEach((content, index) => {
        if (index === step) {
            content.classList.add('active');
        } else {
            content.classList.remove('active');
        }
    });
}

document.querySelectorAll('#saveBtn').forEach((btn) => {
    btn.addEventListener('click', function() {
        if (currentStep < tabs.length - 1) {
            currentStep++;
            switchTab(currentStep);
        }
    });
});

tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
        currentStep = index;
        switchTab(currentStep);
    });
});

switchTab(currentStep);

function openForm() {
    document.getElementById("updateProfileForm").style.display = "block";
}

function closeForm() {
    document.getElementById("updateProfileForm").style.display = "none";
}

document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('input[name="service[]"]');
    const totalValueElement = document.getElementById('total-value');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateTotal);
    });

    function updateTotal() {
        let total = 0;
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                total += parseFloat(checkbox.getAttribute('data-price'));
            }
        });
        totalValueElement.textContent = total.toFixed(2); 
        document.getElementById('total-hidden').value = total.toFixed(2);
    }
});
