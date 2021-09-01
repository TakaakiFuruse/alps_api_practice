from flask import Flask, jsonify, request, abort
from werkzeug.utils import redirect
from docs import doc_pages
import pandas as pd
import datetime

app = Flask(__name__)

app.register_blueprint(doc_pages)
df = pd.read_csv("./data/BlogPosting.csv")


@app.route("/goBlogPosting", methods=["GET"])
def go_blogposting():
    id = int(request.args.get("id"))
    if request.method == "GET" and id:
        if id in df["id"]:
            blog_post = df[df["id"] == id].iloc[0, 0:]
            return jsonify(
                {
                    "$schema": "https://alps-io.github.io/schemas/alps.json",
                    "alps": {
                        "title": "Blog Post",
                        "descriptor": [
                            {
                                "id": str(blog_post["id"]),
                                "articleBody": str(blog_post["articleBody"]),
                                "dateCreated": str(blog_post["dateCreated"]),
                                "href": "/goBlog",
                            },
                        ],
                    },
                },
            )
        else:
            abort(404)
    else:
        abort(405)


@app.route("/doPost", methods=["POST"])
def do_post():
    article_body = request.args.get("articleBody")
    if article_body and request.method == "POST":
        time = str(datetime.datetime.now())
        new_id = df["id"].max() + 1
        new_post = pd.DataFrame(
            {"id": [new_id], "articleBody": [article_body], "dateCreated": time}
        )
        df.append(new_post).to_csv("./data/BlogPosting.csv", index=False)
        return redirect("/goBlog", code=302)
    else:
        abort(405)


@app.route("/goAbout")
def go_about():
    return jsonify(
        {
            "$schema": "https://alps-io.github.io/schemas/alps.json",
            "alps": {
                "title": "Blog Post List",
                "doc": {"value": "Here's my posts!"},
                "descriptor": [{"href": "/goBlog", "doc": "Here's my blog! Enjoy!!"}],
            },
        },
    )


@app.route("/goStart")
@app.route("/goBlog")
def go_blog():

    blog_posts = [
        {
            "id": "BlogPosting",
            "articleBody": row[1]["articleBody"],
            "dateCraeted": row[1]["dateCreated"],
            "href": f"/goBlogPosting&id={str(row[1]['id'])}",
        }
        for row in df.iterrows()
    ]

    blog_posts.append({"id": "goAbout", "type": "safe", "href": "/goAbout"})
    blog_posts.append({"id": "doPost", "type": "unsafe", "href": "/doPost"})

    return jsonify(
        {
            "$schema": "https://alps-io.github.io/schemas/alps.json",
            "alps": {
                "title": "Blog Post List",
                "doc": {"value": "Here's my posts!"},
                "descriptor": blog_posts,
            },
        }
    )


@app.route("/")
def home():
    res = {
        "$schema": "https://alps-io.github.io/schemas/alps.json",
        "alps": {
            "title": "Home",
            "doc": {"value": "welcome to my blog!!"},
            "descriptor": [{"id": "goBlog", "type": "safe", "href": "/goBlog"}],
        },
    }
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
