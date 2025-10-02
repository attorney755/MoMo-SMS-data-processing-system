# Team-Setup-and-Project-Planning

## Team Members
- Attorney Valois Niyigaba
- Prudence Tracey Browns
- Samuel Niyonkuru
- Ngarambe David

## Project Description
In this group project, we are creating an enterprise level fullstack application to process MoMo SMS data in XML format, clean and categorize the data, store it in a relational database, and provide a frontend for analysis and visualization.

## Repository Structure
![Repository structure](./docs/Screenshot%202025-09-19%20184604.png)

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- `curl` for API testing

### 2. Clone Repository
```bash
git clone https://github.com/attorney755/MoMo-SMS-data-processing-system.git
cd MoMo-SMS-data-processing-system
```

### 3. Run the API Server
```bash
python api/server.py
```
The server will start on `http://localhost:8080` with these credentials:
- Username: `team2`
- Password: `alu@123`

### 4. Verify Installation
Test the API with:
```bash
curl --user team2:alu%40123 http://localhost:8080/transactions
```

### 5. (Optional) Run DSA Comparison
```bash
cd dsa
python search_comparison.py
```

## System Architecture
Our architecture is based on an ETL pipeline + database + frontend dashboard, with an optional API layer.

### Flow:
1. **Input Layer**
   - Receives XML data (MoMo SMS)
   - Handles initial input and validation

2. **ETL Pipeline**
   - Parse: Extracts transaction records from XML
   - Clean: Normalizes dates, amounts, and phone numbers
   - Categorize: Classifies transactions (deposit, withdrawal, transfer)
   - Load: Inserts cleaned data into SQLite

3. **Database Layer**
   - Stores normalized transactions in SQLite
   - Provides structured queries for analytics

4. **Frontend Dashboard**
   - Reads processed JSON/DB data
   - Visualizes transactions using charts and tables

5. **Optional FastAPI Backend**
   - Provides API endpoints
   - Serves data to frontend or external systems

[VIEW our draft Architecture Diagram HERE!](https://drive.google.com/file/d/16Aut1PggC4ixzqP85awJLTl4BbRlYdfn/view?usp=sharing)

## Database Design
Our MoMo SMS database is designed to capture, classify, and analyze mobile money transactions from SMS data.

### Entities
- **Users**: Stores users' details (name, phone number, email, account status)
- **Categories**: For classifying payments
- **Transactions**: For all transactions made by users

### Constraints
- Primary Key and Foreign Key relationships
- Unique constraints
- Check constraints
- Cascading rules

### Indexing
Transactions are indexed by `time`, `sender_id`, `receiver_id`, and `category_id` to support analytics.

## Scrum Board
We are using GitHub Projects to manage our tasks with three columns:
- Completed
- In Progress
- To Do

[View Our Scrum Board Here!](https://github.com/users/attorney755/projects/3)

## Reports and Documentation
Find our complete documentation and reports in:
- `docs/api_docs.md` - API endpoint documentation
- `MoMo_API_Report.pdf` - Complete project report
- `MoMo_API_Report.docx` - Editable report version

## API Documentation
For complete API documentation including:
- Endpoint specifications
- Authentication details
- Request/response examples
- Error codes

See: [API Documentation](docs/api_docs.md)
