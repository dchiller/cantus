from unittest import TestCase
from os import path
from cantusdata.settings import BASE_DIR
from cantusdata.helpers.mei_processing.mei_parser import (
    MEIParser,
    get_contour_from_interval,
    get_semitones_between_neume_components,
    analyze_neume,
)
from cantusdata.helpers.mei_processing.mei_parsing_types import (
    NeumeComponentElementData,
    Zone,
    Syllable,
)


class MEIParserTestCase(TestCase):
    default_bounding_box: Zone = {"coordinates": (-1, -1, -1, -1), "rotate": 0.0}
    nc_elem_g3: NeumeComponentElementData = {
        "pname": "g",
        "octave": 3,
        "bounding_box": default_bounding_box,
    }
    nc_elem_d4: NeumeComponentElementData = {
        "pname": "d",
        "octave": 4,
        "bounding_box": default_bounding_box,
    }
    nc_elem_d3: NeumeComponentElementData = {
        "pname": "d",
        "octave": 3,
        "bounding_box": default_bounding_box,
    }
    nc_elem_b2: NeumeComponentElementData = {
        "pname": "b",
        "octave": 2,
        "bounding_box": default_bounding_box,
    }

    def test_mei_parser(self) -> None:
        parser = MEIParser(
            path.join(
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
        )
        zones = parser.zones
        syllables = parser.syllables
        with self.subTest("Test number of zones"):
            self.assertEqual(len(zones), 353)
        with self.subTest("Test number of syllables"):
            self.assertEqual(len(syllables), 115)
        with self.subTest("Test sample zone #1"):
            zone_key = "#m-69ee7af4-e831-41fd-9d22-c2e0433e0847"
            expected_zone = {
                "coordinates": (2430, 2674, 5315, 3018),
                "rotate": -0.937391,
            }
            self.assertIn(zone_key, zones)
            self.assertEqual(zones[zone_key], expected_zone)
        with self.subTest("Test sample zone #2"):
            zone_key = "#zone-0000001924311785"
            expected_zone = {
                "coordinates": (1913, 7127, 1983, 7176),
                "rotate": 0.0,
            }
            self.assertIn(zone_key, zones)
            self.assertEqual(zones[zone_key], expected_zone)
        with self.subTest("Test first syllable"):
            # First and second syllables:
            ## <syllable xml:id="syllable-0000001795831030">
            ##     <syl xml:id="syl-0000000707236922" facs="#zone-0000001663913937">Ec</syl>
            ##     <neume xml:id="neume-0000001734946468">
            ##         <nc xml:id="nc-0000000895518447" facs="#zone-0000001993884372" oct="3" pname="d"/>
            ##     </neume>
            ## </syllable>
            ## <syllable xml:id="syllable-0000001438713822">
            ##     <syl xml:id="syl-0000000470772630" facs="#zone-0000001748077003">ce</syl>
            ##     <neume xml:id="neume-0000000001979919">
            ##         <nc xml:id="nc-0000001973406668" facs="#zone-0000001466045923" oct="3" pname="d"/>
            ##         <nc xml:id="nc-0000000472608670" facs="#zone-0000000528011450" oct="3" pname="c"/>
            ##     </neume>
            ## </syllable>
            # Relevant zones (for first syllable and the single neume component in that syllable):
            ## <zone xml:id="zone-0000001663913937" ulx="2426" uly="2451" lrx="2639" lry="2651"/>
            ## <zone xml:id="zone-0000001993884372" ulx="2608" uly="2391" lrx="2678" lry="2440"/>
            expected_first_syllable: Syllable = {
                "text": {
                    "text": "Ec",
                    "bounding_box": {
                        "coordinates": (2426, 2451, 2639, 2651),
                        "rotate": 0.0,
                    },
                },
                "neumes": [
                    {
                        "neume_name": "punctum",
                        "neume_components": [
                            {
                                "pname": "d",
                                "octave": 3,
                                "bounding_box": {
                                    "coordinates": (2608, 2391, 2678, 2440),
                                    "rotate": 0.0,
                                },
                                "semitone_interval": 0,
                                "contour": "r",
                                "system": 1,
                            }
                        ],
                        "bounding_box": {
                            "coordinates": (2608, 2391, 2678, 2440),
                            "rotate": 0.0,
                        },
                        "system": 1,
                    }
                ],
            }
            self.assertEqual(syllables[0], expected_first_syllable)
        with self.subTest("Test last syllable"):
            # Last syllable:
            ## <syllable xml:id="syllable-0000000764470667">
            ##     <syl xml:id="syl-0000001280622314" facs="#zone-0000001691872419">gil</syl>
            ##     <neume xml:id="neume-0000000529809002">
            ##         <nc xml:id="nc-0000002078669346" facs="#zone-0000001705972533" oct="2" pname="e"/>
            ##     </neume>
            ##     <neume xml:id="neume-0000000342143339">
            ##         <nc xml:id="nc-0000001398460892" facs="#zone-0000000187867615" oct="2" pname="d"/>
            ##     </neume>
            ## </syllable>
            # Relevant zones (for last syllable and the two neume components in that syllable):
            ## <zone xml:id="zone-0000001691872419" ulx="4948" uly="7825" lrx="5272" lry="8082"/>
            ## <zone xml:id="zone-0000001705972533" ulx="5033" uly="7731" lrx="5105" lry="7782"/>
            ## <zone xml:id="zone-0000000187867615" ulx="5097" uly="7782" lrx="5169" lry="7833"/>
            expected_last_syllable: Syllable = {
                "text": {
                    "text": "gil",
                    "bounding_box": {
                        "coordinates": (4948, 7825, 5272, 8082),
                        "rotate": 0.0,
                    },
                },
                "neumes": [
                    {
                        "neume_name": "punctum",
                        "neume_components": [
                            {
                                "pname": "e",
                                "octave": 2,
                                "bounding_box": {
                                    "coordinates": (5033, 7731, 5105, 7782),
                                    "rotate": 0.0,
                                },
                                "semitone_interval": -2,
                                "contour": "d",
                                "system": 13,
                            }
                        ],
                        "bounding_box": {
                            "coordinates": (5033, 7731, 5105, 7782),
                            "rotate": 0.0,
                        },
                        "system": 13,
                    },
                    {
                        "neume_name": "punctum",
                        "neume_components": [
                            {
                                "pname": "d",
                                "octave": 2,
                                "bounding_box": {
                                    "coordinates": (5097, 7782, 5169, 7833),
                                    "rotate": 0.0,
                                },
                                "semitone_interval": None,
                                "contour": None,
                                "system": 13,
                            },
                        ],
                        "bounding_box": {
                            "coordinates": (5097, 7782, 5169, 7833),
                            "rotate": 0.0,
                        },
                        "system": 13,
                    },
                ],
            }
            self.assertEqual(syllables[-1], expected_last_syllable)

    def test_get_contour_from_interval(self) -> None:
        self.assertEqual(get_contour_from_interval(0), "r")
        self.assertEqual(get_contour_from_interval(1), "u")
        self.assertEqual(get_contour_from_interval(-3), "d")

    def test_get_semitones_between_neume_components(self) -> None:
        with self.subTest("Interval test: ascending P5"):
            self.assertEqual(
                get_semitones_between_neume_components(
                    self.nc_elem_g3, self.nc_elem_d4
                ),
                7,
            )
        with self.subTest("Interval test: descending P5"):
            self.assertEqual(
                get_semitones_between_neume_components(
                    self.nc_elem_d4, self.nc_elem_g3
                ),
                -7,
            )
        with self.subTest("Interval test: descending P4"):
            self.assertEqual(
                get_semitones_between_neume_components(
                    self.nc_elem_g3, self.nc_elem_d3
                ),
                -5,
            )
        with self.subTest("Interval test: descending m6"):
            self.assertEqual(
                get_semitones_between_neume_components(
                    self.nc_elem_g3, self.nc_elem_b2
                ),
                -8,
            )

    def test_analyze_neume(self) -> None:
        neume_components_1 = [self.nc_elem_d3, self.nc_elem_g3]
        neume_components_2 = [
            self.nc_elem_d3,
            self.nc_elem_g3,
            self.nc_elem_d3,
        ]
        neume_components_3 = [self.nc_elem_d4, self.nc_elem_g3]
        neume_components_4 = [
            self.nc_elem_b2,
            self.nc_elem_b2,
            self.nc_elem_b2,
        ]
        neume_components_5 = [self.nc_elem_d4]
        with self.subTest("Analyze Pes"):
            self.assertEqual(analyze_neume(neume_components_1), ("pes", [5], ["u"]))
        with self.subTest("Analyze Torculus"):
            self.assertEqual(
                analyze_neume(neume_components_2), ("torculus", [5, -5], ["u", "d"])
            )
        with self.subTest("Analyze Clivis"):
            self.assertEqual(analyze_neume(neume_components_3), ("clivis", [-7], ["d"]))
        with self.subTest("Analyze Tristropha"):
            self.assertEqual(
                analyze_neume(neume_components_4), ("tristopha", [0, 0], ["r", "r"])
            )
        with self.subTest("Analyze Punctum"):
            self.assertEqual(analyze_neume(neume_components_5), ("punctum", [], []))
