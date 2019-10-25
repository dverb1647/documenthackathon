#!/usr/bin/env python3

from flask import Flask, jsonify, request, send_file
from PyPDF2 import PdfFileReader, PdfFileWriter
from docxtpl import DocxTemplate
from io import BytesIO
from os import remove
import json


app = Flask(__name__)


@app.route('/api/document/dummy')
def dummy():
    return jsonify({
        "success": True,
        "data": {}
    })

# request contains keys: doc-1, doc-2, ..., doc-n - which each
# contain PDF files for merge
@app.route('/api/document/merge', methods=['POST'])
def document_merge():
    writer = PdfFileWriter()    
    for key in sorted(request.files.keys()):
        reader = PdfFileReader(request.files[key])
        for p in range(reader.getNumPages()):
            writer.addPage(reader.getPage(p))

    tmp = BytesIO()
    writer.write(tmp)
    tmp.seek(0)

    return send_file(
        tmp,
        as_attachment=True,
        attachment_filename='merged.pdf'
    )

# request contains keys: context, document
# context - text field of JSON which contains template context
# template - template itself as `docx`
@app.route('/api/document/template', methods=['POST'])
def document_template():
    context_raw = request.form['context']
    document = request.files['document']

    context = json.loads(context_raw)

    template = DocxTemplate(document)
    template.render(context)

    try:
        try:
            remove('template.docx')
        except:
            pass
        template.save('template.docx')
        return send_file(
            './template.docx',
            as_attachment=True,
            attachment_filename='template.docx'
        )
    except FileNotFoundError:
        try:
            remove('/server/template.docx')
        except:
            pass
        template.save('/server/template.docx')
        return send_file(
            './template.docx',
            as_attachment=True,
            attachment_filename='template.docx'
        )

if __name__ == '__main__':
    app.run(debug=True)
