# Team-Setup-and-Project-Planning

## Team Members
- Valois Niyigaba
- Prudence Tracey Browns
- Samuel Niyonkuru

## Project Description
In this group project, we are creating an enterprise level fullstack application to process MoMo SMS data in XML format, clean and categorize the data, store it in a relational database, and provide a frontend for analysis and visualization.

# Repository Structure
 ![Repository structure](./docs/Screenshot%202025-09-19%20184604.png)


# System Architecture

Our architecture is based on an **ETL pipeline + database + frontend dashboard**, with an optional API layer.  

   🔹 Flow
1. **Input Layer**
   - Receives XML data (MoMo SMS).
   - Handles initial input and validation.

2. **ETL Pipeline**
   - Parse: To extract transaction records from XML.
   - Clean: Normalize dates, amounts, and phone numbers.
   - Categorize: Classify transactions (deposit, withdrawal, transfer).
   - Load: Insert cleaned and categorized data into SQLite.

3. **Database Layer**
   - Stores normalized and categorized transactions in SQLite.
   - Provides structured queries for analytics.

4. **Frontend Dashboard**
   - Reads processed JSON/DB data.
   - Visualizes transactions using charts and tables.

5. **Optional FastAPI Backend**
   - Provides API endpoints 
   - Serves data to frontend or external systems

[VIEW our draft Architecture Diagram HERE!](https://drive.google.com/file/d/16Aut1PggC4ixzqP85awJLTl4BbRlYdfn/view?usp=sharing)

## Our Database Design
Our MoMo SMS database is designed to capture, classify, and analyze mobile money transactions from SMS data.   

### Entities
- **Users** → Stores the users' details like their name, phone number, email and account status.  
- **Categories** → For classifying payments. 
- **Transactions** → For all the transactions made by the users.   

### Constraints
- PK and FK relationships  
- Unique constraints
- Check constraints 
- Cascading rules

### Indexing
- Transactions are indexed by `time`, `sender_id`, `receiver_id`, and `category_id` to support analytics.   

# Scrum Board
We are using GitHub Projects to manage our tasks. 
We have created 3 columns on our board where we put our completed, in progress and to do lists.
[View Our Scrum Board Here!](https://github.com/users/attorney755/projects/3>)
