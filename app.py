import os
import logging
import json
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Analysis page test -- go to /test-analysis to see a premade analysis result
@app.route("/test-analysis")
def test_analysis():
    # Path to your premade JSON file
    json_path = os.path.join("analysis_results", "https___www.ebay.com_itm_335897458808_chn_ps_mkevt_1_mkcid_28_google_free_listing_action_view_item_srsltid_AfmBOor77SQepblzO9WF1_QxpnQ1QXSEOWnYgvQ1m5ik9Th2hrlMhd-9iLU_gQT_1.json")
    with open(json_path, "r") as f:
        analysis = json.load(f)
    test_url = "https://example.com/test-product"
    return render_template("analysis.html", analysis=analysis, url=test_url)

# Import and register routes
from routes import *


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

