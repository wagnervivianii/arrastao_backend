from flask import redirect

def processar_callback(oauth, redirect_uri, conectar_db):

    token = oauth.google.authorize_access_token()
    user_info = oauth.google.userinfo()

    email = user_info.get("email")
    nome = user_info.get("name")
    nivel = user_info.get("nivel")

    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nivel_permissao FROM usuarios WHERE login = %s", (email,))
    resultado = cur.fetchone()
    cur.close()

    if resultado:
        url = f"http://localhost:3000/bem-vindo?nome={nome}&email={email}&nivel={nivel}"
        return redirect(url)
    else:
        return {"erro": "Usuário não autorizado. Email não encontrado no banco."}, 401
