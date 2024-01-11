# Next Gen Car Showroom Management System: Specifications Layout

## Entities

### Employee

Each employee within the showroom can be identified by a **unique employee ID**. They have details like name, age, gender, and a fixed salary. Every employee is assigned to a **specific department** with a **designated role** (e.g., sales representative, manager) and started their employment on a particular date.

### Customer

Every customer visiting the showroom is assigned a **unique customer ID**. They possess attributes like name, age, contact information (phone number, email), and the date they first registered with the showroom. Their purchase history (if any) is recorded, along with any raw data extracted from their **scanned ID** through **OCR** technology (stored in NoSQL).

### Car

Each car available in the showroom has a **unique identifier**. Its details include make, model, year of manufacture, mileage covered, engine type, listed features, high-quality images and videos (stored in NoSQL), its current inventory status (e.g., available, sold), sale price, and a detailed maintenance history (stored in NoSQL).

### Department

Each department within the showroom has a **unique identifier** and a descriptive name. Additionally, each department is assigned a specific manager using their employee ID.

### Appointment

Every scheduled appointment between a customer and an employee for a specific car has a **unique identifier**. It's linked to both the customer and employee involved, along with the chosen car. Furthermore, it records the appointment date and time, and its current status (pending, confirmed, completed).

### Test Drive

After an appointment, a test drive conducted by a customer, employee, and specific car can be registered with a **unique identifier**. It's linked to the associated appointment and captures any customer feedback provided about the test drive experience.

### Sale

When a car is successfully sold, a detailed sale record is created with a **unique identifier**. It links the customer who purchased the car, the employee who facilitated the sale, and the specific car itself. The record documents the sale date, final price, chosen payment method, and any relevant finance details.

### Review

Every customer can leave a review for a specific car they interacted with, assigned a **unique identifier**. The review links the customer and car involved, captures a star rating, and allows the customer to express their written thoughts or experiences in detail.

## Relationships

### One-to-One

- **WORKS_FOR**: One Employee belongs to one Department: `employee.department_id` references `department.department_id`

- **APPOINTMENT_FOR**: One Appointment is for one Car: `appointment.car_id` references `car.car_id`

- **FOLLOWS**: One Test Drive is linked to one Appointment: `test_drive.appointment_id` references `appointment.appointment_id`

- **INVOLVES**: One Sale is for one Car: `sale.car_id` references `car.car_id`

- **SALE_BY**: One Sale is made by one Employee: `sale.employee_id` references `employee.employee_id`

- **SALE_TO**: One Sale is made to one Customer: `sale.customer_id` references `customer.customer_id`

- **ASSESSES**: One Review is for one Car: `review.car_id` references `car.car_id`

### One-to-Many

- **OWNS**: One Customer can have many Cars: `customer.customer_id` references `car.customer_id` (optional, tracks only cars purchased by the customer)

- **HANDLES**: One Employee can have many Appointments: `employee.employee_id` references `appointment.employee_id`

- **BOOKS**: One Customer can have many Appointments: `customer.customer_id` references `appointment.customer_id`

- **PROVIDES**: One Customer can write many Reviews: `customer.customer_id` references `review.customer_id`
