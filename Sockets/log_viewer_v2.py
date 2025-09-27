import http.server
import socketserver
import re 
import os
import time

PORT = 8081

class LogHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '-1')
        self.end_headers()
        
        # Diagnóstico
        print(f"[{time.strftime('%H:%M:%S')}] Handling request and reading log file...")
        
        # Extract the last 3 connections of log file
        log_entries = self.extract_last_connections(3)
        
        # Create HTML with logs
        html = self.create_html(log_entries)
        
        # Send the response 
        self.wfile.write(html.encode())
        
    def extract_last_connections(self, num_connections=3):
        try:
            log_path = "server_information.log"
            abs_path = os.path.abspath(log_path)
            
            print(f"Looking for log file at: {abs_path}")
            print(f"File exists: {os.path.exists(log_path)}")
            
            if not os.path.exists(log_path):
                return ["Log file not found at: " + abs_path]
                    
            with open(log_path, "r") as f:
                content = f.read()
            
            print(f"Log file size: {len(content)} bytes")
                    
            # Usar puntos de inicio de conexión para dividir el archivo
            connection_start_points = [m.start() for m in re.finditer(r'INFO:__main__:\[CONNECTION OPENED\]', content)]
            
            if not connection_start_points:
                return ["No connection blocks found in the log file"]
            
            print(f"Found {len(connection_start_points)} connection start points")
            
            connection_blocks = []
            for i in range(len(connection_start_points)):
                start = connection_start_points[i]
                # Si no es el último bloque, toma hasta el siguiente inicio
                if i < len(connection_start_points) - 1:
                    end = connection_start_points[i + 1]
                    block = content[start:end]
                else:
                    # Si es el último, toma hasta el final
                    block = content[start:]
                
                connection_blocks.append(block)
                
            # Get the last num_connections blocks
            result = connection_blocks[-num_connections:] if connection_blocks else ["No connections found"]
            print(f"Returning {len(result)} connection blocks")
            return result
                
        except Exception as e:
            print(f"Error reading log file: {str(e)}")
            return [f"Error reading logs: {str(e)}"]
    
    def create_html(self, log_blocks):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = int(time.time())
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Calculator Server Logs</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 40px;
                    background-color: #f8f9fa;
                    color: #333;
                }}
                h1 {{
                    color: #343a40;
                    border-bottom: 2px solid #dee2e6;
                    padding-bottom: 10px;
                }}
                .connection {{
                    background-color: #ffffff;
                    padding: 20px;
                    margin-bottom: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    border-left: 5px solid #28a745;
                }}
                pre {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 4px;
                    font-size: 14px;
                    line-height: 1.5;
                }}
                .refresh {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin-bottom: 20px;
                    font-weight: bold;
                }}
                .refresh:hover {{
                    background-color: #0056b3;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    transition: all 0.2s;
                }}
                h2 {{
                    color: #28a745;
                    margin-top: 0;
                }}
                .timestamp {{
                    color: #6c757d;
                    font-style: italic;
                    margin-bottom: 20px;
                }}
                .success {{
                    color: #28a745;
                    font-weight: bold;
                }}
                .error {{
                    color: #dc3545;
                    font-weight: bold;
                }}
                .operation {{
                    color: #007bff;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>Calculator Server Logs - Last 3 Connections</h1>
            <p class="timestamp">Página generada el: {current_time} (se actualiza automáticamente cada 10 segundos)</p>
            <a href="/?t={timestamp}" class="refresh">Actualizar ahora</a>
        """
        
        if not log_blocks:
            html += "<p>No se encontraron conexiones en los logs.</p>"
        elif isinstance(log_blocks[0], str) and "error" in log_blocks[0].lower():
            # Es un mensaje de error
            html += f"<p class='error'>{log_blocks[0]}</p>"
        else:
            for i, block in enumerate(log_blocks):
                # Colorear algunos elementos para mejorar la presentación
                colorized_block = block
                
                # Resaltar operaciones
                colorized_block = re.sub(
                    r'Operation: (add|sub|mul|div|min)', 
                    r'Operation: <span class="operation">\1</span>', 
                    colorized_block
                )
                
                # Resaltar códigos de éxito
                colorized_block = re.sub(
                    r'Code: (200)', 
                    r'Code: <span class="success">\1</span>', 
                    colorized_block
                )
                
                # Resaltar códigos de error
                colorized_block = re.sub(
                    r'Code: (4\d\d|5\d\d)', 
                    r'Code: <span class="error">\1</span>', 
                    colorized_block
                )
                
                # Resaltar errores
                colorized_block = re.sub(
                    r"'error': '([^']*)'", 
                    r"'error': '<span class='error'>\1</span>'", 
                    colorized_block
                )
                
                html += f"""
                <div class="connection">
                    <h2>Conexión {i+1}</h2>
                    <pre>{colorized_block}</pre>
                </div>
                """
        
        html += """
        </body>
        </html>
        """
        return html

# Create and run the server
if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), LogHandler) as httpd:
        print(f"Log viewer running on port {PORT}")
        httpd.serve_forever()