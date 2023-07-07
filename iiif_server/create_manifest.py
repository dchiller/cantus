import json
import subprocess
import glob

manifest_metadata = {"@context": "http://iiif.io/api/presentation/2/context.json",
                     "@id": "https://10.121.210.43:8000/iiif/salzinnes-minisite/manifest",
                     "@type": "sc:Manifest",
                     "label": "Salzinnes Antiphonal",
                     "viewingDirection": "left-to-right",
                     "viewingHint": "paged",
                     "sequences": [
                         {"@context": "http://iiif.io/api/presentation/2/context.json",
                          "@id": "https://10.121.210.43:8000/iiif/salzinnes-minisite/sequence/normal",
                          "@type": "sc:Sequence",
                          "label": "Hosted Order",
                          "viewingDirection": "left-to-right",
                          "viewingHint": "paged",
                        }
                     ]
}

def create_canvas_item(canvas_name):
    canvas_id = canvas_name.split("-")[1]
    results = subprocess.check_output(["docker", "run","--rm","-v","/Users/dylanhillerbrand/documents/ddmal/salzinnes-images:/imgs",
                             "--entrypoint=identify", "dpokidov/imagemagick",
                             "/imgs/" + canvas_name + ".tiff"]).decode()
    results = results.split("\n")[0].split(" ")[2].split("x")
    width = int(results[0])
    height = int(results[1])
    canvas = {"@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": "https://10.121.210.43:8000/iiif/salzinnes-minisite/canvases/" + canvas_name,
              "@type": "sc:Canvas",
              "label": canvas_name,
              "height": height,
              "width": width,
            "images": [
                {"@id": "https://10.121.210.43:8000/iiif/salzinnes-minisite/annotation/" + canvas_name + "-image",
                 "@type": "oa:Annotation",
                 "motivation": "sc:painting",
                 "resource": {
                     "@id": "https://10.121.210.43:8000/iiif/2/" + canvas_name + ".tiff/full/max/0/default.jpg",
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "service": {
                            "@context": "http://iiif.io/api/image/2/context.json",
                            "@id": "https://10.121.210.43:8000/iiif/2/" + canvas_name + ".tiff",
                            "profile": "http://iiif.io/api/image/2/context.json"
                 }},
                 "on": "https://10.121.210.43:8000/iiif/salzinnes-minisite/canvases/" + canvas_name}
                ]
    }
    return canvas

if __name__ == "__main__":
    image_names = glob.glob("/Users/dylanhillerbrand/documents/ddmal/salzinnes-images/*.tiff")
    image_names = [x.split("/")[-1].split(".")[0] for x in image_names]
    canvas_list = []
    for image in image_names:
        canvas = create_canvas_item(image)
        canvas_list.append(canvas)
    manifest_metadata["sequences"][0]["canvases"] = canvas_list
    with open("salzinnes_minisite_manifest.json", "w") as f:
        json.dump(manifest_metadata, f, indent=2)
