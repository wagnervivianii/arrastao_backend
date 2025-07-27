from flask import redirect

def processar_callback(oauth, redirect_uri_base, conectar_db):
    # Autentica com o Google
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.userinfo()

    email = user_info.get("email")
    nome = user_info.get("name")

    # Consulta o banco para obter o nível de permissão
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nivel_permissao FROM usuarios WHERE login = %s", (email,))
    resultado = cur.fetchone()
    cur.close()

    if resultado:
        _, nivel = resultado  # nível vem da consulta, não do Google
        # Monta a URL de redirecionamento para o frontend
        url = f"{redirect_uri_base}/bem-vindo?nome={nome}&email={email}&nivel={nivel}"

        return redirect(url)
    else:
        return {"erro": "Usuário não autorizado. Email não encontrado no banco."}, 401
