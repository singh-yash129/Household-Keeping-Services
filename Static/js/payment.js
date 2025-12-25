document.addEventListener('DOMContentLoaded', function () {
    const paymentMethods = document.querySelectorAll('input[name="payment-method"]');
    const paymentDetails = document.querySelectorAll('.payment-detail');

    paymentMethods.forEach(method => {
        method.addEventListener('change', function () {
     
            paymentDetails.forEach(detail => {
                detail.style.display = 'none';
            });

     
            const selectedMethod = document.querySelector(`.${method.value}-details`);
            if (selectedMethod) {
                selectedMethod.style.display = 'block';
            }
        });
    });

    const upiInput = document.getElementById('upi-id');
    const upiValidationMessage = document.getElementById('upi-validation-message');

    upiInput.addEventListener('input', function () {
        const upiPattern = /^[\w.-]+@[\w.-]+$/;
        if (upiPattern.test(upiInput.value)) {
            upiInput.classList.remove('invalid');
            upiInput.classList.add('valid');
            upiValidationMessage.style.display = 'none';
        } else {
            upiInput.classList.remove('valid');
            upiInput.classList.add('invalid');
            upiValidationMessage.style.display = 'block';
        }
    });
});
const expiryDateInput = document.getElementById('expiry-date');
            expiryDateInput.addEventListener('input', function (event) {
                let value = expiryDateInput.value;
                if (value.length === 2 && event.inputType !== 'deleteContentBackward') {
                    expiryDateInput.value = value + '/';
                }
            });

            $('#expiry-date').datepicker({
                changeMonth: true,
                changeYear: true,
                showButtonPanel: true,
                dateFormat: 'mm/yy',
                onClose: function(dateText, inst) { 
                    function isDonePressed(){
                        return ($('#ui-datepicker-div .ui-datepicker-close').html() == 'Done');
                    }
                    if (isDonePressed()){
                        var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
                        var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
                        $('#expiry-date').val($.datepicker.formatDate('mm/yy', new Date(year, month, 1)));
                    }
                }
            }).focus(function () {
                $('.ui-datepicker-calendar').hide();
                $('#ui-datepicker-div').position({
                    my: 'center top',
                    at: 'center bottom',
                    of: $(this)
                });
            });
   
