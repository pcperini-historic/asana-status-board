# imports
import md5
import flask
import jinja2
import pyasana
import datetime
from libs.async import async

# constants
apiKey = "14THihfO.MBsmW5MxmCFrjFsNkFyivKd"
workspaceID = "3799843448328"
maximumNumberOfTasks = 5
pageRefreshRate = 120 #seconds

statusBoardTemplate = "asana-status-board.tmpl.html"

# globals
api = pyasana.Api(apiKey)
flaskApp = flask.Flask(__name__)
flaskApp.data = {
    'recentTasks': [],
    'isUpdatingRecentTasks': False
}

# functions
@async
def updateRecentTasks():
    if flaskApp.data['isUpdatingRecentTasks']:
        return
        
    flaskApp.data['isUpdatingRecentTasks'] = True
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
            
    print "updated tasks: ", [task.name for task in tasks]
    flaskApp.data['recentTasks'] = tasks
    flaskApp.data['isUpdatingRecentTasks'] = False
    
# handlers
@flaskApp.route("/")
def handleRoot():
    return "Welcome to Asana Status Board. Please navigate to one of the valid sub-paths."

@flaskApp.route("/MegaBits")
def handleMegaBitsTasks():
    updateRecentTasks()
    return flask.render_template(
        statusBoardTemplate,
        tasks = flaskApp.data['recentTasks'],
        refreshrate = pageRefreshRate
    )
    
# main
if __name__ == "__main__":
    flaskApp.run(
        host = '0.0.0.0',
        debug = True
    )