from flask import Flask, render_template, jsonify, request
import time
import threading

app = Flask(__name__)

# 正しいユーザー名とパスワード
correct_username = "admin"
correct_password = "admin123"

# 辞書ファイル（リスト）を定義
username_dict1 = ["admin", "user", "manager", "guest"]
username_dict2 = ["superuser", "root", "operator", "admin"]

password_dict1 = ["password123", "admin", "letmein", "123456"]
password_dict2 = ["qwerty", "abc123", "football", "admin123"]
password_dict3 = ["pass", "xxx", "r3ff", "kkd93"]
password_dict4 = ["asaerty", "fd23", "fdijifll", "afdfn123"]

# グローバル変数で攻撃の進行状況を保持
attack_logs = []
login_successful = False

# 辞書型攻撃のシミュレーションを行う関数
def simulate_attack(username_dict, password_dict):
    global attack_logs, login_successful
    attack_logs = []
    login_successful = False
    for username in username_dict:
        for password in password_dict:
            if login_successful:
                return
            time.sleep(1)  # 1秒ごとに試す
            log_entry = f"[*] Trying username: {username}, password: {password}"
            attack_logs.append(log_entry)
            if username == correct_username and password == correct_password:
                attack_logs.append(f"[+] Success! Username: {username}, Password: {password}")
                login_successful = True
                return

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_attack', methods=['POST'])
def start_attack():
    data = request.json
    username_dict_choice = data.get('username_dict')
    password_dict_choice = data.get('password_dict')

    # 辞書選択に応じた辞書リストを取得
    username_dict = username_dict1 if username_dict_choice == '1' else username_dict2
    password_dict = password_dict1 if password_dict_choice == '1' else password_dict2

    # 攻撃を別スレッドで実行
    thread = threading.Thread(target=simulate_attack, args=(username_dict, password_dict))
    thread.start()
    return jsonify({"message": "Attack started"})

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({"logs": attack_logs})

# Flask サーバー起動ロジック
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # ポート 5001 で起動
