from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import getpass


with open('../data/transactions.json', 'r') as f:
    transactions = json.load(f)

class TransactionAPI(BaseHTTPRequestHandler):
    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if not auth_header:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Authentication Required"')
            self.end_headers()
            self.wfile.write(b'Authorization required')
            return False

        try:
            auth_type, auth_string = auth_header.split(' ')
            if auth_type.lower() != 'basic':
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Invalid authorization type')
                return False

            decoded = base64.b64decode(auth_string).decode('utf-8')
            username, password = decoded.split(':', 1)
            if username != "team2" or password != "alu@123":
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'401 Unauthorized due to Invalid credentials')
                return False
            return True
        except Exception:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'401 Unauthorized due to Invalid credentials')
            return False

    def do_GET(self):
        if not self.authenticate():
            return

        if self.path == '/transactions':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(transactions).encode())
        elif self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            transaction = next((t for t in transactions if t['transaction_id'] == transaction_id), None)
            if transaction:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(transaction).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Transaction not found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def do_POST(self):
        if not self.authenticate():
            return

        if self.path == '/transactions':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_transaction = json.loads(post_data.decode('utf-8'))
            transactions.append(new_transaction)

            
            with open('../data/transactions.json', 'w') as f:
                json.dump(transactions, f, indent=4)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_transaction).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def do_PUT(self):
        if not self.authenticate():
            return

        if self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_transaction = json.loads(put_data.decode('utf-8'))

            for i, transaction in enumerate(transactions):
                if transaction['transaction_id'] == transaction_id:
                    transactions[i] = updated_transaction

                    with open('../data/transactions.json', 'w') as f:
                        json.dump(transactions, f, indent=4)

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'Transaction updated successfully')
                    return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Transaction not found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def do_DELETE(self):
        if not self.authenticate():
            return

        if self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            for i, transaction in enumerate(transactions):
                if transaction['transaction_id'] == transaction_id:
                    del transactions[i]

                    
                    with open('../data/transactions.json', 'w') as f:
                        json.dump(transactions, f, indent=4)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Transaction deleted')
                    return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Transaction not found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')


if __name__ == "__main__":
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if username != "team2" or password != "alu@123":
        print("401 Unauthorized due to Invalid credentials")
        exit(1)

    server = HTTPServer(('localhost', 8080), TransactionAPI)
    print("Server running on http://localhost:8080")
    print("Username: team2, password: alu@123")
    server.serve_forever()
