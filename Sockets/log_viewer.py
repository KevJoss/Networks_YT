import http.server
import socketserver
import re 
import os

PORT = 8081

class LogHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
#       Extract the last 3 connections of log file
        log_entries = self.extract_last_connections(3)
        
#       Create HTML with logs
        html = self.create_html(log_entries)
        
#       Send the response 
        self.wfile.write(html.encode())
        
def extract_last_connections(self, num_connections=3):
    try:
        log_path = "server_information.log"
        
        # Imprime información de diagnóstico
        print(f"Trying to read log file: {os.path.abspath(log_path)}")
        print(f"File exists: {os.path.exists(log_path)}")
        
        if not os.path.exists(log_path):
            return ["Log file not found"]
                    
        # Lee el archivo completo cada vez
        with open(log_path, "r") as f:
            content = f.read()
            
        # Muestra parte del contenido para diagnóstico
        print(f"File size: {len(content)} bytes")
        print(f"First 100 chars: {content[:100]}")
            
        # Ajustamos la expresión regular para capturar correctamente las conexiones
        connection_blocks = re.findall(
            r'INFO:__main__:\[CONNECTION OPENED\].*?INFO:__main__:\[CONNECTION CLOSED\].*?(?=INFO:__main__:\[CONNECTION OPENED\]|\Z)', 
            content, 
            re.DOTALL
        )
        
        print(f"Found {len(connection_blocks)} connection blocks")
                
        # Get the last num_connections blocks
        return connection_blocks[-num_connections:] if connection_blocks else ["No connections found"]
                
    except Exception as e:
        print(f"Error in extract_last_connections: {e}")
        return [f"Error reading logs: {str(e)}"]
    
    def create_html(self, log_blocks):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Calculator Server Logs</title>
            <style>
                body {
                    font-family: monospace;
                    margin: 40px;
                    background-color: #f8f9fa;
                }
                h1 {
                    color: #343a40;
                    border-bottom: 2px solid #dee2e6;
                    padding-bottom: 10px;
                }
                .connection {
                    background-color: #ffffff;
                    padding: 20px;
                    margin-bottom: 30px;
                    border-radius: 5px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                    border-left: 5px solid #007bff;
                }
                pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 4px;
                }
                .refresh {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin-bottom: 20px;
                }
                .refresh:hover {
                    background-color: #0069d9;
                }
                h2 {
                    color: #007bff;
                    margin-top: 0;
                }
            </style>
        </head>
        <body>
            <h1>Calculator Server Logs - Last 3 Connections</h1>
            <a href="/" class="refresh">Refresh</a>
        """
        
        if not log_blocks:
            html += "<p>No connections found in logs.</p>"
        elif isinstance(log_blocks[0], str) and "error" in log_blocks[0].lower():
            # Es un mensaje de error
            html += f"<p>{log_blocks[0]}</p>"
        else:
            for i, block in enumerate(log_blocks):
                html += f"""
                <div class="connection">
                    <h2>Connection {i+1}</h2>
                    <pre>{block}</pre>
                </div>
                """
        
        html += """
        </body>
        </html>
        """
        return html

# Create and run the server
with socketserver.TCPServer(("0.0.0.0", PORT), LogHandler) as httpd:
    print(f"Log viewer running on port {PORT}")
    httpd.serve_forever()