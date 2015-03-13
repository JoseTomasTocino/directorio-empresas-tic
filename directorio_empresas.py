from flask import Flask
import urllib2
import re
from flask import json

app = Flask(__name__)


@app.route('/')
def hello_world():

    wiki_source_url = 'https://raw.githubusercontent.com/wiki/cadizdevelopers/directorio-empresas-tic/Listado-de-Empresas-TIC.md'

    response = urllib2.urlopen(wiki_source_url)
    html = unicode(response.read(), 'utf-8')

    # Regex for a single company block
    block_re = re.compile(r'^###(.*?)(\n\n|\Z)', re.M | re.S)

    # Regex for a block title
    header_re = re.compile(r'^###\s+(.*)', re.M | re.U)

    # Regex for a block field
    field_re = re.compile(r'^\*\s+(.*):\s+(.*)', re.M | re.U)

    companies = []

    for elem in block_re.finditer(html):

        # Get the content of the company
        block_content = elem.group(0)

        # The id holds the string in the title of the block
        company = { 'id': header_re.search(block_content).group(1) }

        # Each field is written directly
        for field in field_re.finditer(block_content):
            company[field.group(1)] = field.group(2)

        companies.append(company)

    # Build the response
    response = {
        "success": "success",
        "data": companies
    }

    return json.jsonify(response)


if __name__ == '__main__':
    app.run()
