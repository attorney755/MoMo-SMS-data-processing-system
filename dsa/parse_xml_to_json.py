import xml.etree.ElementTree as ET
import json
import re

def extract_transaction_id(body):
    
    match = re.search(r'TxId:\s*(\d+)', body)
    if match:
        return match.group(1)
    match = re.search(r'Financial Transaction Id:\s*(\d+)', body)
    if match:
        return match.group(1)
    return None

def parse_xml_to_json(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    transactions = []

    for sms in root.findall('sms'):
        body = sms.get('body', '')
        transaction_id = extract_transaction_id(body)
        transaction = {
            'transaction_id': transaction_id if transaction_id else '',
            'type': sms.get('type', ''),
            'amount': '',  
            'sender': sms.get('address', ''),
            'receiver': '',  
            'timestamp': sms.get('readable_date', ''),
            'new_balance': '',  
            'message': body,
            'financial_transaction_id': transaction_id if transaction_id else '',
            'service_center': sms.get('service_center', ''),
            'fee': ''  
        }
        transactions.append(transaction)

    return transactions

if __name__ == "__main__":
    transactions = parse_xml_to_json('../data/modified_sms_v2.xml')
    with open('../data/transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)
