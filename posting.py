from flask import Flask, request, render_template

app = Flask(__name__)

_posts_dir_file_path = "/home/solanki/github/techcentaur.github.io/_posts/"

@app.route('/', methods=['GET', 'POST'])
def write_post():
    if request.method=="POST":
        values = request.form
        ret = create_post(values)
        if ret:
            return render_template('options.html')
    return render_template('post.html')


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
        fname = _posts_dir_file_path + fname
        with open(fname, 'w') as f:
            f.write(data)

    except Exception as e:
        print("[?] Exception: {}".format(e))
        return False

    return True

if __name__=="__main__":
	app.run()


