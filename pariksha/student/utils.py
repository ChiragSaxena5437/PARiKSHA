import random
import pygal

def shuffle(q):
    selected_keys = []
    i = 0
    while i < len(q):
        current_selection = random.choice(list(q.keys()))
        if current_selection not in selected_keys:
            selected_keys.append(current_selection)
            i = i+1
    return selected_keys

def bar_graph(list_of_quizzes):
    graph = pygal.Bar()
    graph.title = 'Perfomance Analysis'
    x_labels,user_marks,highest_marks,avg_marks = list(),list(),list(),list()
    for quiz in list_of_quizzes:
        x_labels.append(quiz['quiz_title'])
        user_marks.append(quiz['marks'])
        highest_marks.append(max(quiz['all_marks']))
        avg_marks.append(sum(quiz['all_marks'])/len(quiz['all_marks']))
    graph.x_labels = x_labels
    graph.add('Your Marks',user_marks)
    graph.add('Avg. Class Marks',avg_marks)
    graph.add('Highest Marks',highest_marks)

    return graph.render_data_uri()


