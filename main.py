import os
import subprocess
from typing import List, Dict
from dataclasses import dataclass
from flask import Flask, redirect, render_template

app = Flask(__name__)

@dataclass
class AppConfig:
    name: str
    path: str
    port: int
    type: str

class AppManager:
    def __init__(self):
        self.apps: Dict[str, AppConfig] = {}
        self.load_config()

    def load_config(self) -> None:
        # 設定ファイルから読み込むことも可能
        self.apps = {
            'streamlit_apps': [
                AppConfig(
                    name="ランサムウェア",
                    path=os.getenv("STREAMLIT_PATH", "test.py"),
                    port=int(os.getenv("STREAMLIT_PORT", 8501)),
                    type="streamlit"
                ),
                # 他のStreamlitアプリを追加可能
                AppConfig(
                    name="ぺネトレ",
                    path="pentest.py",
                    port=8502,
                    type="streamlit"
                )
            ],
            'flask_apps': [
                AppConfig(
                    name="CTFアプリ",
                    path=os.getenv("CTF_PATH", "ctf.py"),
                    port=int(os.getenv("CTF_PORT", 5001)),
                    type="flask"
                )
            ]
        }

    def start_all_apps(self) -> None:
        for app_type, apps in self.apps.items():
            for app in apps:
                self._start_app(app)

    def _start_app(self, app: AppConfig) -> None:
        log_file = open(f"{app.name}.log", "w")
        if app.type == "streamlit":
            subprocess.Popen(
                ["streamlit", "run", app.path, "--server.port", str(app.port)],
                stdout=log_file,
                stderr=log_file
            )
        elif app.type == "flask":
            subprocess.Popen(
                ["python3", app.path],
                stdout=log_file,
                stderr=log_file
            )

app_manager = AppManager()

@app.route('/')
def index() -> str:
    """動的に生成されたパネル形式のホーム画面"""
    return render_template(
        "index1.html",
        streamlit_apps=app_manager.apps['streamlit_apps'],
        flask_apps=app_manager.apps['flask_apps']
    )

@app.route('/<app_type>/<app_name>')
def redirect_to_app(app_type: str, app_name: str) -> str:
    """各アプリケーションへのリダイレクト"""
    for app in app_manager.apps[f"{app_type}_apps"]:
        if app.name == app_name:
            return redirect(f"http://localhost:{app.port}")
    return "アプリケーションが見つかりません", 404

# if __name__ == '__main__':
#     app_manager.start_all_apps()
#     app.run(port=int(os.getenv("FLASK_PORT", 5000)))

# localhost の代わりに 0.0.0.0 を使用
if __name__ == '__main__':
    app_manager.start_all_apps()
    app.run(host='0.0.0.0', port=int(os.getenv("FLASK_PORT", 5000)))

# リダイレクト時のホスト名も変更
@app.route('/<app_type>/<app_name>')
def redirect_to_app(app_type: str, app_name: str) -> str:
    for app in app_manager.apps[f"{app_type}_apps"]:
        if app.name == app_name:
            return redirect(f"http://0.0.0.0:{app.port}")
    return "アプリケーションが見つかりません", 404
