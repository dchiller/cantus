import json
from operator import itemgetter
from typing import Any, Tuple, List, Dict, Literal, cast, TypedDict
from typing_extensions import NotRequired

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.request import Request

from solr.core import SolrConnection  # type: ignore
import solr.core  # type: ignore


class NotationException(APIException):
    status_code = 400
    default_detail = "Notation search request invalid"


# TODO: Implement pitch_names_invariant, text, interval, and incipit
# search types
SearchType = Literal["neume_names", "pitch_names", "contour"]


class ResultBox(TypedDict):
    """
    A dictionary representing a box on the image
    that contains a search result. This format is
    required by the DivaView front-end.

    p: the image URI
    f: the folio
    w: the width of the box
    h: the height of the box
    x: the left-most x-coordinate of the box
    y: the top-most y-coordinate of the box
    """

    p: str
    f: str
    w: int
    h: int
    x: int
    y: int


class SearchResult(TypedDict):
    """
    A dictionary representing a search result.
    This format is required by the DivaView front-end.

    boxes: a list of ResultBox dictionaries
    contour: the contour of the search result
    pnames: the pitch names of the search result
    semitone_intervals: the semitone intervals of the search result
    neumes: the neumes of the search result
    """

    boxes: List[ResultBox]
    contour: List[str]
    pnames: List[str]
    semitones: List[int]
    neumes: NotRequired[List[str]]


class SearchNotationView(APIView):
    """
    Search algorithm adapted from the Liber Usualis code
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Check that request includes required parameters. If it does, pass the query on
        to the query_solr method and return the results. If not, return a 200 reponse
        with empty results.

        Required parameters:
        - q: the search query
        - type: the type of search to perform
        - manuscript: the manuscript to search in
        """
        q = request.GET.get("q", None)
        search_type = request.GET.get("type", None)
        manuscript = request.GET.get("manuscript", None)

        if q and search_type and manuscript:
            if search_type not in ("neume_names", "pitch_names", "contour"):
                if search_type in ("pnames-invariant", "text", "interval", "incipit"):
                    raise NotationException("Search type not implemented")
                raise NotationException("Invalid search type")
            # MyPy doesn't recognize that we've already checked this
            search_type = cast(SearchType, search_type)
            results, num_found = self.query_solr(
                manuscript=manuscript, search_type=search_type, query=q
            )
        else:
            num_found = 0
            results = []

        return Response({"numFound": num_found, "results": results})

    def create_boxes(self, result_doc: Dict[str, Any]) -> List[ResultBox]:
        """
        Using a query result, create a list of boxes in the format
        required by the front-end DivaView to highlight the result
        location on the image.

        :param result_doc: the result document
        :return: a list of boxes (of type ResultBox)
        """
        boxes: List[ResultBox] = []
        locations = json.loads(result_doc["location_json"])

        for location in locations:
            boxes.append(
                {
                    "p": result_doc["image_uri"],
                    "f": result_doc["folio"],
                    "w": location["width"],
                    "h": location["height"],
                    "x": location["ulx"],
                    "y": location["uly"],
                }
            )

        return boxes

    def query_solr(
        self, manuscript: str, search_type: SearchType, query: str
    ) -> Tuple[List[SearchResult], int]:
        """
        Perform the query against the Solr server and return the results.

        :param manuscript: the manuscript to search in
        :param search_type: the type of search to perform
        :param query: the search query
        """
        solrconn = SolrConnection(settings.SOLR_SERVER)

        # This will be appended to the search query so that we only get
        # data from the manuscript that we want!
        manuscript_query = f"AND manuscript_id:{manuscript}"

        # Normalize case and replace whitespace with underscores
        query_stmt = "_".join(elem for elem in query.lower().split())

        response: solr.core.Response = solrconn.query(
            f"{search_type}:{query_stmt} {manuscript_query}",
            score=False,
            sort="folio asc",
            rows=100,
        )

        results = []

        for query_result in response:
            boxes = self.create_boxes(query_result)

            result: SearchResult = {
                "boxes": boxes,
                "contour": query_result["contour"].split("_"),
                "pnames": query_result["pitch_names"].split("_"),
                "semitones": [
                    int(x) for x in query_result["semitone_intervals"].split("_") if x
                ],
            }

            if search_type == "neume_names":
                result["neumes"] = query_result["neume_names"].split("_")

            results.append(result)

        sorting_keys = itemgetter("f", "y", "x")
        results.sort(key=lambda result: [sorting_keys(box) for box in result["boxes"]])

        return results, response.numFound
