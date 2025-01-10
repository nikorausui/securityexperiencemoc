

import streamlit as st
st.set_page_config(page_title="Advanced Ransomware Detection Training", layout="wide")
st.markdown(
    """
    <a href="http://localhost:5000" target="_blank" style="text-decoration:none;">
        <div style="
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-align: center;
            border-radius: 5px;
            cursor: pointer;
        ">
            Home
        </div>
    </a>
    """,
    unsafe_allow_html=True
)
st.title("Malware experience")
st.write("やってみよう")
import os
import time
import platform
import psutil
import datetime
import glob
from pathlib import Path
from cryptography.fernet import Fernet
import random
import string
import base64
from PIL import Image
import io

# 疑似ソースコード
SOURCE_CODE = """
def check_system_status():
    return os.system("systeminfo")

def network_connection():
    return socket.connect(("8.8.8.8", 53))

def process_data_stream():
    with open("data.bin", "rb") as f:
        return f.read()

def encrypt_files(directory):
    key = Fernet.generate_key()
    f = Fernet(key)
    for file in os.listdir(directory):
        with open(file, "rb") as data:
            encrypted = f.encrypt(data.read())

def send_system_info():
    return platform.system()

def create_backup():
    shutil.copy("source.txt", "backup.txt")

def modify_registry():
    return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE")

def check_vm_environment():
    return platform.processor()

def disable_system_restore():
    return os.system("vssadmin delete shadows /all /quiet")

def create_persistence():
    return os.system("schtasks /create /tn Task /tr calc.exe")
"""

# システム情報収集関数
def collect_system_info():
    try:
        username = os.getlogin()
    except:
        try:
            username = os.environ.get('USER', os.environ.get('USERNAME', 'Unknown'))
        except:
            username = 'Unknown'

    system_info = {
        "OS": platform.system(),
        "OSバージョン": platform.version(),
        "マシン": platform.machine(),
        "プロセッサ": platform.processor(),
        "メモリ使用率": f"{psutil.virtual_memory().percent}%",
        "CPU使用率": f"{psutil.cpu_percent()}%",
        "ユーザー名": username,
        "ホスト名": platform.node(),
        "実行時刻": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Python バージョン": platform.python_version(),
        "実行PID": os.getpid()
    }
    return system_info


# ディレクトリ構造取得関数
def scan_directory(path="test", depth=2):
    file_structure = []
    base_path = Path(path)
    
    if not os.path.exists(path):
        os.makedirs(path)
        # テスト用のダミーファイルを作成
        for i in range(5):
            dummy_file = base_path / f"dummy_file_{i}.txt"
            with open(dummy_file, "w") as f:
                f.write(f"This is test file {i}")
    
    for item in base_path.rglob("*"):
        relative_path = item.relative_to(base_path)
        if len(relative_path.parts) <= depth:
            file_info = {
                "名前": item.name,
                "タイプ": "フォルダ" if item.is_dir() else "ファイル",
                "サイズ": f"{os.path.getsize(item)}バイト" if item.is_file() else "-",
                "更新日時": datetime.datetime.fromtimestamp(os.path.getmtime(item)).strftime("%Y-%m-%d %H:%M:%S"),
                "パス": str(relative_path)
            }
            file_structure.append(file_info)
    
    return file_structure


def create_mock_files(directory="test"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Ubuntuの標準的なディレクトリ構造
    ubuntu_dirs = [
        'bin',
        'boot',
        'dev',
        'etc',
        'home/ubuntu',
        'lib',
        'media',
        'mnt',
        'opt',
        'proc',
        'root',
        'run',
        'sbin',
        'srv',
        'tmp',
        'usr/bin',
        'usr/lib',
        'usr/local',
        'var/log',
        'var/cache'
    ]

    # ディレクトリの作成
    for dir_path in ubuntu_dirs:
        full_path = os.path.join(directory, dir_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    # 一般的なUbuntuファイルの作成
    ubuntu_files = [
        ('etc/passwd', 'システムユーザー情報'),
        ('etc/hosts', 'ホスト名設定'),
        ('etc/fstab', 'ファイルシステム設定'),
        ('home/ubuntu/.bashrc', 'Bashの設定ファイル'),
        ('var/log/syslog', 'システムログ'),
        ('boot/grub/grub.cfg', 'GRUB設定'),
    ]

    def generate_random_content():
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(100))

    # ファイルの作成
    for file_path, desc in ubuntu_files:
        full_path = os.path.join(directory, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w') as f:
            content = f"# これは{desc}のシミュレーションファイルです。\n"
            content += generate_random_content()
            f.write(content)
        
        # ファイル作成日時をランダムに設定
        created_time = time.time() - random.randint(0, 30*24*60*60)
        os.utime(full_path, (created_time, created_time))

# 暗号化のビジュアライゼーション
# show_encryption_visualization 関数を以下のように修正
def execute_initial_analysis():
    """初期分析を実行する関数"""
    st.write("### 初期システム分析開始")
    col1, col2 = st.columns([3, 7])
    
    with col2:  # 右側（ログ表示）
        st.write("📝 システム分析ログ:")
        log_container = st.empty()
        log_content = []
        
        def update_log(new_line):
            log_content.append(new_line)
            displayed_logs = log_content[-14:]
            log_container.markdown(f""" 
            <div class="log-container" id="logContainer"> 
            {'<br>'.join(displayed_logs)} 
            </div>
            """, unsafe_allow_html=True)

        # システム情報の収集と表示
        update_log(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 🚀 初期分析を開始...")
        sys_info = collect_system_info()
        for key, value in sys_info.items():
            timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            update_log(f"[{timestamp}] 🔍 SYSTEM_INFO: {key}: {value}")
            time.sleep(0.2)

        # ファイル構造のスキャン
        update_log(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 📂 ファイルシステムスキャン開始...")
        files = scan_directory()
        for file in files:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            update_log(f"[{timestamp}] FILE_SCAN: Size: {file['サイズ']}  {file['パス']}  ")
            time.sleep(0.1)

        # マルウェアアクティビティのシミュレーション
        activities = [
            ("🔒 HOOK", "システムAPIをフック中..."),
            ("💾 ACCESS", "ファイルシステムにアクセス..."),
            ("🔑 CRYPTO", "暗号化キーを生成中..."),
            ("🔍 SCAN", "ファイル拡張子をスキャン中..."),
            ("⚙️ INIT", "暗号化アルゴリズムを初期化..."),
            ("📝 MODIFY", "ファイルヘッダを書き換え..."),
            ("💻 MEMORY", "バッファメモリを確保..."),
            ("🔄 CONVERT", "ファイル変換を実行中...")
        ]

        for activity_type, msg in activities:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            mem_usage = random.randint(50,80)
            threads = random.randint(1,4)
            update_log(f"[{timestamp}] {activity_type}: {msg}")
            update_log(f" └─ MEM: {mem_usage}% | Threads: {threads} | PID: {os.getpid()}")
            time.sleep(0.5)

        # CONVERTの後に暗号化プロセスの視覚化を表示
        # with col1:
        #     st.write("### 暗号化プロセス")


        # 残りのアクティビティ
        # remaining_activities = [
        #     ("🗑️ DELETE", "元ファイルを削除中..."),
        #     ("🧹 CLEAN", "痕跡を消去中...")
        # ]

        # for activity_type, msg in remaining_activities:
        #     timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        #     mem_usage = random.randint(50,80)
        #     threads = random.randint(1,4)
        #     update_log(f"[{timestamp}] {activity_type}: {msg}")
        #     update_log(f" └─ MEM: {mem_usage}% | Threads: {threads} | PID: {os.getpid()}")
        #     time.sleep(0.5)

        return log_content, log_container

def show_ransomware_screen():
    st.markdown("""
    <div style='
        background-color: #ff0000;
        color: white;
        padding: 15px;
        text-align: center;
        position: fixed;
        top: 5%;
        left: 2%;
        width: 95%;
        height: 95%;
        z-index: 9999;
        font-size: 20px;
    '>
        <h1 style='font-size: 24px;'>⚠️ YOUR FILES HAVE BEEN ENCRYPTED ⚠️</h1>
        <p>This is an educational demonstration.</p>
        <p>In a real ransomware attack, your files would be locked now.</p>
        <h2 style='font-size: 20px;'>Bitcoin payment required: 0.5 BTC</h2>
        <p>Time remaining: 72:00:00</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    scan_directory()
    create_mock_files()


    st.markdown("""
        <style>
            .log-container {
                height: 400px !important;  /* 必ず200pxを適用 */
                overflow-y: scroll;
                background-color: black;
                color: #00ff00;
                padding: 0px;
                font-family: 'Courier New', monospace;
                border-radius: 5px;
                white-space: pre-wrap;
                word-wrap: break-word;
                flex-direction: column-reverse;
            }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["実行タブ", "マルウェアファイル", "セキュリティ設定"])
    
    with tab1:
        col1, col2 = st.columns([9, 1])
        with col1:
            if st.button("疑似ランサムウェアを実行"):
                # 初期分析を必ず実行
                log_content, log_container = execute_initial_analysis()
         
                
                def update_log(new_line):
                    log_content.append(new_line)
                    displayed_logs = log_content[-14:]
                    log_container.markdown(f""" 
                    <div class="log-container" id="logContainer"> 
                    {'<br>'.join(displayed_logs)} 
                    </div>
                    """, unsafe_allow_html=True)
                # 選択された関数のチェック
                if st.session_state.get('detected_function') == 'encrypt_files':
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                    log_content.append(f"[{timestamp}] 🛡️ 警告: 暗号化機能を検知")
                    log_content.append(f"[{timestamp}] 🚫 実行をブロック")
                    log_container.markdown(f"""
                        <div class="log-container">
                            {'<br>'.join(log_content[-14:])}
                        </div>
                        """, unsafe_allow_html=True)
                    st.success("🛡️ 暗号化機能を検知！攻撃をブロックしました")
                else:

                    # activities = [
                    #     ("🔒 HOOK", "システムAPIをフック中..."),
                    #     ("💾 ACCESS", "ファイルシステムにアクセス..."),
                    #     ("🔑 CRYPTO", "暗号化キーを生成中..."),
                    #     ("🔍 SCAN", "ファイル拡張子をスキャン中..."),
                    #     ("⚙️ INIT", "暗号化アルゴリズムを初期化..."),
                    #     ("📝 MODIFY", "ファイルヘッダを書き換え..."),
                    #     ("💻 MEMORY", "バッファメモリを確保..."),
                    #     ("🔄 CONVERT", "ファイル変換を実行中...")
                    # ]

                    # for activity_type, msg in activities:
                    #     timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                    #     mem_usage = random.randint(50,80)
                    #     threads = random.randint(1,4)
                    #     update_log(f"[{timestamp}] {activity_type}: {msg}")
                    #     update_log(f" └─ MEM: {mem_usage}% | Threads: {threads} | PID: {os.getpid()}")
                    #     time.sleep(0.5)

                    # # CONVERTの後に暗号化プロセスの視覚化を表示
                 
      
                    progress_container = st.container()
                    with progress_container:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        
                        # 10%ごとにファイル名の暗号化を表示
                        if i % 10 == 0:
                            original_file = f"document_{i//10}.txt"
                            encrypted_file = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".encrypted"
                        
                        status_text.code(f"""
                        ┌── Encryption Status ───┐
                        │ Progress: {i+1:>3}%       │
                        │ Files: {i//10 + 1:>2}/10        │
                        │ [{('#'*(i//10)).ljust(10, '.')}] │
                        │                         │
                        │ Current File:          │
                        │ {original_file}        │
                        │    ↓                   │
                        │ {encrypted_file}       │
                        └─────────────────────┘
                        """)
                        time.sleep(0.05)

                    # 残りのアクティビティ
                    remaining_activities = [
                        ("🗑️ DELETE", "元ファイルを削除中..."),
                        ("🧹 CLEAN", "痕跡を消去中...")
                    ]

                    for activity_type, msg in remaining_activities:
                        timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                        mem_usage = random.randint(50,80)
                        threads = random.randint(1,4)
                        update_log(f"[{timestamp}] {activity_type}: {msg}")
                        update_log(f" └─ MEM: {mem_usage}% | Threads: {threads} | PID: {os.getpid()}")
                        time.sleep(0.5)
                    
                    show_ransomware_screen()

    
    with tab2:
        st.header("ソースファイル")
        
        # 最初にバイナリ表示
        st.code("""
        malware: ELF 64-bit LSB executable, x86-64, version 1 (SYSV)
        00000000  7f 45 4c 46 02 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
        00000010  02 00 3e 00 01 00 00 00  30 44 40 00 00 00 00 00  |..>.....0D@.....|
        00000020  40 00 00 00 00 00 00 00  e8 31 00 00 00 00 00 00  |@........1......|
        00000030  00 00 00 00 40 00 38 00  0b 00 40 00 24 00 23 00  |....@.8...@.$.#.|
        ...
        """, language='text')

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Fileについて調べる"):
                st.info("File情報取得中...")
                time.sleep(1)
                st.code("""
                File: malware
                Type: ELF 64-bit LSB executable, x86-64, version 1 (SYSV)
                動的リンク (uses shared libs)
                コンパイラ: GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
                セキュリティ: NX enabled
                サイズ: 8.2MB
                作成日時: 2025-01-07 19:00:00
                """, language='text')
        
        with col2:
            if st.button("逆コンパイルする"):
                st.info("逆コンパイル中...")
                time.sleep(3)
                st.code(SOURCE_CODE, language='python')
                st.info("👆 逆アセンブルされたコードをみてセキュリティ設定から不審な関数を選択してください")
        
    with tab3:
        st.header("セキュリティ設定")
        
        suspicious_functions = [
            "選択してください",
            "check_system_status",
            "network_connection",
            "process_data_stream",
            "encrypt_files",
            "send_system_info",
            "create_backup",
            "modify_registry",
            "check_vm_environment",
            "disable_system_restore",
            "create_persistence"
        ]
        
        st.session_state.detected_function = st.selectbox(
            "検知する不審な関数を選択:",
            suspicious_functions
        )
        
        if st.session_state.detected_function != "選択してください":
            st.write(f"選択された関数: {st.session_state.detected_function}")
            
            function_details = {
                "encrypt_files": {
                    "リスク": "高",
                    "説明": "ファイルの暗号化を行う関数。ランサムウェアの主要な機能。",
                    "検知方法": "暗号化APIの使用とファイル操作の組み合わせを監視"
                },
                "modify_registry": {
                    "リスク": "高",
                    "説明": "レジストリの改変を行う関数。マルウェアの永続化に使用される可能性。",
                    "検知方法": "レジストリ操作APIの監視"
                },
                "disable_system_restore": {
                    "リスク": "高",
                    "説明": "システムリストアを無効化する関数。復旧を妨害する。",
                    "検知方法": "システム設定変更の監視"
                },
                "create_persistence": {
                    "リスク": "中",
                    "説明": "自動実行の設定を行う関数。マルウェアの永続化に使用。",
                    "検知方法": "スケジューラーAPIの監視"
                }
            }
            
            if st.session_state.detected_function in function_details:
                details = function_details[st.session_state.detected_function]
                st.write("### 関数の詳細分析")
                st.write(f"**リスクレベル:** {details['リスク']}")
                st.write(f"**説明:** {details['説明']}")
                st.write(f"**検知方法:** {details['検知方法']}")

if __name__ == "__main__":
    main()
