from flask import Flask, render_template, request, redirect
import csv
app = Flask(__name__)

# sajt22
# sajt333 

@app.route('/', methods=['GET', 'POST'])
def show_list():
    stories = read_data('database.csv')
    if request.method == "POST":
        return add_new_story()
    else:
        return render_template('list.html', stories=stories, title='Super Sprinter 3000')


@app.route('/story', methods=['POST'])
def add_new_story():
    return render_template('form.html', title='Add new Story', button='Create', story=['', '', '', '', '1000', '2.5', ''])

@app.route('/edit/<id>')
def edit(id):
    stories = read_data()
    for row in stories:
        if row[0] == id:
            story = row
    return render_template('form.html', title='Edit Story', button='Update', story=story, id=id)


@app.route('/list', methods=['POST'])
def update():
    stories = read_data('database.csv')
    if request.form['button'] == 'Create':
        if len(stories) == 1:
            id_number = '1'
        else:
            id_number = str(int(stories[len(stories)-1][0])+1)
        new_row = []
        new_row.append(id_number)
        new_row.append(request.form['story_title'])
        new_row.append(request.form['user_story'])
        new_row.append(request.form['criteria'])
        new_row.append(request.form['value'])
        new_row.append(request.form['estimation'])
        new_row.append(request.form['status'])
        stories = append_data(new_row)
        return render_template('list.html', stories=stories, title='Super Sprinter 3000')
    elif request.form['button'] == 'Update':
        original_data = read_data()
        id = request.form['id']
        new_row = []
        new_row.append(id)
        new_row.append(request.form['story_title'])
        new_row.append(request.form['user_story'])
        new_row.append(request.form['criteria'])
        new_row.append(request.form['value'])
        new_row.append(request.form['estimation'])
        new_row.append(request.form['status'])
        new_data = []
        for row in original_data:
            if row[0] != id:
                new_data.append(row)
            else:
                new_data.append(new_row)
        write_data(new_data)
        return redirect('/')


def read_data(file_name='database.csv'):
    data = []
    with open(file_name, newline='') as f:
            datareader = csv.reader(f, delimiter=',', quotechar='|')
            for row in datareader:
                data.append(row)
    return data


def append_data(new_story, file_name='database.csv'):
    with open(file_name, 'a', newline='') as f:
        datawriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(new_story)
    stories = read_data('database.csv')
    return stories


def write_data(story, file_name='database.csv'):
    with open(file_name, 'w', newline='') as f:
        datawriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerows(story)


if __name__ == '__main__':
    app.run()