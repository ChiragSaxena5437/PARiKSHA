from flask import Blueprint,render_template,request

extra = Blueprint('extra',__name__,template_folder='templates',url_prefix='/extra')

#url will be 127.0.0.1:5000/extra/test
@extra.route("/test")
def extra_test():
    #enter the name of template (eg. 'test_temp.html')
    #add the templates in the templates folder in the extra module
    return render_template("test_temp.html")


@extra.route("/test1", methods = ['POST','GET'])
def extra_test1():
    #enter the name of template (eg. 'test_temp.html')
    #add the templates in the templates folder in the extra module
    if request.method == 'POST':
        response = request.form
        no_of_questions = len(response)/5
        list_of_questions = dict()
        for num in range(1,int(no_of_questions)+1):
            question_key = "Question"+str(num)
            question = [ response[question_key] ,response["Option"+str(num)+"A"] ,response["Option"+str(num)+"B"] ,response["Option"+str(num)+"C"] ,response["Option"+str(num)+"D"], response["Marks"+str(num)]]
            list_of_questions[num] = question
        return list_of_questions
    elif request.method == 'GET':
        return render_template("teacherinput.html")

@extra.route("/test2")
def extra_test2():
    #enter the name of template (eg. 'test_temp.html')
    #add the templates in the templates folder in the extra module
    return render_template("test.html")
@extra.route("/testid")
def extra_testid():
    #enter the name of template (eg. 'test_temp.html')
    #add the templates in the templates folder in the extra module
    return render_template("teacherId.html")

