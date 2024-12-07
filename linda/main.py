from flask import Flask, request, jsonify, render_template, session
import random

app = Flask(__name__)
app.secret_key = '0710'  # Replace with a secure key

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
    names = data.get('names', [])
    
    if not names:
        return jsonify({'success': False, 'message': 'No names provided'})
    
    valid_names = [name.strip() for name in names if name and name.strip()]
    employees = session.get('employees', [])
    new_employees = [name for name in valid_names if name not in employees]
    
    employees.extend(new_employees)
    session['employees'] = employees  # Save back to session

    # Debugging log to confirm addition
    app.logger.info(f"Employees after addition: {employees}")
    print(f"Employees after addition: {employees}")
    
    return jsonify({'success': True, 'message': f'{len(new_employees)} employees added.'})

@app.route('/select_winner', methods=['GET'])
def select_winner():
    try:
        prize_type = request.args.get('prize_type')
        num_winners = int(request.args.get('num_winners', 1))

        # Get employees and winners from session
        employees = session.get('employees', [])
        winners = session.get('winners', [])
        
        # Debugging log
        app.logger.info(f"Selecting winners for prize: {prize_type}. Number of winners requested: {num_winners}.")
        app.logger.info(f"Current winners: {winners}")
        print(f"Employees: {employees}")
        print(f"Winners: {winners}")
        
        # Get eligible candidates
        eligible_candidates = [e for e in employees if e not in [w['name'] for w in winners]]
        app.logger.info(f"Eligible candidates: {eligible_candidates}")
        print(f"Eligible candidates: {eligible_candidates}")
        if len(eligible_candidates) < num_winners:
            return jsonify({'error': 'Number of winners exceeds number of eligible employees'})

        # Select winners
        selected_winners = random.sample(eligible_candidates, num_winners)
        for winner in selected_winners:
            winners.append({'name': winner, 'prize_type': prize_type})

        session['winners'] = winners  # Save winners back to session

        app.logger.info(f"Selected winners: {selected_winners}")
        print(f"Selected winners: {selected_winners}")
        return jsonify({'winners': selected_winners})
    except Exception as e:
        app.logger.error(f"Error selecting winner: {e}")
        return jsonify({'error': f'An error occurred: {e}'}), 500

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
