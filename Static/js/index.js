
function myMode() {
    var element = document.body;
    var x = document.getElementById("mode");
    var y = document.getElementById("dot");

    element.classList.toggle("darkmode");
    if (element.classList.contains("darkmode")) {
        x.innerHTML = "light_mode";
        y.innerHTML='Light Mode'
        x.style.color='orange'
        y.style.color='orange'
    
    } else {
        x.innerHTML = "dark_mode";
        y.innerHTML = "Dark Mode"
        x.style.color='black';
        y.style.color='black'
    }
}

const fileInputs = document.querySelectorAll('.custom-file-upload input[type="file"]');


fileInputs.forEach(input => {
    input.addEventListener('change', function () {
        const fileName = this.files[0]?.name || 'No file selected';
        const container = this.parentElement; 
        const placeholder = container.querySelector('span:nth-child(2)');
        if (this.files.length > 0) {
         
            container.style.backgroundColor = '#d4edda'; 
            container.style.borderColor = '#28a745'; 
            placeholder.textContent = fileName;
        } else {
            
            container.style.backgroundColor = '#f9f9f9'; 
            container.style.borderColor = '#ddd'; 
            placeholder.textContent = 'No file selected';
        }
    });
});

function openDeactivateForm() {
    document.getElementById("deactivateForm").style.display = "block";
}

function closeDeactivateForm() {
    document.getElementById("deactivateForm").style.display = "none";
}
function openVerifyForm() {
    document.getElementById("verifyForm").style.display = "block";
}

function closeVerifyForm() {
    document.getElementById("verifyForm").style.display = "none";
    
}



function openForm() {
    document.getElementById("updateProfileForm").style.display = "block";
}

function closeForm() {
    document.getElementById("updateProfileForm").style.display = "none";
}

function toggleNotifications() {
    const notiPanel = document.getElementById('myNoti');
    notiPanel.style.display = notiPanel.style.display === 'none' || !notiPanel.style.display ? 'block' : 'none';
}


document.querySelector('.cls').addEventListener('click', function () {
    document.getElementById('myNoti').style.display = 'none';
});



document.addEventListener("DOMContentLoaded", function() {
    var closeIcon = document.querySelector(".cls");
    closeIcon.addEventListener("click", function() {
        document.getElementById("myNoti").style.display = "none";
    });
});

function mySettings() {
    var x = document.getElementById("set");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
document.addEventListener("DOMContentLoaded", function() {
    var closeIcon = document.querySelector(".cls2");
    closeIcon.addEventListener("click", function() {
        document.getElementById("set").style.display = "none";
    });
});

function myChange() {
    var x = document.getElementById("change_password");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
document.addEventListener("DOMContentLoaded", function() {
    var closeIcon = document.querySelector(".cls3");
    closeIcon.addEventListener("click", function() {
        document.getElementById("change_password").style.display = "none";
    });
});




function myDelete() {
    var x = document.getElementById("delete");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
document.addEventListener("DOMContentLoaded", function() {
    var closeIcon = document.querySelector(".cls4");
    closeIcon.addEventListener("click", function() {
        document.getElementById("delete").style.display = "none";
    });
});



document.addEventListener("DOMContentLoaded", function() {
    const checkbox = document.querySelector('#visibility-checkbox');
    const visibilityInput = document.querySelector('#visibility-input');
    const form = document.querySelector('#visibility-form');

    checkbox.addEventListener('change', function() {
        visibilityInput.value = checkbox.checked ? 'on' : 'off';
        form.submit();
    });
});
 function toggleDropdown(id) { 
    var element = document.getElementById(id);
    if (element.classList.contains('show')) { 
        element.classList.remove('show'); } 
        else { element.classList.add('show'); }
     }
