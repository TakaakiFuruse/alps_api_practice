from flask import jsonify, render_template, abort, Response
from flask.blueprints import Blueprint
import json

doc_pages = Blueprint("doc_page", __name__, template_folder="doc")


@doc_pages.route("/documents")
def documents_route():
    return render_template(f"index.html")


@doc_pages.route("/docs/<string:filename>")
def documents_resources(filename):
    return render_template(f"docs/{filename}")


@doc_pages.route("/<string:filename>")
def documents_route_resources(filename):
    if filename.endswith("svg"):
        return render_template(f"alps-blog.svg")
    elif filename.endswith("alps-blog.json"):
        return render_template(f"alps-blog.json")
    elif filename.endswith("index.html"):
        return render_template(f"index.html")
    else:
        abort(404)
