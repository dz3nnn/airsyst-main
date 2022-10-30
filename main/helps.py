import re

from main.models import Option, OptionRelation, OptionValue, Equipment_Item


def get_options_for_equip(equips):
    """Get Options for equip list"""
    equip_ids = equips.values_list("pk", flat=True)
    options = OptionRelation.objects.filter(equipment__pk__in=equip_ids)
    return options


def get_options_by_relations(option_relations):
    relation_ids = option_relations.values_list("option__pk", flat=True)
    options_list = Option.objects.filter(pk__in=relation_ids).order_by("name")
    return options_list


def apply_filter_for_equip(request, equips):
    """Apply filters to Equipment QuerySet"""
    # brand_ids_from_req = get_brands_from_params_v2(request)

    # # Apply brands
    # if brand_ids_from_req:
    #     equips = equips.filter(brand__in=brand_ids_from_req)

    # Apply filters
    option_ids = get_numeric_parameters_from_request(request)
    for option_id in option_ids:
        option_values_string = request.GET.get(option_id)
        if option_values_string:

            equips_ids = equips.values_list("pk", flat=True)

            option_values_string = re.sub("[^0-9:,.]", "", option_values_string)

            option_model = Option.objects.filter(pk=option_id).first()

            if option_model.numerical:
                # param is 100:800
                big_min = -999999
                big_max = 999999
                if option_values_string[0] == ":":
                    option_values_string = str(big_min) + option_values_string
                if option_values_string[-1] == ":":
                    option_values_string = option_values_string + str(big_max)
                option_values = option_values_string.split(":")
                # Maybe check if option_values len > 1
                float_values = to_float(option_values)

                min_val = min(float_values, default=0)
                max_val = max(float_values, default=0)

                relations = OptionRelation.objects.filter(
                    equipment__pk__in=equips_ids, option__pk=option_id
                ).distinct()

                new_ids = []
                for rel in relations:
                    z = rel.option_value.name.replace(",", ".")
                    z_split = z.split("-")
                    if len(z_split) > 1:
                        for c in z_split:
                            if is_float(c):
                                z = float(c)
                                if z >= min_val and z <= max_val:
                                    new_ids.append(rel.pk)
                    elif is_float(z):
                        z = float(z)
                        if z >= min_val and z <= max_val:
                            new_ids.append(rel.pk)

                relations_ids = (
                    OptionRelation.objects.filter(
                        equipment__pk__in=equips_ids,
                        option__pk=option_id,
                        pk__in=new_ids,
                    )
                    .values_list("equipment__pk", flat=True)
                    .distinct()
                )
                equips = Equipment_Item.objects.filter(pk__in=relations_ids)
            else:
                # param is 1:2:3
                option_values_ids = option_values_string.split(":")
                option_values_ids_formatted = [
                    x.replace("/", "") for x in option_values_ids
                ]
                equips_ids_filter = OptionRelation.objects.filter(
                    equipment__pk__in=equips_ids,
                    option_value__pk__in=option_values_ids_formatted,
                    option__pk=option_id,
                ).values_list("equipment__pk", flat=True)
                equips = Equipment_Item.objects.filter(pk__in=equips_ids_filter)
    return equips


def get_numeric_parameters_from_request(request):
    params = []
    if request.GET:
        check = request.GET
        for t in check:
            if t.isnumeric():
                params.append(t)
    return params


def to_float(arr):
    result = []
    for t in arr:
        z = t.replace(",", ".")
        z_split = z.split("-")
        if len(z_split) > 1:
            for c in z_split:
                if is_float(c):
                    result.append(float(c))
        elif is_float(z):
            result.append(float(z))
    return result


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
