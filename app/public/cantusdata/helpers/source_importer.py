from urllib import request
import json
from html.parser import HTMLParser


class ProvenanceParser(HTMLParser):
    """
    ProvenanceParser extracts the short provenance name from a CantusDB source
    page (/source/id-of-source/).

    provenance_div flags whether the parser has reached the div containing the
    provenance text.

    provenance_a flags whether the parser has reached the anchor tag that contains
    the provenance text.
    """

    def __init__(self):
        super().__init__()
        self.provenance_div = False
        self.provenance_a = False
        self.provenance = ""

    def handle_starttag(self, tag, attrs):
        """
        While parsing the html:
        1. determine whether a div tag encountered by the parser has the unique
        class attributes assigned to the div that contains provenance data. If
        this div is encountered, the provenance_div flag is set to True.
        2. if a anchor tag is encountered within this div tag, set the
        provenance_a flag to True.
        """
        if tag == "div":
            if ("class", "views-field views-field-field-provenance-tax") in attrs:
                self.provenance_div = True
        if tag == "a":
            if self.provenance_div:
                self.provenance_a = True

    def handle_endtag(self, tag):
        """
        Once provenance data has been extracted, set the flags to False
        """
        if self.provenance_a:
            self.provenance_div = False
            self.provenance_a = False

    def handle_data(self, data):
        """
        Extract the provenance data when provenance_a has been triggered.
        """
        if self.provenance_a:
            self.provenance = data


class SourceImporter:
    """
    Imports sources from CantusDB by way of its APIs.

    :param str cantus_db_base_url: the domain for CantusDB.
    """

    def __init__(self, cantus_db_base_url):
        self.cdb_base_url = cantus_db_base_url

    def request_source_ids(self):
        """
        Requests the IDs of all sources available in CantusDB

        :return: a list of character source ID's
        """
        sources_url = f"{self.cdb_base_url}/json-sources/"
        sources_response = request.urlopen(sources_url).read()
        sources_json = json.loads(sources_response)
        source_ids = sources_json.keys()
        return source_ids

    def download_source_data(self, source_id):
        """
        Requests data on an individual source in CantusDB using
        the /json-node/ endpoint.

        :param str source_id: the ID of the source in CantusDB
        :return: a parsed json object containing source data
        """
        source_url = f"{self.cdb_base_url}/json-node/{source_id}"
        source_response = request.urlopen(source_url).read()
        source_json = json.loads(source_response)
        return source_json

    def download_source_provenance(self, source_id):
        """
        The current Old CantusDB API endpoints do not provide
        a method for obtaining Provenance metadata (the text returned
        by the API in the provenance field contains more extensive notes
        on the source provenance, but not the shorter designation that is
        displayed publicly in CantusDB and on Cantus Ultimus). As such, this
        method extracts this source provenance from CantusDB html. Incorporating
        this into CantusDB's API is an open issue
        (see https://github.com/DDMAL/CantusDB/issues/564), so this will be
        simplified once that is complete.
        """
        source_pg_url = f"{self.cdb_base_url}/source/{source_id}"
        source_pg_response = request.urlopen(source_pg_url).read().decode()
        source_pg_html = ProvenanceParser()
        source_pg_html.feed(source_pg_response)
        return source_pg_html.provenance

    def extract_source_data(self, source_json):
        """
        Extracts required elements for the CU Manuscript
        model from the API response json.

        :param json source_json: parsed json response from json-node api
        :return: a dictionary of Manuscript attributes
        """
        source_dict = {}
        source_dict["id"] = source_json["vid"]
        source_dict["name"] = source_json["title"]
        if source_json["field_siglum"]:
            source_dict["siglum"] = source_json["field_siglum"]["und"][0]["value"]
        else:
            source_dict["siglum"] = ""
        if source_json["field_date"]:
            source_dict["date"] = source_json["field_date"]["und"][0]["value"]
        else:
            source_dict["date"] = ""
        ## See documentation of the download_source_provenance method for details
        ## on these commented lines.
        # if source_json["field_provenance"]:
        #     source_dict["provenance"] = source_json["field_provenance"]["und"][0]["value"]
        # else:
        #     source_dict["provenance"] = ""
        source_dict["provenance"] = self.download_source_provenance(source_dict["id"])
        if source_json["field_summary"]:
            source_dict["description"] = source_json["field_summary"]["und"][0]["value"]
        else:
            source_dict["description"] = ""
        return source_dict

    def get_source_data(self, source_id):
        """
        Given a source ID from CantusDB, returns a dictionary of
        source metadata required to create a Cantus Ultimus
        manuscript object.

        :param str source_id: the ID of the source in CantusDB
        :return: a dictionary of metadata for use in creating a
        Manuscript object in Cantus Ultimus
        """
        source_json = self.download_source_data(source_id)
        source_data = self.extract_source_data(source_json)
        return source_data