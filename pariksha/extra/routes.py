from flask import Blueprint,render_template

extra = Blueprint('extra',__name__,template_folder='templates',url_prefix='/extra')

#url will be 127.0.0.1:5000/extra/test
@extra.route("/test")
def extra_test():
    #enter the name of template (eg. 'test_temp.html')
    #add the templates in the templates folder in the extra module
    return render_template("test_temp.html")


@extra.route("/test1")
def extra_test1():
    #enter the name of template (eg. 'test_temp.html')
    #add the templates in the templates folder in the extra module
    return render_template("teacherinput.html")
