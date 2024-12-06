from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Define lists to store employee names and winners
employees = []
winners_10000 = []
winners_5000 = []
winners_1000 = []

@app.route('/')
def index():
    return render_template('index.html', employees=employees)

# Route for adding employees
@app.route('/add_employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    names = data.get('names', [])
    
    if not names:
        return jsonify({'success': False, 'message': 'No names provided'})
    
    # Filter out empty names and add valid ones
    valid_names = [name.strip() for name in names if name and name.strip()]
    employees.extend(valid_names)
    
    return jsonify({'success': True})

# Route for running the lottery
@app.route('/select_winner')
def select_winner():
    prize_type = request.args.get('prize_type')
    num_winners = int(request.args.get('num_winners', 1))
    
    # Get available candidates based on prize type
    available_candidates = []
    if prize_type == '10000':
        # For 10000, exclude those who won 5000
        available_candidates = [emp for emp in employees if emp not in winners_5000 and emp not in winners_1000]
    elif prize_type == '5000':
        # For 5000, exclude those who won 10000
        available_candidates = [emp for emp in employees if emp not in winners_10000 and emp not in winners_1000]
    else:  # 1000
        # For 1000, can select anyone
        available_candidates = [emp for emp in employees if emp not in winners_10000 and emp not in winners_5000]
    
    if not available_candidates:
        return jsonify({'error': 'No eligible employees in the pool'})
    
    if num_winners > len(available_candidates):
        return jsonify({'error': 'Number of winners exceeds number of eligible employees'})
    
    winners = random.sample(available_candidates, num_winners)
    
    # Store winners in appropriate category
    if prize_type == '10000':
        winners_10000.extend(winners)
    elif prize_type == '5000':
        winners_5000.extend(winners)
    else:
        winners_1000.extend(winners)
    
    return jsonify({'winners': winners})

@app.route('/bulk_add', methods=['POST'])
def bulk_add():
    data = request.get_json()
    names = data.get('employee_names', '')
    if names:
        new_employees = [name.strip() for name in names.splitlines() if name.strip()]
        global employees
        employees.extend(new_employees)
        return jsonify({'success': True, 'employees': employees})
    else:
        return jsonify({'error': 'No names provided'})

if __name__ == '__main__':
    app.run(debug=True)