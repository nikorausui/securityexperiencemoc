import streamlit as st
import time
import threading

# 正しいユーザー名とパスワード
correct_username = "admin"
correct_password = "admin123"

# 辞書ファイル（リスト）を定義
username_dict1 = ["admin", "user", "manager", "guest"]
username_dict2 = ["superuser", "root", "operator", "admin"]

password_dict1 = ["password123", "admin", "letmein", "123456"]
password_dict2 = ["qwerty", "abc123", "football", "admin123"]

# グローバル変数で攻撃の進行状況を保持
attack_logs = []
login_successful = False
thread_running = False  # スレッド実行状態の確認用

# 辞書型攻撃のシミュレーションを行う関数
def simulate_attack(username_dict, password_dict):
    global attack_logs, login_successful, thread_running
    attack_logs = []
    login_successful = False
    thread_running = True
    for username in username_dict:
        for password in password_dict:
            if login_successful:
                thread_running = False
                return
            time.sleep(1)  # 1秒ごとに試す
            log_entry = f"[*] Trying username: {username}, password: {password}"
            attack_logs.append(log_entry)
            if username == correct_username and password == correct_password:
                attack_logs.append(f"[+] Success! Username: {username}, Password: {password}")
                login_successful = True
                thread_running = False
                return
    thread_running = False

# 攻撃を別スレッドで実行する関数
def start_attack_thread(username_dict, password_dict):
    thread = threading.Thread(target=simulate_attack, args=(username_dict, password_dict))
    thread.start()

# ストリームリットのUI構築
st.title("辞書型攻撃シミュレーション")

# 攻撃のオプションを選択
st.sidebar.header("設定")
username_dict_choice = st.sidebar.radio(
    "ユーザー名辞書を選択",
    ("1: username_dict1", "2: username_dict2")
)

password_dict_choice = st.sidebar.radio(
    "パスワード辞書を選択",
    ("1: password_dict1", "2: password_dict2")
)

# 選択に基づいて辞書リストを取得
username_dict = username_dict1 if username_dict_choice.startswith("1") else username_dict2
password_dict = password_dict1 if password_dict_choice.startswith("1") else password_dict2

# 攻撃開始ボタン
if st.button("攻撃開始", key="start_attack"):
    if thread_running:
        st.warning("攻撃が既に実行中です。ログを確認してください。")
    else:
        start_attack_thread(username_dict, password_dict)
        st.success("攻撃を開始しました。ログを確認してください！")

# 攻撃ログの表示
st.subheader("攻撃ログ")
if st.button("ログ更新", key="update_logs"):
    if len(attack_logs) > 0:
        st.text_area("ログ内容", "\n".join(attack_logs), height=300)
    if login_successful:
        st.success("攻撃が成功しました！")
    elif thread_running:
        st.info("攻撃が進行中です...")
    else:
        st.info("攻撃が終了しましたが、成功しませんでした。")
