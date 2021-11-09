"""
https://flask.palletsprojects.com/en/2.0.x/patterns/packages/
Circular Imports
Every Python programmer hates them, and yet we just added some: circular imports
(That’s when two modules depend on each other. In this case views.py depends on __init__.py). Be advised that this is a
 bad idea in general but here it is actually fine. The reason for this is that we are not actually using the views
 in __init__.py and just ensuring the module is imported and we are doing that at the bottom of the file.

There are still some problems with that approach but if you want to use decorators there is no way around that.
Check out the Becoming Big section for some inspiration how to deal with that.
"""

from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

from src.http.v0 import * # noqa

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
