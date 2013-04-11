# imports
import md5
import flask
import jinja2
import pyasana
import datetime

# constants
apiKey = "14THihfO.MBsmW5MxmCFrjFsNkFyivKd"
workspaceID = "3799843448328"
maximumNumberOfTasks = 5

statusBoardTemplate = "asana-status-board.tmpl.html"

# globals
api = pyasana.Api(apiKey)
flaskApp = flask.Flask(__name__)

# functions
def tasks():
    projects = api.get_projects(int(workspaceID))

    tasks = []
    for project in projects:
        tasks.extend(api.get_tasks(int(project.id), fields = ["name", "completed_at", "assignee", "notes"]))
     
    for task in tasks:
        task.completed_at = datetime.datetime.strptime(task.completed_at, "%Y-%m-%dT%H:%M:%S.%fZ") if task.completed_at else datetime.datetime.fromtimestamp(0) 
    tasks = sorted(tasks, key = lambda task: task.completed_at, reverse = True)[:min(len(tasks), maximumNumberOfTasks)]
    
    for task in tasks:
        task.assignee = api.get_user(int(task.assignee.id)) if task.assignee else None
        if task.assignee:
            task.assignee.avatar = "http://www.gravatar.com/avatar/%s" % (md5.new(task.assignee.email.lower()).hexdigest())
    
    return tasks
    
# handlers
@flaskApp.route("/MegaBits")
def handleMegaBitsTasks():
    return flask.render_template(statusBoardTemplate, tasks = tasks())
    
# main
if __name__ == "__main__":
    flaskApp.run(
        host = '0.0.0.0',
        debug = True
    )