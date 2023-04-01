from flask import Flask, jsonify, request
from sqlalchemy import select, text

from drones.models import db, db_populate, CModel, CState, Drone, Medication

import time
from timeloop import Timeloop
from datetime import timedelta

# Create de TimeLoop
tl = Timeloop()

# create the app
app = Flask(__name__)

# Loading config from file
app.config.from_pyfile('config.py')

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
    db_populate()


@app.route('/')
def hello_world():
    from datetime import datetime
    now = datetime.now()
    pair = {'message': "It Works!", 'now_its': now.strftime("%H:%M:%S")}
    return jsonify({"result": pair})


@app.get('/model')
def get_models():
    result = []
    drone_models = db.session.execute(select(CModel.id, CModel.name))
    for row in drone_models:
        pair = {'id': str(row[0]), 'name': str(row[1])}
        result.append(pair)
    return jsonify({'result': result})


@app.get('/state')
def get_states():
    result = []
    drone_states = db.session.execute(select(CState.id, CState.name))
    for row in drone_states:
        pair = {'id': row[0], 'name': row[1]}
        result.append(pair)
    return jsonify({"result": result})


@app.get('/drone')
def get_drones():
    result = []
    query = select(Drone.id, Drone.serial, Drone.max_weight, Drone.battery, CModel.name.label("model"), CState.name.label("state")).join(CModel).join(CState)
    drone_states = db.session.execute(query)
    keys = [str(k['name']) for k in query.column_descriptions]
    for row in drone_states:
        drone = {}
        for (idx, val) in enumerate(keys):
            drone[val] = row[idx]
        result.append(drone)
    return jsonify({"result": result})


# registering a drone;
@app.post('/drone')
def add_drone():
    message = ""
    rq = request.get_json()
    drone = {"serial": rq["serial"], "model": rq["model"], "max_weight": rq["max_weight"], "battery": rq["battery"]}
    this_model = db.session.execute(select(CModel.name, CModel.id).where(CModel.name == rq["model"]))
    temp = this_model.fetchall()
    (out_model, out_id) = temp[0]
    drone['model_id'] = out_id
    ins_drone = "INSERT INTO Drone (serial, max_weight, battery, model_id, state_id) VALUES ('{0}', {1}, {2}, {3}, 1)".format(str(rq["serial"]), int(rq["max_weight"]), int(rq["battery"]), int(out_id))
    err = db.session.execute(text(ins_drone))
    db.session.commit()
    return jsonify({"result": drone, "message": str(ins_drone)})


# loading a drone with medication items;
@app.post('/drone/<string:serial>/load')
def load_drone(serial):
    result = []
    tmp_weight = 0
    message = ""
    query1 = select(Drone.id, Drone.max_weight, Drone.battery).where(Drone.serial == serial)
    this_drone = db.session.execute(query1).fetchall()
    (did, max_weight, battery) = this_drone[0]
    if battery <= 25:
        return jsonify({"message": "Batter is less or equal to 25%"})
    query_weight = select(Medication.weight).join(Drone.medications).where(Drone.serial == serial)
    all_weights = db.session.execute(query_weight).fetchall()
    for w in all_weights:
        tmp_weight += int(w[0])
    upd_loading = "UPDATE Drone SET state_id = {0} WHERE Drone.id = {1}".format(2, did)
    err = db.session.execute(text(upd_loading))
    db.session.commit()
    query2 = select(Medication.id, Medication.name, Medication.weight, Medication.code).where(Medication.drone_id == None)
    unloaded_meds = db.session.execute(query2)
    keys = [str(k['name']) for k in query2.column_descriptions]
    for row in unloaded_meds:
        if row[2] + tmp_weight >= max_weight:
            message = "Weight limit reached"
            continue
        tmp_weight += row[2]
        upd_med = "UPDATE Medication SET drone_id = {0} WHERE Medication.id = {1}".format(did, int(row[0]))
        err = db.session.execute(text(upd_med))
        db.session.commit()
        med = {}
        for (idx, val) in enumerate(keys):
            med[val] = row[idx]
        result.append(med)
    upd_loaded = "UPDATE Drone SET state_id = {0} WHERE Drone.id = {1}".format(3, did)
    err = db.session.execute(text(upd_loaded))
    db.session.commit()
    return jsonify({"result": result, "limit": max_weight, "message": message, "load": tmp_weight})


# checking loaded medication items for a given drone;
@app.get('/drone/<string:serial>/load')
def get_load(serial):
    result = []
    query = select(Medication.id, Medication.name, Medication.weight, Medication.code).join(Drone.medications).where(Drone.serial == serial)
    medications = db.session.execute(query)
    keys = [str(k['name']) for k in query.column_descriptions]
    weight = 0
    for row in medications:
        medication = {}
        for (idx, val) in enumerate(keys):
            medication[val] = row[idx]
            if val == 'weight':
                weight += row[idx]
        result.append(medication)
    return jsonify({'result': result, "weight": weight})


# checking available drones for loading;
@app.get('/drone/available')
def get_available():
    result = []
    query = select(Drone.id, Drone.serial, Drone.max_weight, Drone.battery, CModel.name.label("model"), CState.name.label("state")).join(CModel).join(CState).where(Drone.state_id == 1)
    drone_idle = db.session.execute(query)
    keys = [str(k['name']) for k in query.column_descriptions]
    for row in drone_idle:
        drone = {}
        for (idx, val) in enumerate(keys):
            drone[val] = row[idx]
        result.append(drone)
    return jsonify({"result": result})


# check drone battery level for a given drone;
@app.get('/drone/<string:serial>/battery')
def get_battery(serial):
    drone = db.session.execute(select(Drone.serial, Drone.battery).where(Drone.serial == serial))
    temp = drone.fetchall()
    (serial, battery) = temp[0]
    return jsonify({"serial": serial, "battery": battery})

@app.get('/drone/healthcheck')
def get_drone_health():
    pass


@tl.job(interval=timedelta(seconds=10))
def sample_job_every_10s():
    print("10s job current time : {}".format(time.ctime()))


if __name__ == '__main__':
    tl.start(block=True)
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True)
