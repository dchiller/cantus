from rest_framework.test import APITransactionTestCase
from rest_framework import status


class FolioChantSetViewTestCase(APITransactionTestCase):
    fixtures = ["2_initial_data"]

    def test_get(self):
        response = self.client.get("/chant-set/folio/1/")
        # Test that we get a response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that it's the response we're expecting
        expected_string = (
            '[{"office": "", "sequence": 72, "item_id": "1",'
            ' "differentia": "", "marginalia": "",'
            ' "cantus_id": "1234",'
            ' "folio": "123", "manuscript": "ABC - 456",'
            ' "folio_id": 1, "type": "cantusdata_chant",'
            ' "manuscript_name_hidden": "geoff",'
            ' "incipit": "5678", "volpiano": "",'
            ' "genre": "", "manuscript_id": 3, "full_text": "",'
            ' "feast": "", "mode": "", "finalis": "",'
            ' "position": ""}]'
        )
        self.assertJSONEqual(response.content, expected_string)


class ManuscriptChantSetTestCase(APITransactionTestCase):
    fixtures = ["2_initial_data"]

    def test_get(self):
        response = self.client.get("/chant-set/manuscript/3/")
        # Test that we get a response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that it's the response we're expecting
        expected_string = (
            '[{"office": "", "sequence": 72, "item_id": "1",'
            ' "differentia": "", "marginalia": "",'
            ' "cantus_id": "1234",'
            ' "folio": "123", "manuscript": "ABC - 456",'
            ' "folio_id": 1,'
            ' "type": "cantusdata_chant",'
            ' "manuscript_name_hidden": "geoff",'
            ' "incipit": "5678", "volpiano": "",'
            ' "genre": "", "manuscript_id": 3, "full_text": "",'
            ' "feast": "", "mode": "", "finalis": "",'
            ' "position": ""}]'
        )
        self.assertJSONEqual(response.content, expected_string)

    def test_get_empty_chant(self):
        response = self.client.get("/chant-set/manuscript/3/page-2/")
        # Test that we get a response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Empty response is just square brackets
        self.assertJSONEqual(response.content, "[]")
