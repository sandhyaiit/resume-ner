from flask import Flask, render_template, request, redirect, url_for
import os
import spacy
import glob
from converter import convert_pdf_to_text
from converter import convert_docx_to_text

app = Flask(__name__)
nlp = spacy.load("./model")

def readFile(fileName):
    '''
    Read a file given its name as a string.
    Modules required: os
    UNIX packages required: antiword, ps2ascii
    '''
    extension = fileName.split(".")[-1]
    if extension == "txt":
        f = open(fileName, 'r')
        string = f.read()
        f.close()
        return string, extension
    elif extension == "docx":
        try:
            return convert_docx_to_text(fileName), extension
        except:
            return ''
            pass
    elif extension == "pdf":
        try:
            return convert_pdf_to_text(fileName), extension
        except:
            return ''
            pass
    else:
        print
        'Unsupported format'
        return '', ''

def parse_resume(base_path):
    # nlp = spacy.load("./model")
    f = base_path
    # # Glob module matches certain patterns
    # docx_files = glob.glob("resumes/*.docx")
    # pdf_files = glob.glob("resumes/*.pdf")
    # text_files = glob.glob("resumes/*.txt")

    # files = set(docx_files + pdf_files + text_files)
   # files = list(files)

    # for f in files:
        # info is a dictionary that stores all the data obtained from parsing
    info = {}
    print(f)
    inputString, info['extension'] = readFile(f)
    info['fileName'] = f

    doc_to_test = nlp(inputString)
    print([(ent.text, ent.label_) for ent in doc_to_test.ents])
    print('--------')

    entity_json={}
    for ent in doc_to_test.ents:
        if ent.label_ not in entity_json:
            entity_json[ent.label_] = []


        entity_json[ent.label_].append(ent.text)
    return entity_json


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    print("hit")
    if uploaded_file.filename != '':
        print("hit_2")
        uploaded_file.save(uploaded_file.filename)
        print(uploaded_file.filename)
    # return redirect(url_for('index'))
       # parse_resume(os.path.realpath(os.path.dirname(__file__))+uploaded_file.filename)
        a = parse_resume(os.path.join(os.path.realpath(os.path.dirname(__file__)),uploaded_file.filename))

    print(a)
    return render_template('resume.html', resume_info = a)

if __name__ == "__main__":
    app.run(debug=True)
# parse_resume("resumes\sample_input.pdf")
# from parse import Parse
# Parse()
