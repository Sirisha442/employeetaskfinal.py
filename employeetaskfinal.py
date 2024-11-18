import json

class Employee:
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary

    def display_details(self):
        print(f"Employee ID: {self.emp_id}")
        print(f"Name: {self.name}")
        print(f"Department: {self.department}")
        print(f"Salary: ${self.salary:,.2f}")

class EmployeeManagementSystem:
    def __init__(self):
        self.employees = []
        self.auto_id = 1  # Initial employee ID
        self.load_data()  # Load employee data when the system starts

    def load_data(self):
        try:
            # Attempt to load data from the JSON file
            with open("employees.json", "r") as file:
                data = json.load(file)

                # Check if data is a dictionary containing 'auto_id' and 'employees'
                if isinstance(data, dict):
                    self.auto_id = data.get("auto_id", 1)  # Default to 1 if no auto_id is found
                    self.employees = [Employee(**emp) for emp in data.get("employees", [])]  # Load employee records
                else:
                    print("Error: Data in JSON file is not in the expected format.")
        except FileNotFoundError:
            print("No data file found. Starting with an empty employee list.")
        except json.JSONDecodeError:
            print("Error reading the JSON file. The file may be corrupted or empty.")

    def save_data(self):
        try:
            # Save data back to JSON file
            data = {
                "auto_id": self.auto_id,
                "employees": [emp.__dict__ for emp in self.employees]  # Convert employee objects to dictionaries
            }
            with open("employees.json", "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    # Method to add a new employee
    def add_employee(self):
        print("\nEnter employee details:")
        name = input("Enter Name: ")
        department = input("Enter Department: ")
        salary = float(input("Enter Salary: "))

        # Create a new Employee object with an auto-generated ID
        employee = Employee(self.auto_id, name, department, salary)

        # Add employee to the list
        self.employees.append(employee)

        # Increment the auto_id for the next employee
        self.auto_id += 1

        print(f"Employee added successfully with ID: {employee.emp_id}")
        self.save_data()  # Save data after adding a new employee

    # Method to filter employees by department
    def filter_by_department(self, department):
        filtered_employees = [emp for emp in self.employees if emp.department.lower() == department.lower()]
        return filtered_employees

    # Method to filter employees by salary range
    def filter_by_salary_range(self, min_salary, max_salary):
        filtered_employees = [emp for emp in self.employees if min_salary <= emp.salary <= max_salary]
        return filtered_employees

    # Method to view employees
    def view_employees(self):
        if not self.employees:
            print("\nNo employees found!")
        else:
            print("\nEmployee Details:")
            for employee in self.employees:
                employee.display_details()

    # Method to view employees based on filters
    def view_filtered_employees(self):
        print("\nView Employees By:")
        print("1. Department")
        print("2. Salary Range")
        filter_choice = input("Enter 1 or 2 to filter: ").strip()

        if filter_choice == '1':
            department = input("Enter department to filter by: ").strip()
            filtered_employees = self.filter_by_department(department)
            self.display_filtered_employees(filtered_employees)

        elif filter_choice == '2':
            try:
                min_salary = float(input("Enter minimum salary: "))
                max_salary = float(input("Enter maximum salary: "))
                filtered_employees = self.filter_by_salary_range(min_salary, max_salary)
                self.display_filtered_employees(filtered_employees)
            except ValueError:
                print("Invalid salary input. Please enter numeric values.")

        else:
            print("Invalid choice for filtering option.")

    # Method to display filtered employees
    def display_filtered_employees(self, employees):
        if employees:
            print("\nFiltered Employee Details:")
            for employee in employees:
                employee.display_details()
        else:
            print("No employees found matching the criteria.")

    # Method to update employee details
    def update_employee(self):
        emp_id = int(input("\nEnter the Employee ID to update: "))
        employee = self.search_employee(emp_id)

        if employee:
            print(f"Updating details for Employee ID: {emp_id}")
            employee.name = input(f"Enter new name (Current: {employee.name}): ") or employee.name
            employee.department = input(f"Enter new department (Current: {employee.department}): ") or employee.department
            salary = input(f"Enter new salary (Current: {employee.salary}): ")
            employee.salary = float(salary) if salary else employee.salary
            print("Employee details updated successfully!")
            self.save_data()  # Save data after updating employee details
        else:
            print(f"No employee found with ID: {emp_id}")

    # Method to delete employee details
    def delete_employee(self):
        emp_id = int(input("\nEnter the Employee ID to delete: "))
        employee = self.search_employee(emp_id)

        if employee:
            self.employees.remove(employee)
            print(f"Employee with ID {emp_id} deleted successfully!")
            self.save_data()  # Save data after deleting an employee
        else:
            print(f"No employee found with ID: {emp_id}")

    # Method to search for an employee by ID
    def search_employee(self, emp_id):
        for employee in self.employees:
            if employee.emp_id == emp_id:
                return employee
        return None

    # Method to calculate average salary by department
    def calculate_average_salary_by_department(self, department):
        employees_in_dept = self.filter_by_department(department)
        if not employees_in_dept:
            print(f"No employees found in the {department} department.")
            return
        total_salary = sum(emp.salary for emp in employees_in_dept)
        average_salary = total_salary / len(employees_in_dept)
        print(f"\nAverage salary in {department} department: ${average_salary:,.2f}")

# Main function to interact with the system
def main():
    system = EmployeeManagementSystem()

    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. View Employees by Criteria")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Search Employee")
        print("7. Calculate Average Salary by Department")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            system.add_employee()
        elif choice == '2':
            system.view_employees()
        elif choice == '3':
            system.view_filtered_employees()
        elif choice == '4':
            system.update_employee()
        elif choice == '5':
            system.delete_employee()
        elif choice == '6':
            emp_id = int(input("\nEnter Employee ID to search: "))
            employee = system.search_employee(emp_id)
            if employee:
                employee.display_details()
            else:
                print(f"No employee found with ID: {emp_id}")
        elif choice == '7':
            department = input("\nEnter the department to calculate average salary: ").strip()
            system.calculate_average_salary_by_department(department)
        elif choice == '8':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
