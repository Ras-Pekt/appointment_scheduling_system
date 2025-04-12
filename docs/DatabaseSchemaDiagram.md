┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Users │ │ Doctors │ │ Patients │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ PK: id │───┐ │ PK: id │ ┌───│ PK: id │
│ email │ │ │ FK: user_id │ │ │ FK: user_id │
│ first_name │ │ │ specialization │ │ │ insurance_prov │
│ last_name │ │ └─────────────────┘ │ │ insurance_num │
│ hashed_pw │ │ │ └─────────────────┘
│ role │ │ │
└─────────────────┘ │ │
| │ │
| 1:1 │ │
| (doctor) │ │
| │ │
| 1:1 │ │
| (patient) │ │
| │ │
▼ │ │
┌─────────────────┐ │ ┌─────────────────┐ │ ┌─────────────────┐
│ Appointments │ │ │ Availability │ │ │ MedicalRecords │
├─────────────────┤ │ ├─────────────────┤ │ ├─────────────────┤
│ PK: id │ │ │ PK: id │ │ │ PK: id │
│ FK: doctor_id │◄──┘ │ FK: doctor_id │◄──┘ │ FK: doctor_id │
│ FK: patient_id │ │ weekday │ │ FK: patient_id │
│ scheduled_time │ │ start_time │ │ FK: appt_id │
│ status │ │ end_time │ │ notes │
└─────────────────┘ │ available │ │ created_at │
▲ └─────────────────┘ └─────────────────┘
| ▲ ▲
| | |
└──────────────────────┘────────────────────────┘
