import sqlite3
import re
from datetime import datetime
from nlp_model import NLPProcessor


class QueryProcessor:
    def __init__(self, db_path='data\company.db'):
        self.db_path = db_path
        self.nlp= NLPProcessor()
    
    def _get_connection(self):
        """Create a new database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # To access columns by name
        return conn
    
    def process_query(self, query):
        """Use NLP to classify the query before passing it to the rule-based SQL model."""
        query_type, error = self.nlp.classify_query(query)
        
        if error:
            return error  # Return message if the query is unclear
        
        if query_type == "employees_in_department":
            return self._employees_in_department(query)
        elif query_type == "department_manager":
            return self._get_department_manager(query)
        elif query_type == "hired_after":
            return self._employees_hired_after(query)
        elif query_type == "salary_expense":
            return self._total_salary_expense(query)
        elif query_type == "all_employees":
            return self._list_all_employees()
        elif query_type == "all_departments":
            return self._list_all_departments()
        else:
            return "Sorry, I couldn't match your query with known types."
        
        #except Exception as e:
            #return f"An error occurred: {str(e)}"
    
    def _employees_in_department(self, query):
        # Extract department name
        match = re.search(r'employees in the (\w+) department', query)
        if not match:
            return "Invalid department query format."
        
        department = match.group(1).capitalize()

        # Get a new database connection for this request
        conn = self._get_connection()
        cursor = conn.cursor()

        # Execute SQL query with DISTINCT to avoid duplicates
        cursor.execute("""
            SELECT DISTINCT Name, Salary, Hire_Date
            FROM Employees
            WHERE Department = ?
        """, (department,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return f"No employees found in the {department} department."
        
        # Format results as an HTML table
        response = f"<h3>Employees in the {department} department:</h3>"
        response += "<table border='1'><tr><th>Name</th><th>Salary</th><th>Hire Date</th></tr>"
        for name, salary, hire_date in results:
            response += f"<tr><td>{name}</td><td>${salary:,.2f}</td><td>{hire_date}</td></tr>"
        response += "</table>"
    
        return response

    
    def _get_department_manager(self, query):
        # Extract department name
        match = re.search(r'manager of the (\w+) department', query)
        if not match:
            return "Invalid department manager query format."
        
        department = match.group(1).capitalize()
        
        # Get a new database connection for this request
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Execute SQL query
        cursor.execute("""
            SELECT Manager 
            FROM Departments 
            WHERE Name = ?
        """, (department,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return f"No manager found for the {department} department."
        
        return f"<h3>Manager of the {department} department:</h3><p>{result[0]}</p>"
    
    def _employees_hired_after(self, query):
        # Extract date
        match = re.search(r'hired after (\d{4}-\d{2}-\d{2})', query)
        if not match:
            return "Invalid date format. Use YYYY-MM-DD."
        
        hire_date = match.group(1)
        
        # Validate date
        try:
            datetime.strptime(hire_date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format."
        
        # Get a new database connection for this request
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Execute SQL query
        cursor.execute("""
            SELECT DISTINCT Name, Department, Salary, Hire_Date 
            FROM Employees 
            WHERE Hire_Date > ?
            ORDER BY Hire_Date
        """, (hire_date,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return f"No employees hired after {hire_date}."
        
        # Format results as an HTML table
        response = f"<h3>Employees hired after {hire_date}:</h3>"
        response += "<table border='1'><tr><th>Name</th><th>Department</th><th>Salary</th><th>Hire Date</th></tr>"
        for name, dept, salary, hired in results:
            response += f"<tr><td>{name}</td><td>{dept}</td><td>${salary:,.2f}</td><td>{hired}</td></tr>"
        response += "</table>"
        
        return response
    
    def _total_salary_expense(self, query):
        # Extract department name
        match = re.search(r'total salary expense for the (\w+) department', query)
        if not match:
            return "Invalid salary expense query format."
        
        department = match.group(1).capitalize()
        
        # Get a new database connection for this request
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Execute SQL query
        cursor.execute("""
            SELECT SUM(Salary) 
            FROM Employees 
            WHERE Department = ?
        """, (department,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result[0] is None:
            return f"No salary data found for the {department} department."
        
        return f"<h3>Total salary expense for {department} department:</h3><p>${result[0]:,.2f}</p>"
    
    def _list_all_employees(self):
        # Get a new database connection for this request
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Execute SQL query
        cursor.execute("""
            SELECT Name, Department, Salary, Hire_Date 
            FROM Employees 
            ORDER BY Department, Name
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "No employees found."
        
        # Format results as an HTML table
        response = "<h3>All Employees:</h3>"
        response += "<table border='1'><tr><th>Name</th><th>Department</th><th>Salary</th><th>Hire Date</th></tr>"
        for name, dept, salary, hired in results:
            response += f"<tr><td>{name}</td><td>{dept}</td><td>${salary:,.2f}</td><td>{hired}</td></tr>"
        response += "</table>"
        
        return response
    
    def _list_all_departments(self):
        # Get a new database connection for this request
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Execute SQL query
        cursor.execute("""
            SELECT Name, Manager 
            FROM Departments 
            ORDER BY Name
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "No departments found."
        
        # Format results as an HTML table
        response = "<h3>All Departments:</h3>"
        response += "<table border='1'><tr><th>Name</th><th>Manager</th></tr>"
        for name, manager in results:
            response += f"<tr><td>{name}</td><td>{manager}</td></tr>"
        response += "</table>"
        
        return response
