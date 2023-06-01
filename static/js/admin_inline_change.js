// js for admin

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var c_data = 0; c_data < cookies.length; c_data++) {
            var cookie = cookies[c_data].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function() {
    var inlineGroup = document.querySelector('.inline-group');
    var currentUrl = window.location.href;
    var baseUrl = currentUrl.split('/admin')[0]

    inlineGroup.addEventListener('change', function(event) {
        var target = event.target;
        if (target.matches('select[name^="pricingplans"][name$="product_name"]')) {
            var selectedOption = target.value;
            var targetId = target.id.split('-')[1]
            // Construct the AJAX URL based on the current URL
            var ajaxUrl = baseUrl + '/update-inline/'
            fetch(ajaxUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ 'selectedOption': selectedOption })
            })
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Error occurred during the AJAX request.');
            })
            .then(function(data) {
                var newValue = data.newValue;
                // Set the field with the new value
                var field = document.querySelector('#id_pricingplans-'+ targetId +'-fee');
                field.value = newValue;
            })
            .catch(function(error) {
                console.error(error);
            });
        }
    });
});
