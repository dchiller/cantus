from unittest import TestCase
from os import path
import json
from typing import List
from cantusdata.settings import BASE_DIR
from cantusdata.helpers.mei_processing.mei_tokenizer import MEITokenizer, NgramDocument


TEST_MEI_FILE = path.join(
    BASE_DIR,
    "cantusdata",
    "test",
    "core",
    "helpers",
    "mei_processing",
    "test_mei_files",
    "123723",
    "CDN-Hsmu_M2149.L4_001r.mei",
)


def calculate_expected_total_ngrams(
    mei_file: str, min_ngram: int, max_ngram: int
) -> int:
    """
    Function to calculate the expected number of ngrams created
    from an MEI file. The function uses the "flattened_neumes" property
    of the MEITokenizer class, but does not use any functions
    of that class that create ngrams.

    The expected number of ngrams is calculated as follows:
    - The number of neume components in the MEI file is calculated
    and used to determine how many ngrams are created with min_ngram,
    min_ngram + 1, ..., max_ngram pitches.
    - There will be an additional ngram created for every sequence of
    min_ngram, min_ngram + 1, ..., or max_ngram neumes whose commulative
    number of pitches is greater than max_ngram. We add one to the count of
    expected ngrams for every such sequence.


    """
    tokenizer = MEITokenizer(mei_file, min_ngram, max_ngram)
    parsed_neumes = tokenizer.flattened_neumes
    num_neume_components = sum(
        len(neume["neume_components"]) for neume in parsed_neumes
    )
    # The number of ngrams of pitches for a given n is:
    # number of neume components - n + 1
    exp_num_ngrams = sum(
        max(0, num_neume_components - i + 1) for i in range(min_ngram, max_ngram + 1)
    )
    for i in range(min_ngram, max_ngram + 1):
        for j in range(len(parsed_neumes) - i + 1):
            if (
                sum(
                    len(neume["neume_components"]) for neume in parsed_neumes[j : j + i]
                )
                > max_ngram
            ):
                exp_num_ngrams += 1
    return exp_num_ngrams


def prepare_tokenizer_results(
    tokenizer: MEITokenizer,
) -> List[NgramDocument]:
    """
    This function prepares the results of a tokenizer for comparison
    with expected results by:
    - removing the unique ID from generated ngram documents
    - removing the "type" field from generated ngram documents
    """
    ngram_docs = tokenizer.create_ngram_documents()
    for doc in ngram_docs:
        doc.pop("id")
        doc.pop("type")
    return ngram_docs


class MEITokenizerTestCase(TestCase):

    def test_mei_tokenizer(self) -> None:
        tokenizer_1_2 = MEITokenizer(
            TEST_MEI_FILE,
            min_ngram=1,
            max_ngram=2,
        )
        ngram_docs_1_2 = prepare_tokenizer_results(tokenizer_1_2)
        tokenizer_2_3 = MEITokenizer(
            TEST_MEI_FILE,
            min_ngram=2,
            max_ngram=3,
        )
        ngram_docs_2_3 = prepare_tokenizer_results(tokenizer_2_3)
        tokenizer_3_5 = MEITokenizer(
            TEST_MEI_FILE,
            min_ngram=3,
            max_ngram=5,
        )
        ngram_docs_3_5 = prepare_tokenizer_results(tokenizer_3_5)
        with self.subTest("Total number of ngrams: 1- and 2-grams"):
            expected_num_ngrams_1_2 = calculate_expected_total_ngrams(
                TEST_MEI_FILE, 1, 2
            )
            self.assertEqual(len(ngram_docs_1_2), expected_num_ngrams_1_2)
        with self.subTest("Total number of ngrams: 2- and 3-grams"):
            expected_num_ngrams_2_3 = calculate_expected_total_ngrams(
                TEST_MEI_FILE, 2, 3
            )
            self.assertEqual(len(ngram_docs_2_3), expected_num_ngrams_2_3)
        with self.subTest("Total number of ngrams: 3- to 5-grams"):
            expected_num_ngrams_3_5 = calculate_expected_total_ngrams(
                TEST_MEI_FILE, 3, 5
            )
            self.assertEqual(len(ngram_docs_3_5), expected_num_ngrams_3_5)
        # First three neumes in test file:
        # <neume xml:id="neume-0000001734946468">
        #     <nc xml:id="nc-0000000895518447" facs="#zone-0000001993884372" oct="3" pname="d"/>
        # </neume>
        # <neume xml:id="neume-0000000001979919">
        #     <nc xml:id="nc-0000001973406668" facs="#zone-0000001466045923" oct="3" pname="d"/>
        #     <nc xml:id="nc-0000000472608670" facs="#zone-0000000528011450" oct="3" pname="c"/>
        # </neume>
        # <neume xml:id="m-10023faa-5a94-4eb8-adbf-378d19a7edaa">
        #     <nc xml:id="m-d6735a59-f657-4197-a004-c949253f9268" facs="#m-0306c35f-6624-477a-8f15-f2995401695a" oct="3" pname="f"/>
        # </neume>
        # Relevant zones for first three neumes:
        # <zone xml:id="zone-0000001993884372" ulx="2608" uly="2391" lrx="2678" lry="2440"/>
        # <zone xml:id="zone-0000001466045923" ulx="2725" uly="2391" lrx="2795" lry="2440"/>
        # <zone xml:id="zone-0000000528011450" ulx="2795" uly="2440" lrx="2865" lry="2489"/>
        # <zone xml:id="m-0306c35f-6624-477a-8f15-f2995401695a" ulx="3015" uly="2293" lrx="3085" lry="2342"/>
        # Last three neumes in test file:
        # <neume xml:id="m-fb4e81e1-f606-4888-aaa0-4170bd5bbf0e">
        #     <nc xml:id="m-62905ec7-7482-46fc-b018-da5787b8dc91" facs="#m-cedf6e10-16c6-4857-ac25-ff4799e73af2" oct="2" pname="d"/>
        #     <nc xml:id="m-ea486c9c-3aa8-4762-8225-22d0ad0af6e0" facs="#m-919045a2-520e-4d7b-aa2f-f82ccbc14cc5" oct="2" pname="c"/>
        # </neume>
        # <neume xml:id="neume-0000000529809002">
        #     <nc xml:id="nc-0000002078669346" facs="#zone-0000001705972533" oct="2" pname="e"/>
        # </neume>
        # <neume xml:id="neume-0000000342143339">
        #     <nc xml:id="nc-0000001398460892" facs="#zone-0000000187867615" oct="2" pname="d"/>
        # </neume>
        # Relevant zones for the last three neumes:
        # <zone xml:id="m-cedf6e10-16c6-4857-ac25-ff4799e73af2" ulx="4750" uly="7782" lrx="4822" lry="7833"/>
        # <zone xml:id="m-919045a2-520e-4d7b-aa2f-f82ccbc14cc5" ulx="4811" uly="7833" lrx="4883" lry="7884"/>
        # <zone xml:id="zone-0000001705972533" ulx="5033" uly="7731" lrx="5105" lry="7782"/>
        # <zone xml:id="zone-0000000187867615" ulx="5097" uly="7782" lrx="5169" lry="7833"/>
        with self.subTest("First 1-gram"):
            expected_1gram: NgramDocument = {
                "location_json": json.dumps(
                    [{"ulx": 2608, "uly": 2391, "width": 70, "height": 49}]
                ),
                "pitch_names": "d",
                "contour": "",
                "semitone_intervals": "",
                "neume_names": "punctum",
            }
            self.assertEqual(expected_1gram, ngram_docs_1_2[0])
        with self.subTest("Ngram of first 3 neumes"):
            expected_3gram: NgramDocument = {
                "location_json": json.dumps(
                    [{"ulx": 2608, "uly": 2293, "width": 477, "height": 196}]
                ),
                "neume_names": "punctum_clivis_punctum",
                "pitch_names": "d_d_c_f",
                "contour": "r_d_u",
                "semitone_intervals": "0_-2_5",
            }
            self.assertEqual(expected_3gram, ngram_docs_3_5[1])
            self.assertEqual(expected_3gram, ngram_docs_2_3[2])
        with self.subTest("Pitch 3-gram: second three pitches"):
            # This 3-gram is constructed from the second three
            # pitches of the sample above.
            pitch_3gram: NgramDocument = {
                "location_json": json.dumps(
                    [{"ulx": 2725, "uly": 2293, "width": 360, "height": 196}]
                ),
                "pitch_names": "d_c_f",
                "semitone_intervals": "-2_5",
                "contour": "d_u",
                "neume_names": "clivis_punctum",
            }
            self.assertEqual(
                pitch_3gram,
                ngram_docs_2_3[4],
            )
            self.assertEqual(
                pitch_3gram,
                ngram_docs_3_5[4],
            )
        with self.subTest("Pitch 3-gram: last three pitches"):
            # This 4-gram is constructed from the last three
            # pitches of the test document.
            pitch_3gram_1: NgramDocument = {
                "location_json": json.dumps(
                    [{"ulx": 4811, "uly": 7731, "width": 358, "height": 153}]
                ),
                "pitch_names": "c_e_d",
                "semitone_intervals": "4_-2",
                "contour": "u_d",
            }
            self.assertIn(
                pitch_3gram_1,
                ngram_docs_2_3,
            )
            self.assertIn(
                pitch_3gram_1,
                ngram_docs_3_5,
            )
        with self.subTest("Pitch 4-gram: last 4 pitches"):
            # This 4-gram is constructed from the last four
            # pitches of the test document.
            pitch_4gram: NgramDocument = {
                "location_json": json.dumps(
                    [{"ulx": 4750, "uly": 7731, "width": 419, "height": 153}]
                ),
                "pitch_names": "d_c_e_d",
                "semitone_intervals": "-2_4_-2",
                "contour": "d_u_d",
                "neume_names": "clivis_punctum_punctum",
            }
            self.assertIn(
                pitch_4gram,
                ngram_docs_3_5,
            )
