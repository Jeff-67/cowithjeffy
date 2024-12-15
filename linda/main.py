from flask import Flask, request, jsonify, render_template, session
from slack_sdk import WebClient
import random
import os
app = Flask(__name__)
app.secret_key = os.getenv('SESSION_SECRET_KEY')  # Replace with a secure key
client = WebClient(token=os.getenv('SLACK_OAUTH_TOKEN'))
channel_id = "C0844RPP6Q3"
bot_name = "drafting_bot"

@app.before_request
def ensure_session_lists():
    # Initialize session variables if not already present
    if 'employees' not in session:
        session['employees'] = []
    if 'winners' not in session:
        session['winners'] = []

@app.route('/')
def index():
    # Pass session-stored employees to the template
    employees = session.get('employees', [])
    return render_template('index.html', employees=employees)

@app.route('/add_employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    employees_data = data.get('employees', [])
    
    if not employees_data:
        return jsonify({'success': False, 'message': 'No employees provided'})
    
    employees = session.get('employees', [])
    new_employees = []
    
    for emp in employees_data:
        name = emp.get('name', '').strip()
        experience = emp.get('experience', 0)  # 12 for senior, 3 for junior
        
        if name and not any(existing['name'] == name for existing in employees):
            new_employees.append({
                'name': name,
                'experience': experience
            })
    
    employees.extend(new_employees)
    session['employees'] = employees

    employee_names = [emp['name'] for emp in new_employees]
    message = f"✅ {len(new_employees)} 位員工已加入抽獎名單 ➡️\n{', '.join(employee_names)}"
    response = client.chat_postMessage(channel=channel_id, text=message, username=bot_name)

    return jsonify({'success': True, 'message': message})

@app.route('/select_winner', methods=['GET'])
def select_winner():
    try:
        prize_type = request.args.get('prize_type')
        num_winners = int(request.args.get('num_winners', 1))

        employees = session.get('employees', [])
        winners = session.get('winners', [])
        
        # Define experience requirements for each prize
        prize_requirements = {
            '60000': 12,  # Special prize: 1 year
            '50000': 12,  # First prize: 1 year
            '30000': 12,  # Second prize: 1 year
            '20000': 3,   # Third prize: 3 months
            '20000_extra': 3,  # Extra prize: 3 months
            '10000': 3    # Extra prize: 3 months
        }
        
        required_experience = prize_requirements.get(prize_type, 12)
        
        # Filter eligible candidates based on experience and previous wins
        eligible_candidates = [
            emp for emp in employees 
            if emp['experience'] >= required_experience and  # Check experience requirement
            not any(w['name'] == emp['name'] for w in winners)  # Check if not already won
        ]

        if len(eligible_candidates) < num_winners:
            return jsonify({'error': '符合資格的員工人數不足'})

        # Select winners
        selected_winners = random.sample(eligible_candidates, num_winners)
        
        # Add winners to the winners list
        for winner in selected_winners:
            winners.append({
                'name': winner['name'],
                'experience': winner['experience'],
                'prize_type': prize_type
            })

        session['winners'] = winners

        # Display prize amount (convert 20000_extra to 20000 for display)
        display_prize = prize_type.replace('_extra', '') if prize_type == '20000_extra' else prize_type
        winner_names = [w['name'] for w in selected_winners]
        message = f"🎉 {display_prize}得獎名單 ({num_winners}名) 🎉\n{', '.join(winner_names)}"
        response = client.chat_postMessage(channel=channel_id, text=message, username=bot_name)
        return jsonify({'winners': winner_names})
        
    except Exception as e:
        app.logger.error(f"Error selecting winner: {e}")
        return jsonify({'error': f'發生錯誤: {e}'}), 500

@app.route('/clear_candidates', methods=['POST'])
def clear_candidates():
    session['employees'] = []  # Clear employees from session
    return jsonify({'success': True, 'message': 'All candidates cleared.'})

@app.route('/reset_winners', methods=['POST'])
def reset_winners():
    session['winners'] = []  # Clear winners from session
    app.logger.info("Winners have been reset.")
    return jsonify({'success': True, 'message': 'All winners have been reset successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
