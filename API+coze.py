import json
import os
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

# Google Sheets 設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_json = os.environ.get('GOOGLE_CREDENTIALS')
if creds_json is None:
    raise ValueError("環境變數 GOOGLE_CREDENTIALS 未設定")

creds_dict = json.loads(creds_json)
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
        sub_category = data.get('sub_category', '')
        note = data.get('note', '')
        tz = timezone('Asia/Taipei')
        timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

        row = [user_id, timestamp, description, category, sub_category, note]
        worksheet.append_row(row)

        return jsonify({"status": "success", "message": "資料已成功寫入 Google Sheets"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
