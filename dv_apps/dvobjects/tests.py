from django.test import TestCase
from dv_apps.dvobjects.models import DvObject

class DvObjectsTestCase(TestCase):

    fixtures = ['test_2016_0812.json']

    def setUp(self):
        pass
        #print ('count: ', MetadataSchema.objects.all().count())
        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    def test_01_todo(self):
        """Test to see if db created"""

        cnt = DvObject.objects.all().count()
        self.assertEqual(cnt, 2510)
        print 'num DvObjects', cnt
