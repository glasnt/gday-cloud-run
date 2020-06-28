import httpx
import os
from flask import Flask, render_template, request

mate = Flask(__name__, static_url_path="/assets/", static_folder="static")

METADATA_URI = "http://metadata.google.internal/"


def query(q):
    r = httpx.get(METADATA_URI + q, headers={"Metadata-Flavor": "Google"})
    return r.text


@mate.route("/")
def main():

    print(request.args)
    if "us-central1" in request.args:
        print("us-central1")
        fliptext = "australia-southeast1"
        flipcss = ""
    else:
        print("australia-east1")
        fliptext = "us-central1"
        with open("static/flip.css") as f:
            flipcss = f.read()
    flipbutton = f'<div class="cta fliptext"><a href="?{fliptext}">{fliptext.upper()} COMPAT MODE</a></div>'
    data = {}
    data["region"] = query("computeMetadata/v1/instance/region").split('/')[-1]
    data["service"] = os.environ.get("K_SERVICE", "Unknown")
    data["revision"] = os.environ.get("K_REVISION")
    return render_template(
        "base.html", data=data, flipbutton=flipbutton, flipcss=flipcss
    )


if __name__ == "__main__":
    print(main)
    mate.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
