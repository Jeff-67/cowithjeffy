from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import random
import os

app = Flask(__name__, instance_path=os.path.join('/tmp', 'instance'))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prize_type = db.Column(db.String(10), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=[e.name for e in employees])

@app.route('/add_employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    names = data.get('names', [])
    
    if not names:
        return jsonify({'success': False, 'message': 'No names provided'})
    
    valid_names = [name.strip() for name in names if name and name.strip()]
    existing_names = {e.name for e in Employee.query.all()}
    new_employees = [name for name in valid_names if name not in existing_names]
    
    for name in new_employees:
        db.session.add(Employee(name=name))
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'{len(new_employees)} employees added.'})

@app.route('/select_winner', methods=['GET'])
def select_winner():
    prize_type = request.args.get('prize_type')
    num_winners = int(request.args.get('num_winners', 1))

    # Determine eligible candidates
    ineligible_names = {w.name for w in Winner.query.filter(Winner.prize_type != prize_type).all()}
    available_candidates = Employee.query.filter(Employee.name.not_in(ineligible_names)).all()
    
    if len(available_candidates) < num_winners:
        return jsonify({'error': 'Number of winners exceeds number of eligible employees'})

    winners = random.sample([e.name for e in available_candidates], num_winners)

    # Save winners to database
    for winner in winners:
        db.session.add(Winner(name=winner, prize_type=prize_type))
    db.session.commit()

    return jsonify({'winners': winners})

@app.route('/reset', methods=['POST'])
def reset():
    db.session.query(Winner).delete()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Winners reset successfully'})

@app.route('/clear_candidates', methods=['POST'])
def clear_candidates():
    try:
        # Delete all employees from the database
        logging.info("Attempting to delete all employees.")
        num_deleted = Employee.query.delete()
        db.session.commit()

        logging.info(f"Successfully deleted {num_deleted} candidates.")
        return jsonify({'success': True, 'message': f'All {num_deleted} candidates cleared.'})

    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        logging.error(f"Error deleting employees: {e}")
        return jsonify({'success': False, 'message': 'Failed to clear candidates due to a server error.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
