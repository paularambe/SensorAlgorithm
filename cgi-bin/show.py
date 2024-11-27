#!/usr/bin/python
import cgi
import sqlite3

# Establece la conexión con la base de datos
conn = sqlite3.connect('/var/www/html/data.db')
cursor = conn.cursor()
# Habilita la recepción de datos del formulario
form = cgi.FieldStorage()

# Obtiene el ID de los parámetros de la URL
id = form.getvalue("id")

# Realiza una consulta en la base de datos para obtener la información del usuario
cursor.execute("SELECT * FROM users WHERE session_id = ?", (id,))
user_info = cursor.fetchone()

# Cierra la conexión con la base de datos
conn.close()

# Configura el encabezado de respuesta HTTP
print("Content-type: text/html\n")

if user_info:
    # Construye la respuesta HTML directamente
    if user_info[5]=='admin':
            
        response_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Account - PolyFlix</title>
            <link rel="stylesheet" type="text/css" href="http://192.168.2.24/stylessesion.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
            
        </head>
        <body>
            <header>
                <div class="netflixLogo">
                    <a id="logo"><img src="http://192.168.2.24/logo_poly.png" alt="Logo Image"></a>
                </div>
            </header>
            <div class="container">
    <h2>My Account</h2>
        <div class="user-info">
            <div class="user-details">
                <p id="name">Name: {user_info[1]} {user_info[2]}</p>
                <p id="username">Username: {user_info[3]} ({user_info[5]})</p>
                <p id="email">Email: {user_info[6]}</p>
                <p id="add">Address: {user_info[12]}</p>
                <p id="phone">Phone: {user_info[7]}</p>
            </div>
            <div class="user-image">
                <img src="http://192.168.2.24/prf_pic/{user_info[3]}" alt="Profile Image" width="100" height="100">
            </div>
            </div>
            <div class="button-container">
                <input id="login" type="submit" value="Logout" onclick="redirectToLogin()">
                <input id="register" type="submit" value="Home" onclick="redirectToHome()">
            </div>
            <div class="button-container">
                <input id="google" type="submit" value="Google Analytics" onclick="redirectToGoogle()">
            </div>
        </div>

        
            <script>
                function redirectToLogin() {{
                    window.location.href = "cgi-bin/logout.py?id={user_info[8]}";
                }}
        
                function redirectToHome() {{
                    window.location.href = "http://192.168.2.24/home.html?id={user_info[8]}";
                }}
                function redirectToGoogle() {{
                    window.location.href = "https://analytics.google.com/analytics/web/#/p413735057/reports/intelligenthome?params=_u..nav%3Dmaui";
                }}
            </script>

            <footer>
                <p>&copy; PolyFlix, Inc.</p>
                <a href="https://www.facebook.com/profile.php?id=61553077526033&is_tour_dismissed=true"><i class="fab fa-facebook-square fa-2x logo" style="color: var(--dark);"></i></a>
                <a href="https://www.instagram.com/pol.yflix/"><i class="fab fa-instagram fa-2x logo" style="color: var(--dark);"></i></a>
                <a href="https://twitter.com/polyflix"><i class="fab fa-twitter fa-2x logo" style="color: var(--dark);"></i></a>
                <a href="https://youtube.com/@PolyFlix?si=leBztwkdjZxI9sJg"><i class="fab fa-youtube fa-2x logo" style="color: var(--dark);"></i></a>
                <p>Paul Aramberri Araiz &copy; 2023</p>
            </footer>
        </body>
        </html>
        """
    else:
        response_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Account - PolyFlix</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
            <link rel="stylesheet" type="text/css" href="http://192.168.2.24/stylessesion.css">
        </head>
        <body>
            <header>
                <div class="netflixLogo">
                    <a id="logo"><img src="http://192.168.2.24/logo_poly.png" alt="Logo Image"></a>
                </div>
            </header>
            <div class="container">
                <h2>My Account</h2>
                <div class="user-info">
                    <div class="user-details">
                        <p id="name">Name: {user_info[1]} {user_info[2]}</p>
                        <p id="username">Username: {user_info[3]} ({user_info[5]})</p>
                        <p id="email">Email: {user_info[6]}</p>
                        <p id="add">Address: {user_info[12]}</p>
                        <p id="phone">Phone: {user_info[7]}</p>
                    </div>
                    <div class="user-image">
                        <img src="http://192.168.2.24/prf_pic/{user_info[3]}" alt="Profile Image" width="100" height="100">
                    </div>
                </div>
                <div class="button-container">
                    <input id="login" type="submit" value="Logout" onclick="redirectToLogin()">
                    <input id="register" type="submit" value="Home" onclick="redirectToRegister()">
                </div>
            </div>

        
            <script>
                function redirectToLogin() {{
                    window.location.href = "cgi-bin/logout.py?id={user_info[8]}";
                }}
        
                function redirectToRegister() {{
                    window.location.href = "http://192.168.2.24/home.html?id={user_info[8]}";
                }}
            </script>

            <footer>
                <p>&copy; PolyFlix, Inc.</p>
                <a href="https://www.facebook.com/profile.php?id=61553077526033&is_tour_dismissed=true"><i class="fab fa-facebook-square fa-2x logo" style="color: var(--dark);"></i></a>
                <a href="https://www.instagram.com/pol.yflix/"><i class="fab fa-instagram fa-2x logo" style="color: var(--dark);"></i></a>
                <a href="https://twitter.com/polyflix"><i class="fab fa-twitter fa-2x logo" style="color: var(--dark);"></i></a>
                <a href="https://youtube.com/@PolyFlix?si=leBztwkdjZxI9sJg"><i class="fab fa-youtube fa-2x logo" style="color: var(--dark);"></i></a>
                <p>Paul Aramberri Araiz &copy; 2023</p>
            </footer>
        </body>
        </html>
        """

else:
    # Respuesta si el usuario no se encuentra
    response_html = "<h1>Usuario no encontrado</h1>"

# Imprime la respuesta HTML
print(response_html)
