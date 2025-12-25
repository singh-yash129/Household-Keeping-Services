    function toggleDetails(element) {
        const row = element.closest('tr');
      
        const detailsRow = row.nextElementSibling;

        if (detailsRow.style.display === 'none' || detailsRow.style.display === '') {
            detailsRow.style.display = 'table-row';
            element.innerText = 'arrow_drop_up'; 
        } else {
            detailsRow.style.display = 'none';
            element.innerText = 'arrow_drop_down'; 
        }
    }

