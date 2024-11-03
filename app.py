from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pool_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    table = db.Column(db.String(50), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    pool_tables = {
        "Table 1": Player.query.filter_by(table="Table 1").all(),
        "Table 2": Player.query.filter_by(table="Table 2").all(),
        "Table 3": Player.query.filter_by(table="Table 3").all(),
    }
    return render_template('index.html', pool_tables=pool_tables)

@app.route('/add_player', methods=['POST'])
def add_player():
    table = request.form.get('table')
    player_name = request.form.get('player_name')
    if table and player_name:
        new_player = Player(name=player_name, table=table)
        db.session.add(new_player)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove_player', methods=['POST'])
def remove_player():
    player_name = request.form.get('player_name')
    player = Player.query.filter_by(name=player_name).first()
    if player:
        db.session.delete(player)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
