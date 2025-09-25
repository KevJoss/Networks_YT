import smtplib
from email.message import EmailMessage

# Configuración del correo
msg = EmailMessage()
msg['Subject'] = 'Correo HTML desde Gmail'
msg['From'] = 'kelth.joss53@gmail.com'      # tu cuenta de Outlook
msg['To'] = 'kevincillo6653@gmail.com'      # correo del destinatario

# Contenido en texto plano
text = "Hola, este correo está diseñado en HTML!"

# Contenido en HTML
html = """
<html>
  <body>
    <h1 style="color: #4CAF50;">¡Hola a mi mismo!</h1>
    <p>Este correo es una prueba de funcionamiento del protocolo SMTP de forma segura <b>diseñado en HTML</b> desde Python usando <i>GMAIL SMTP</i>.</p>
    <img src="https://serversmtp.com/wp-content/uploads/2024/09/smtp-que-es-y-como-funciona.jpg" alt="Imagen sobre un protocolo SMTP" width="300">
    <p>Voy a incluir algunos enlaces de álbumes y playlists de Spotify que debería escuchar pronto:</p>
    <ul>
      <li><a href="https://open.spotify.com/intl-es/album/2X6WyzpxY70eUn3lnewB7d?si=TFK_lmHRTSqtWlUswW-dcQ">Data - Tainy</a></li>
      <li><a href="https://open.spotify.com/intl-es/album/7kfPf285KnlWUTbqaB1jnI?si=9k3iYOPNQYOL3aBj3HLH9g">Sayonara - Alvaro Diaz</a></li>
      <li><a href="https://open.spotify.com/intl-es/album/2GROf0WKoP5Er2M9RXVNNs?si=0iZwd_u2RHSP7dapgqzylQ">The car - Arctic Monkeys</a></li>
      <li><a href="https://open.spotify.com/intl-es/album/3hPzlhEUvBbKEBeGMhCu3h?si=9Zbw6Z80QI2GdIbfpMbOFg">El Big blue - Bandalos Chinos</a></li>
      <li><a href="https://open.spotify.com/intl-es/album/5dmUoar8TvME0J8IvZmZS3?si=MlS_PCAzSK2obycjQaZZtw">BACH - Bandalos Chinos</a></li>
      <li><a href="https://open.spotify.com/intl-es/album/78bpIziExqiI9qztvNFlQu?si=gR8VmXyISuusZU7LLuWxHg">AM - Arctic Monkeys</a></li>
    </ul>
    <hr>
    <p style="font-size: small;">Enviado desde Python con GMAIL SMTP</p>
    <p style="font-size: small;">Bendiciones a la familia</p>
  </body>
</html>
"""

# Adjuntar ambas versiones (texto y HTML)
msg.set_content(text)
msg.add_alternative(html, subtype='html')

# Configuración del servidor SMTP de Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'kelth.joss53@gmail.com'
smtp_password = 'djud zmce lvsz wfer'

# Enviar correo
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # activar TLS
    server.login(smtp_user, smtp_password)
    server.send_message(msg)

print("Correo HTML enviado exitosamente!")