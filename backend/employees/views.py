import io, os, tempfile, zipfile
from django.http import HttpResponse
from docxtpl import DocxTemplate
from vanguard.settings import MEDIA_ROOT


def doc_test(request):
    doc = DocxTemplate(os.path.join(MEDIA_ROOT, "test.docx"))
    # ... your other code ...
    context = { 'title' : "NGLAZKOV one file" }
    doc.render(context)
    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object

    response = HttpResponse(doc_io.read())

    # Content-Disposition header makes a file downloadable
    response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response

def generate_zip(files):
    mem_zip = io.BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()

def doc_multiple_test(request):
    files = []

    for i in range(5):
      doc = DocxTemplate(os.path.join(MEDIA_ROOT, "test.docx"))
      # ... your other code ...
      context = { 'title' : "NGLAZKOV company - multiple " + str(i) + " tests"}
      doc.render(context)
      doc_io = io.BytesIO() # create a file-like object
      doc.save(doc_io) # save data to file-like object
      doc_io.seek(0) # go to the beginning of the file-like object
      files.append(("test"+str(i)+".docx", doc_io.getvalue()))

    full_zip_in_memory = generate_zip(files) 

    response = HttpResponse(full_zip_in_memory, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    return response