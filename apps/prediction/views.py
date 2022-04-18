import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .models import Category, Breed


def form(request):
    return HttpResponse(loader.get_template('form/form.html').render({'categories_list': Category.objects.all().order_by('category_order')}, request))


def result(request):
    if request.method != 'POST':
        print('Not post')
        return redirect('prediction:form')

    data = json.loads(request.POST['prediction_data'])

    character_breeds = []
    character_percentages = []
    for breed in data['Character']:
        percentage = float(data['Character'][breed]['Percentage'])

        if percentage < 70:
            continue

        character_breeds.append(Breed.objects.all().get(id=int(data['Character'][breed]['ID'])))
        character_percentages.append(percentage)

    image_breeds = []
    image_percentages = []
    for breed in data['Images']['Sum']:
        percentage = float(data['Images']['Sum'][breed])

        if percentage < 30:
            continue

        image_breeds.append(Breed.objects.all().get(id=int(breed)))
        image_percentages.append(percentage)

    context = {
        'is_not_predicted_image': data['Images']['Output']['AmountNotDog'] >= 1,
        'len_not_predicted_images': data['Images']['Output']['AmountNotDog'],
        'is_predicted_image': len(image_breeds) >= 1,
        'range_predicted_images': range(len(image_breeds)),
        'predicted_images': zip(image_breeds, image_percentages),
        'is_skipped_due_to_error': data['Images']['Output']['SkippedDueToError'] >= 1,
        'len_skipped_due_to_error': data['Images']['Output']['SkippedDueToError'],
        'is_predicted_breed': len(character_breeds) >= 1,
        'predicted_breeds': zip(character_breeds, character_percentages)
    }

    return HttpResponse(loader.get_template('result/result.html').render(context, request))
