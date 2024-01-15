# ER Diagram & Relational Mapping

## ER Diagram

![ER Diagram](./er%20snapshot.png)

### Entities Present

- **Employee**
- **Department**
- **Appointment**
- **Review**
- **Sale**
- **Customer**
- **Car**
- **Test Drive**

### Relationships Present

#### One-to-Many

- **WORKS_FOR**: Employee & Department (1:N)
- **HANDLES**: Employee & Appointment (1:N)
- **BOOKS**: Customer & Appointment (1:N)
- **PROVIDES**: Customer & Review (1:N)
- **OWNS**: Customer & Car (1:N)

#### One-to-One

- **MANAGES**: Employee & Department (1:1)
- **ASSESSES**: Review & Car (1:1)
- **SALE_TO**: Sale & Customer (1:1)
- **SALE_BY**: Sale & Employee (1:1)
- **APPOINTMENT_FOR**: Appointment & Car (1:1)
- **FOLLOWS**: Test Drive & Appointment (1:1)
- **INVOLVES**: Sale & Car (1:1)

## Mapping ER Diagram to Relational Schema
