# Employee Lottery System

A web-based lottery system built with Flask that allows organizations to conduct prize drawings for employees with different prize tiers.

## Features

- **Bulk Employee Entry**: Add multiple employees at once using a text area input
- **Multiple Prize Tiers**: Support for three prize levels:
  - $10,000 tier
  - $5,000 tier
  - $1,000 tier
- **Prize Rules**:
  - 10,000 winners cannot win 5,000 or 1,000 prizes
  - 5,000 winners cannot win 10,000 or 1,000 prizes
  - 1,000 winners cannot win 10,000 or 5,000 prizes
- **Dynamic UI**: Animated winner selection with visual feedback
- **Responsive Design**: Works on both desktop and mobile devices

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Design**: Custom CSS with animations

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```

2. Install the required dependencies:
   ```bash
   pip install flask
   ```

3. Run the application:
   ```bash
   python linda/main.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```
