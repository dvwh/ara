#   Copyright 2016 Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.


from flask import render_template
from ara import app, models, utils


# Routes
@app.route('/')
def main():
    """ Returns the home page """
    default_data = utils.default_data()
    return render_template('home.html', **default_data)


@app.route('/host/<host>')
@app.route('/host/<host>/<status>')
def host(host, status=None):
    default_data = utils.default_data()

    if status is not None:
        status_query = utils.status_to_query(status)
        data = models.Tasks.query.filter_by(host=host, **status_query)
    else:
        data = models.Tasks.query.filter_by(host=host)

    return render_template('host.html', host=host, data=data, **default_data)


@app.route('/task/<task>')
@app.route('/task/<task>/<status>')
def task(task, status=None):
    default_data = utils.default_data()

    if status is not None:
        status_query = utils.status_to_query(status)
        data = models.Tasks.query.filter_by(task=task, **status_query)
    else:
        data = models.Tasks.query.filter_by(task=task)

    return render_template('task.html', task=task, data=data, **default_data)


@app.route('/play/<play>')
@app.route('/play/<play>/<status>')
def play(play, status=None):
    default_data = utils.default_data()

    if status is not None:
        status_query = utils.status_to_query(status)
        data = models.Tasks.query.filter_by(play=play, **status_query)
    else:
        data = models.Tasks.query.filter_by(play=play)

    return render_template('play.html', play=play, data=data, **default_data)


@app.route('/playbook/<playbook>')
@app.route('/playbook/<playbook>/<status>')
def playbook(playbook, status=None):
    default_data = utils.default_data()
    playbook_data = models.Playbooks.query.filter_by(playbook=playbook).first()
    playbook_uuid = playbook_data.id

    if status is not None:
        status_query = utils.status_to_query(status)
        task_data = models.Tasks.query.filter_by(playbook_uuid=playbook_uuid,
                                                 **status_query)
    else:
        task_data = models.Tasks.query.filter_by(playbook_uuid=playbook_uuid)
    stats_data = models.Stats.query.filter_by(playbook_uuid=playbook_uuid)

    return render_template('playbook.html', playbook=playbook,
                           playbook_data=playbook_data, task_data=task_data,
                           stats_data=stats_data, **default_data)
