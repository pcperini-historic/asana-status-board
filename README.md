__asana-status-board__ is a [Heroku](https://www.heroku.com)-ready [Flask](http://flask.pocoo.org) app. It reads in the most recently completed tasks from an [Asana](https://asana.com) workspace, and serves up a self-refreshing [Status Board](http://panic.com/statusboard/)-ready table.

Simply add your Heroku app's URL to a Status Board table widget, and watch the completed tasks roll in.

##Notes:##
- asana-status-board asynchronously loads the data from Asana. On the first load, no information will be provided.
- asana-status-board currently relies on a not-yet-pulled version of [pyasana](https://github.com/caseydunham/python-asana), ergo it lives in the `libs/` directory. Once that version is pulled, this repository will be updated to use the official build.