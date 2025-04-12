Patient API Server Database Celery
| | | |
| 1. Get Doctor Availability| | |
|-------------------------->| | |
| | 2. Query Availability | |
| | (weekday+time filters) | |
| |----------------------->| |
| | | |
| | 3. Return Available Slots| |
| |<-----------------------| |
| 4. Show Available Slots | | |
|<--------------------------| | |
| | | |
| 5. Book Appointment | | |
| (doctor_id, patient_id, | | |
| scheduled_time) | | |
|-------------------------->| | |
| | 6. Begin Transaction | |
| |----------------------->| |
| | | |
| | 7. Check Slot Available| |
| |----------------------->| |
| | | |
| | 8. Create Appointment | |
| |----------------------->| |
| | | |
| | 9. Commit Transaction | |
| |----------------------->| |
| | | |
| | 10. Trigger Email Task | |
| |--------------------------------------------->|
| 11. Appointment Confirmed| | |
|<--------------------------| | |
