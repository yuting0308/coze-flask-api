from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

app = Flask(__name__)

# Google Sheets 設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# 從環境變數讀取金鑰
json_str = os.environ.get('GOOGLE_CREDENTIALS')
if not json_str:
    raise ValueError("未找到 GOOGLE_CREDENTIALS 環境變數，請確認 Render 環境設定")

creds_dict = json.loads(json_str)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
spreadsheet = client.open('同行者心知AI用戶資料庫')
worksheet = spreadsheet.sheet1

@app.route('/log_discomfort', methods=['POST'])
def log_discomfort():
    try:
        data = request.json
        user_id = data.get('user_id', '未知使用者')
        description = data.get('description', '')
        category = data.get('category', '')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        row = [user_id, timestamp, description, category]
        worksheet.append_row(row)

        return jsonify({"status": "success", "message": "資料已成功寫入 Google Sheets"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
