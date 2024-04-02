from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置 MySQL 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# 创建数据库表格（如果尚未创建）
@app.before_first_request
def create_tables():
    db.create_all()

# 创建新用户
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'])
    password_user =User(password=data['password'])
    db.session.add(new_user)
    db.session.add(password_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

# 获取所有用户
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

# 更新用户
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.filter_by(id=id).first()
    if user:
        user.username = data['username']
        db.session.commit()
        return jsonify({"message": "User updated"})
    else:
        return jsonify({"message": "User not found"}), 404

# 删除用户
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"message": "User not found"}), 404

class SoilData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)

@app.route('/get_crop_recommendation', methods=['POST'])
def get_crop_recommendation():
    # 这里是模拟的逻辑。在实际应用中，应该根据输入的土壤数据来计算推荐的作物
    data = request.json
    recommended_crop = get_recommended_crop(data)
    return jsonify({"recommended_crop": recommended_crop})

def get_recommended_crop(soil_data):
    # 模拟根据土壤数据返回推荐作物的逻辑
    # 这里仅为示例，实际应用中应根据具体逻辑进行实现
    return "Wheat"  # 假设总是推荐小麦，可以使用模型中的predicted_label来替换"Wheat"，这里为了方便在本地调试

if __name__ == '__main__':
    app.run(debug=True)
