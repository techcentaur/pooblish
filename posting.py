import os
import DIRECTORIES
from datetime import datetime
from flask import Flask, request, render_template
from titlecase import titlecase
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/show/<value>', methods=['GET'])
def show(value):
    data = None
    value = value.strip()
    if value == "drafts":
        files = os.listdir(DIRECTORIES.DRAFTS_PATH)
        data = [x[3] for x in sorted([tuple(file[:10].split("-") + [file]) for file in files])]
    elif value == "blog":
        files = os.listdir(DIRECTORIES.POSTS_PATH)
        data = [x[3] for x in sorted([tuple(file[:10].split("-") + [file]) for file in files])]
    elif value == "journal":
        files = os.listdir(DIRECTORIES.POSTS_PATH)
        data = [x[3] for x in sorted([tuple(file[:10].split("-") + [file]) for file in files])]
    elif value == "staticpages":
        files = os.listdir(DIRECTORIES.STATIC_PAGES)

        if DIRECTORIES.INDEX_PAGE:
            indexpage = DIRECTORIES.INDEX_PAGE.split("/")[-1]
        files.append(indexpage)
        data = files

    return render_template('show.html', data=data, value=value)

@app.route('/migration/<value>/<filename>')
def migration(value, filename):
    value=value.strip()
    if str(value) == "drafts":
        subprocess.run(["mv", DIRECTORIES.DRAFTS_PATH + "/" + filename , DIRECTORIES.POSTS_PATH])
        return render_template('options.html', name="Migrated to Published Posts")
    else:
        subprocess.run(["mv", DIRECTORIES.POSTS_PATH + "/" + filename , DIRECTORIES.DRAFTS_PATH])
        return render_template('options.html', name="Migrated to Drafts")

@app.route('/delete/<value>/<filename>')
def delete_post(value, filename):
    value, filename = value.strip(), filename.strip()
    if str(value) == "drafts":
        subprocess.run(["rm", DIRECTORIES.DRAFTS_PATH + "/" + filename])
    else:
        subprocess.run(["rm", DIRECTORIES.POSTS_PATH + "/" + filename])

    return render_template('options.html', name="Post Deleted")

def strip_first_line(data):
    idx = data.index('\n')
    firstline = (data[:idx]).strip()
    data = firstline + data[idx:]
    return data

@app.route('/show/<value>/<filename>')
def view_post(value, filename):
    data = None
    value = value.strip()
    if value == "drafts":
        with open(DIRECTORIES.DRAFTS_PATH + filename) as f:
            data = f.read()
    elif value == "blog":
        with open(DIRECTORIES.POSTS_PATH + filename) as f:
            data = f.read()
    elif value == "journal":
        with open(DIRECTORIES.POSTS_PATH + filename) as f:
            data = f.read()
    elif value == "staticpages":
        if "index" in filename:
            with open(DIRECTORIES.INDEX_PAGE) as f:
                data = f.read()
        else:
            with open(DIRECTORIES.STATIC_PAGES + filename) as f:
                data = f.read()

    data = strip_first_line(data)
    return render_template('viewpost.html',
                    data="{}".format(data),
                    value=value,
                    filename=filename)

@app.route('/edit/<value>/<filename>', methods=['GET', 'POST'])
def edit_post(value, filename):
    if request.method == "GET":
        data = None
        value = value.strip()

        if value == "drafts":
            with open(DIRECTORIES.DRAFTS_PATH + filename) as f:
                data = f.read()
        elif value == "blog":
            with open(DIRECTORIES.POSTS_PATH + filename) as f:
                data = f.read()
        elif value == "journal":
            with open(DIRECTORIES.POSTS_PATH + filename) as f:
                data = f.read()
        elif value == "staticpages":
            if "index" in filename:
                with open(DIRECTORIES.INDEX_PAGE) as f:
                    data = f.read()
            else:
                with open(DIRECTORIES.STATIC_PAGES + filename) as f:
                    data = f.read()

        data = strip_first_line(data)
        return render_template('editpost.html', data=data, value=value)
    else:
        values = request.form
        data = strip_first_line(str(values['editarea']))

        if value == "drafts":
            with open(DIRECTORIES.DRAFTS_PATH + filename, 'w') as f:
                f.write(data)
        elif value == "blog":
            with open(DIRECTORIES.POSTS_PATH + filename, 'w') as f:
                f.write(data)
        elif value == "journal":
            with open(DIRECTORIES.POSTS_PATH + filename, 'w') as f:
                f.write(data)
        elif value == "staticpages":
            if "index" in filename:
                with open(DIRECTORIES.INDEX_PAGE, 'w') as f:
                    f.write(data)
            else:
                with open(DIRECTORIES.STATIC_PAGES + filename, 'w') as f:
                    f.write(data)

        edit_link = "/edit/{}/{}".format(value, filename)
        return render_template('options.html', name="Edited", edit_link=edit_link)
  
@app.route('/create', methods=['GET', 'POST'])
def write_post():
    if request.method=="POST":
        values = request.form
        ret = create_post(values)
        if ret:
            return render_template('options.html', name="Posted", edit_link="/")
    return render_template('post.html')

def create_post(values):
    header = ["---"]

    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    date = values['date'].split("-")

    today = datetime.now()
    header.append("date: '{} {} {} {}:00:00 GMT+0530 (India Standard Time)'".format(month_dict[int(date[1])], date[2], date[0], today.hour))

    header.append("title: '{}'".format(titlecase(values['title'])))

    if 'showcase' in values:
        header.append("showcase: true")
    else:
        header.append("showcase: false")

    if 'journal' in values:
        header.append("journal: true")
    else:
        header.append("journal: false")

    header.append("tags: ")
    tags = [x.strip() for x in values['tags'].split("*")]
    for t in tags:
        header.append("  - {}".format(t))
    header.append("---\n")

    header.append(values['content'])


    data = "\n".join(header)
    fname = values['date'] + "-" + "-".join([x.lower() for x in values['title'].split()])  + ".md"
    fname = DIRECTORIES.POSTS_PATH + "/" + fname
    with open(fname, 'w') as f:
        f.write(data)

    return True

if __name__=="__main__":
	app.run()


