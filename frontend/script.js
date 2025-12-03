
const API_BASE = '/api';

async function api(path, method='GET', body=null) {
  const opts = {method, headers:{'Content-Type':'application/json'}};
  if(body) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  return res.json();
}

async function loadPatients(){
  const list = document.getElementById('patient-list');
  list.innerHTML = '<li>Loading...</li>';
  const patients = await api('/patients');
  list.innerHTML = '';
  patients.forEach(p=>{
    const li = document.createElement('li');
    li.textContent = `${p.id}: ${p.name} (${p.age} anni)`;
    list.appendChild(li);
  });
}

async function loadAppointments(){
  const list = document.getElementById('appt-list');
  list.innerHTML = '<li>Loading...</li>';
  const appts = await api('/appointments');
  list.innerHTML = '';
  appts.forEach(a=>{
    const li = document.createElement('li');
    li.textContent = `${a.id}: paziente ${a.patient_id} - ${a.date} - ${a.reason}`;
    list.appendChild(li);
  });
}

document.getElementById('patient-form').onsubmit = async (e)=>{
  e.preventDefault();
  const name = document.getElementById('p-name').value;
  const age = parseInt(document.getElementById('p-age').value,10);
  await api('/patients', 'POST', {name, age});
  document.getElementById('p-name').value=''; document.getElementById('p-age').value='';
  loadPatients();
}

document.getElementById('appt-form').onsubmit = async (e)=>{
  e.preventDefault();
  const patient_id = parseInt(document.getElementById('a-patient-id').value,10);
  const date = document.getElementById('a-date').value;
  const reason = document.getElementById('a-reason').value;
  await api('/appointments', 'POST', {patient_id, date, reason});
  document.getElementById('a-patient-id').value=''; document.getElementById('a-date').value=''; document.getElementById('a-reason').value='';
  loadAppointments();
}

window.onload = ()=>{ loadPatients(); loadAppointments(); }
