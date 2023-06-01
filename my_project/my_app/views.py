import json
from django.http import JsonResponse

from my_project.my_app.models import VendorPricingPlan


def update_inline(request):
    """
    This function updates the inline form value with suggested fee
    as pricing plan updates in the dropdown.
    """
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        selected_option = payload.get('selectedOption')
        if selected_option:
            new_value = VendorPricingPlan.objects.filter(product_name=selected_option).first()
            if new_value:
                return JsonResponse({'newValue': new_value.suggested_fee})
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
        elif selected_option == '':
             return JsonResponse({'newValue': ''})
