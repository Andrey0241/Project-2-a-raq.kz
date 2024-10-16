from flask import Blueprint, request, jsonify
from models import db, User, Ad, Comment
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
auth_bp = Blueprint('auth', __name__)

# 1. User Registration
@auth_bp.route('/auth/users/', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        phone=data['phone'],
        password=data['password'],
        name=data['name'],
        city=data['city']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id}), 200

# 2. User Login
@auth_bp.route('/auth/users/login', methods=['POST'])
def login_user():
    data = request.form
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# 3. Update User Data
@auth_bp.route('/auth/users/me', methods=['PATCH'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.query.get(user_id)

    if user:
        user.phone = data.get('phone', user.phone)
        user.name = data.get('name', user.name)
        user.city = data.get('city', user.city)

        db.session.commit()
        return jsonify({"message": "User data updated successfully"}), 200
    return jsonify({"message": "User not found"}), 404

# 4. Get User Data
@auth_bp.route('/auth/users/me', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "name": user.name,
            "city": user.city
        }), 200
    return jsonify({"message": "User not found"}), 404

# 5. Create Ad
@auth_bp.route('/shanyraks/', methods=['POST'])
@jwt_required()
def create_ad():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_ad = Ad(
        user_id=user_id,
        type=data['type'],
        price=data['price'],
        address=data['address'],
        area=data['area'],
        rooms_count=data['rooms_count'],
        description=data['description']
    )
    db.session.add(new_ad)
    db.session.commit()
    return jsonify({"id": new_ad.id}), 200

# 6. Get Ad Details
@auth_bp.route('/shanyraks/<int:id>', methods=['GET'])
def get_ad(id):
    ad = Ad.query.get(id)
    if ad:
        return jsonify({
            "id": ad.id,
            "type": ad.type,
            "price": ad.price,
            "address": ad.address,
            "area": ad.area,
            "rooms_count": ad.rooms_count,
            "description": ad.description,
            "user_id": ad.user_id,
            "total_comments": Comment.query.filter_by(ad_id=ad.id).count()  # Count comments
        }), 200
    return jsonify({"message": "Ad not found"}), 404

# 7. Update Ad
@auth_bp.route('/shanyraks/<int:id>', methods=['PATCH'])
@jwt_required()
def update_ad(id):
    user_id = get_jwt_identity()
    ad = Ad.query.get(id)

    if ad and ad.user_id == user_id:
        data = request.get_json()
        ad.type = data.get('type', ad.type)
        ad.price = data.get('price', ad.price)
        ad.address = data.get('address', ad.address)
        ad.area = data.get('area', ad.area)
        ad.rooms_count = data.get('rooms_count', ad.rooms_count)
        ad.description = data.get('description', ad.description)

        db.session.commit()
        return jsonify({"message": "Ad updated successfully"}), 200
    return jsonify({"message": "Ad not found or you do not have permission"}), 404

# 8. Delete Ad
@auth_bp.route('/shanyraks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ad(id):
    user_id = get_jwt_identity()
    ad = Ad.query.get(id)

    if ad and ad.user_id == user_id:
        db.session.delete(ad)
        db.session.commit()
        return jsonify({"message": "Ad deleted successfully"}), 200
    return jsonify({"message": "Ad not found or you do not have permission"}), 404

# 9. Add Comment
@auth_bp.route('/shanyraks/<int:id>/comments', methods=['POST'])
@jwt_required()
def add_comment(id):
    user_id = get_jwt_identity()
    data = request.get_json()
    new_comment = Comment(
        ad_id=id,
        user_id=user_id,
        content=data['content']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully"}), 200

# 10. Get Comments for Ad
@auth_bp.route('/shanyraks/<int:id>/comments', methods=['GET'])
def get_comments(id):
    comments = Comment.query.filter_by(ad_id=id).all()
    return jsonify({
        "comments": [
            {
                "id": comment.id,
                "content": comment.content,
                "created_at": comment.created_at.isoformat(),
                "author_id": comment.user_id
            } for comment in comments
        ]
    }), 200

# 11. Update Comment
@auth_bp.route('/shanyraks/<int:id>/comments/<int:comment_id>', methods=['PATCH'])
@jwt_required()
def update_comment(id, comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if comment and comment.user_id == user_id:
        data = request.get_json()
        comment.content = data.get('content', comment.content)
        db.session.commit()
        return jsonify({"message": "Comment updated successfully"}), 200
    return jsonify({"message": "Comment not found or you do not have permission"}), 404

# 12. Delete Comment
@auth_bp.route('/shanyraks/<int:id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id, comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if comment and comment.user_id == user_id:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comment deleted successfully"}), 200
    return jsonify({"message": "Comment not found or you do not have permission"}), 404
