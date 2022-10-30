from django.test import TestCase
from main.templatetags.main_extras import get_min_value_for_option
from main.models import Option, OptionRelation, OptionValue, Equipment_Item


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        opt_val = OptionValue.objects.create(name="100")
        opt = Option.objects.create(name="Мощность", numerical=True)
        eq = Equipment_Item.objects.create(
            name="Test Product", name_ru="Тестовый Товар"
        )
        OptionRelation.objects.create(option=opt, option_value=opt_val, equipment=eq)

    def test_get_min_value(self):
        min_val = get_min_value_for_option(1)
        self.assertEqual(min_val, 100)
