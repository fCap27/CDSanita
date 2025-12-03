
# Flask backend for ClinicaDemo (see README for running instructions)
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.String(64), nullable=False)
    reason = db.Column(db.String(256))

# CRUD endpoints (see swagger.json for documentation)
@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    p = Patient(name=data['name'], age=data['age'])
    db.session.add(p); db.session.commit()
    return jsonify({'id': p.id, 'name': p.name, 'age': p.age}), 201

@app.route('/api/patients', methods=['GET'])
def list_patients():
    ps = Patient.query.all()
    return jsonify([{'id':p.id,'name':p.name,'age':p.age} for p in ps])

@app.route('/api/patients/<int:pid>', methods=['GET'])
def get_patient(pid):
    p = Patient.query.get_or_404(pid)
    return jsonify({'id':p.id,'name':p.name,'age':p.age})

@app.route('/api/patients/<int:pid>', methods=['PUT'])
def update_patient(pid):
    p = Patient.query.get_or_404(pid)
    data = request.get_json()
    p.name = data.get('name', p.name)
    p.age = data.get('age', p.age)
    db.session.commit()
    return jsonify({'id':p.id,'name':p.name,'age':p.age})

@app.route('/api/patients/<int:pid>', methods=['DELETE'])
def delete_patient(pid):
    p = Patient.query.get_or_404(pid)
    db.session.delete(p); db.session.commit()
    return jsonify({'result': 'deleted'})

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    if not Patient.query.get(data['patient_id']):
        return jsonify({'error':'patient not found'}), 400
    a = Appointment(patient_id=data['patient_id'], date=data['date'], reason=data.get('reason',''))
    db.session.add(a); db.session.commit()
    return jsonify({'id':a.id,'patient_id':a.patient_id,'date':a.date,'reason':a.reason}), 201

@app.route('/api/appointments', methods=['GET'])
def list_appointments():
    ap = Appointment.query.all()
    return jsonify([{'id':a.id,'patient_id':a.patient_id,'date':a.date,'reason':a.reason} for a in ap])

@app.route('/api/appointments/<int:aid>', methods=['GET'])
def get_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    return jsonify({'id':a.id,'patient_id':a.patient_id,'date':a.date,'reason':a.reason})

@app.route('/api/appointments/<int:aid>', methods=['PUT'])
def update_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    data = request.get_json()
    a.date = data.get('date', a.date)
    a.reason = data.get('reason', a.reason)
    db.session.commit()
    return jsonify({'id':a.id,'patient_id':a.patient_id,'date':a.date,'reason':a.reason})

@app.route('/api/appointments/<int:aid>', methods=['DELETE'])
def delete_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    db.session.delete(a); db.session.commit()
    return jsonify({'result':'deleted'})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    if not os.path.exists('health.db'):
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
