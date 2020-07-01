import os
import DIRECTORIES
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/create', methods=['GET', 'POST'])
def write_post():
    if request.method=="POST":
        values = request.form
        ret = create_post(values)
        if ret:
            return render_template('options.html')
    return render_template('post.html')


@app.route('/show/<value>', methods=['GET'])
def show(value):
    data = None

    if str(value) == "drafts":
        files = os.listdir(DIRECTORIES.DRAFTS_PATH)
        data = [x[3] for x in sorted([tuple(file[:10].split("-") + [file]) for file in files])]

    elif str(value) == "blog":
        pass
    elif str(value) == "journal":
        pass
    return render_template('show.html', data=data, value=value)

@app.route('/show/<value>/<filename>')
def view_post(value, filename):
    data = None
    if str(value) == "drafts":
        with open(DIRECTORIES.DRAFTS_PATH + "/" + filename) as f:
            data = f.read()
        data = data.replace("/\n/g", "<br /><br />")
    elif str(value) == "blog":
        pass
    elif str(value) == "journal":
        pass
    return render_template('viewpost.html', data=data)


def create_post(values):
    try:
        header = ["---"]

        month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        date = values['date'].split("-")

        header.append("date: '{} {} {} 15:00:00 GMT+0530 (India Standard Time)'".format(month_dict[int(date[1])], date[2], date[0]))
        header.append("title: '{}'".format(values['title']))
            
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
        fname = DIRECTORIES.POSTS_DIRECTORY + "/" + fname
        with open(fname, 'w') as f:
            f.write(data)

    except Exception as e:
        print("[?] Exception: {}".format(e))
        return False

    return True

if __name__=="__main__":
	app.run()


