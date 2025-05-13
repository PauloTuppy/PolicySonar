"""
PolicySonar Backend Server with historical analogs endpoint
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

class PolicySonarHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        endpoint = parsed_path.path
        
        if endpoint == '/health':
            self._handle_health()
        elif endpoint == '/api/policy-analogs':
            self._handle_get_analogs()
        else:
            self._handle_not_found()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        endpoint = parsed_path.path
        
        if endpoint == '/api/policy-analogs':
            self._handle_create_analog()
        else:
            self._handle_not_found()

    def _handle_health(self):
        self.send_response(200)
        self._set_json_headers()
        response = {'status': 'healthy'}
        self.wfile.write(json.dumps(response).encode())

    def _handle_get_analogs(self):
        self.send_response(200)
        self._set_json_headers()
        response = {
            'analogs': [
                {
                    'id': 1,
                    'policy_text': 'Sample policy text',
                    'historical_match': 'Historical policy match',
                    'similarity_score': 0.85,
                    'risk_factors': ['economic impact', 'public opposition'],
                    'outcome_analysis': 'Positive economic growth but faced public protests',
                    'policy_type': 'Economic',
                    'jurisdiction': 'National',
                    'time_period': '1990-1995'
                }
            ]
        }
        self.wfile.write(json.dumps(response).encode())

    def _handle_create_analog(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        self.send_response(201)
        self._set_json_headers()
        response = {
            'message': 'Policy analog created',
            'data': data
        }
        self.wfile.write(json.dumps(response).encode())

    def _handle_not_found(self):
        self.send_response(404)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Not Found')

    def _set_json_headers(self):
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PolicySonarHandler)
    print('Starting backend server on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
