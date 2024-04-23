from rest_framework.test import APISimpleTestCase, APIRequestFactory
from django.conf import settings
from django.core.management import call_command
from django.urls import reverse

from cantusdata.views.search_notation import SearchNotationView

from solr.core import SolrConnection  # type: ignore

TEST_MEI_FILES_PATH = "cantusdata/test/core/helpers/mei_processing/test_mei_files"


class NotationSearchViewTestCase(APISimpleTestCase):
    solr_conn = SolrConnection(settings.SOLR_TEST_SERVER)
    factory = APIRequestFactory()
    url = reverse("search-notation-view")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Indexes sample MEI files for manuscript 123723.
        """
        call_command(
            "index_manuscript_mei",
            "123723",
            "--min-ngram",
            "1",
            "--max-ngram",
            "5",
            "--mei-dir",
            TEST_MEI_FILES_PATH,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Flushes the Solr test index after tests are run.
        """
        call_command("index_manuscript_mei", "123723", "--flush-index")

    def test_get_request(self) -> None:
        """
        Test that a 200 response is returned for a valid GET request.
        """
        query_params = {
            "q": "punctum",
            "type": "neume_names",
            "manuscript": "123723",
        }
        response = self.client.get(self.url, query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["numFound"], 164)

    def test_missing_parameters(self) -> None:
        """
        Test that a 200 response is returned when the request is missing parameters
        with an empty results array.
        """
        complete_query_params = {
            "q": "punctum",
            "type": "neume_names",
            "manuscript": "123723",
        }
        for param in complete_query_params:
            with self.subTest(param=param):
                # Test that the response is empty when one of the parameters is missing
                test_query_params = complete_query_params.copy()
                test_query_params.pop(param)
                response = self.client.get(self.url, test_query_params)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["numFound"], 0)
                self.assertEqual(response.data["results"], [])

    def test_query_solr_method(self) -> None:
        """
        Test that the query_solr method returns the expected results.
        """
        view = SearchNotationView()
        with self.subTest("Test neume_names search"):
            _, num_found = view.query_solr("123723", "neume_names", "punctum")
            # Folios 001r and 001v have 164 puncta
            self.assertEqual(num_found, 164)
            results, num_found = view.query_solr(
                "123723", "neume_names", "punctum Torculus"
            )
            # Folios 001r and 001v have 2 punctum torculus sequences
            self.assertEqual(num_found, 2)
            expected_results = [
                {
                    "boxes": [
                        {
                            "p": "https://lib.is/IE9434868/iiif/2/FL9435887",
                            "f": "001v",
                            "w": 361,
                            "h": 99,
                            "x": 6036,
                            "y": 4267,
                        }
                    ],
                    "contour": ["r", "u", "d"],
                    "pnames": ["e", "e", "f", "e"],
                    "semitones": [0, 1, -1],
                    "neumes": ["punctum", "torculus"],
                },
                {
                    "boxes": [
                        {
                            "p": "https://lib.is/IE9434868/iiif/2/FL9435887",
                            "f": "001v",
                            "w": 678,
                            "h": 147,
                            "x": 3011,
                            "y": 5343,
                        }
                    ],
                    "contour": ["r", "u", "d"],
                    "pnames": ["a", "a", "c", "b"],
                    "semitones": [0, 3, -1],
                    "neumes": ["punctum", "torculus"],
                },
            ]
            self.assertEqual(results, expected_results)
        with self.subTest("Test pitch_names search"):
            _, num_found = view.query_solr("123723", "pitch_names", "f e d")
            # Folios 001r and 001v have 17 sequences of F E D
            self.assertEqual(num_found, 17)
            _, num_found = view.query_solr("123723", "pitch_names", "a B   c b")
            # Folios 001r and 001v have 3 sequences of A B C B
            self.assertEqual(num_found, 3)
        with self.subTest("Test contour search"):
            _, num_found = view.query_solr("123723", "contour", "u")
            # Folios 001r and 001v have 133 sequences of "up"
            self.assertEqual(num_found, 133)
            _, num_found = view.query_solr("123723", "contour", "r r R ")
            # Folios 001r and 001v have 1 sequence of "repeat, repeat, repear"
            self.assertEqual(num_found, 1)
