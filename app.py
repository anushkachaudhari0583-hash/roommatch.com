from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random
from typing import List, Dict, Any

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///roommatch.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:5500', 'http://localhost:5500'])

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    sent_matches = db.relationship('Match', foreign_keys='Match.user1_id', backref='user1', lazy='dynamic')
    received_matches = db.relationship('Match', foreign_keys='Match.user2_id', backref='user2', lazy='dynamic')

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Basic Info
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    occupation = db.Column(db.String(100))
    education = db.Column(db.String(100))
    
    # Living Preferences
    budget_min = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    location_preference = db.Column(db.String(200))
    room_type = db.Column(db.String(50))  # single, shared, studio
    
    # Lifestyle Preferences (stored as JSON)
    lifestyle_preferences = db.Column(db.Text)  # JSON string
    
    # Compatibility Factors
    cleanliness_level = db.Column(db.Integer)  # 1-5 scale
    social_level = db.Column(db.Integer)  # 1-5 scale
    noise_tolerance = db.Column(db.Integer)  # 1-5 scale
    pet_preference = db.Column(db.String(20))  # yes, no, maybe
    smoking_preference = db.Column(db.String(20))  # yes, no, maybe
    
    # Bio and Additional Info
    bio = db.Column(db.Text)
    interests = db.Column(db.Text)  # JSON string
    deal_breakers = db.Column(db.Text)  # JSON string
    
    # Profile Status
    is_complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    compatibility_score = db.Column(db.Float, nullable=False)
    match_reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure unique matches
    __table_args__ = (db.UniqueConstraint('user1_id', 'user2_id', name='unique_match'),)

# Utility Functions
def calculate_compatibility_score(profile1: UserProfile, profile2: UserProfile) -> float:
    """Calculate compatibility score between two user profiles"""
    score = 0.0
    total_weight = 0.0
    
    # Budget compatibility (30% weight)
    if profile1.budget_min and profile1.budget_max and profile2.budget_min and profile2.budget_max:
        budget_overlap = min(profile1.budget_max, profile2.budget_max) - max(profile1.budget_min, profile2.budget_min)
        budget_range1 = profile1.budget_max - profile1.budget_min
        budget_range2 = profile2.budget_max - profile2.budget_min
        
        if budget_overlap > 0:
            budget_score = budget_overlap / max(budget_range1, budget_range2)
            score += budget_score * 0.3
        total_weight += 0.3
    
    # Lifestyle compatibility (40% weight)
    lifestyle_score = 0.0
    lifestyle_factors = ['cleanliness_level', 'social_level', 'noise_tolerance']
    
    for factor in lifestyle_factors:
        val1 = getattr(profile1, factor)
        val2 = getattr(profile2, factor)
        if val1 and val2:
            factor_score = 1 - abs(val1 - val2) / 4  # Normalize to 0-1
            lifestyle_score += factor_score
    
    if lifestyle_factors:
        lifestyle_score /= len(lifestyle_factors)
        score += lifestyle_score * 0.4
        total_weight += 0.4
    
    # Pet preference compatibility (10% weight)
    if profile1.pet_preference and profile2.pet_preference:
        if profile1.pet_preference == profile2.pet_preference:
            score += 0.1
        elif 'maybe' in [profile1.pet_preference, profile2.pet_preference]:
            score += 0.05
        total_weight += 0.1
    
    # Smoking preference compatibility (10% weight)
    if profile1.smoking_preference and profile2.smoking_preference:
        if profile1.smoking_preference == profile2.smoking_preference:
            score += 0.1
        elif 'maybe' in [profile1.smoking_preference, profile2.smoking_preference]:
            score += 0.05
        total_weight += 0.1
    
    # Location preference (10% weight)
    if profile1.location_preference and profile2.location_preference:
        if profile1.location_preference.lower() == profile2.location_preference.lower():
            score += 0.1
        total_weight += 0.1
    
    # Normalize score
    if total_weight > 0:
        score = score / total_weight
    
    return min(score, 1.0)  # Cap at 1.0

def generate_match_reason(profile1: UserProfile, profile2: UserProfile, score: float) -> str:
    """Generate a human-readable reason for the match"""
    reasons = []
    
    # Budget compatibility
    if profile1.budget_min and profile1.budget_max and profile2.budget_min and profile2.budget_max:
        budget_overlap = min(profile1.budget_max, profile2.budget_max) - max(profile1.budget_min, profile2.budget_min)
        if budget_overlap > 0:
            reasons.append("Similar budget range")
    
    # Lifestyle factors
    if abs(profile1.cleanliness_level - profile2.cleanliness_level) <= 1:
        reasons.append("Compatible cleanliness standards")
    
    if abs(profile1.social_level - profile2.social_level) <= 1:
        reasons.append("Similar social preferences")
    
    if abs(profile1.noise_tolerance - profile2.noise_tolerance) <= 1:
        reasons.append("Compatible noise tolerance")
    
    # Pet preference
    if profile1.pet_preference == profile2.pet_preference and profile1.pet_preference != 'maybe':
        reasons.append(f"Both {profile1.pet_preference} pets")
    
    # Location
    if profile1.location_preference and profile2.location_preference:
        if profile1.location_preference.lower() == profile2.location_preference.lower():
            reasons.append("Same location preference")
    
    if not reasons:
        reasons.append("Good overall compatibility")
    
    return ", ".join(reasons[:3])  # Limit to 3 reasons

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Roommatch API is running'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone')
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_verified': user.is_verified
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profile_data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'is_verified': user.is_verified
            }
        }
        
        if user.profile:
            profile_data['profile'] = {
                'age': user.profile.age,
                'gender': user.profile.gender,
                'occupation': user.profile.occupation,
                'education': user.profile.education,
                'budget_min': user.profile.budget_min,
                'budget_max': user.profile.budget_max,
                'location_preference': user.profile.location_preference,
                'room_type': user.profile.room_type,
                'cleanliness_level': user.profile.cleanliness_level,
                'social_level': user.profile.social_level,
                'noise_tolerance': user.profile.noise_tolerance,
                'pet_preference': user.profile.pet_preference,
                'smoking_preference': user.profile.smoking_preference,
                'bio': user.profile.bio,
                'is_complete': user.profile.is_complete,
                'lifestyle_preferences': json.loads(user.profile.lifestyle_preferences) if user.profile.lifestyle_preferences else None,
                'interests': json.loads(user.profile.interests) if user.profile.interests else None,
                'deal_breakers': json.loads(user.profile.deal_breakers) if user.profile.deal_breakers else None
            }
        
        return jsonify(profile_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['POST', 'PUT'])
@jwt_required()
def create_update_profile():
    """Create or update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Check if profile exists
        if user.profile:
            profile = user.profile
        else:
            profile = UserProfile(user_id=user_id)
            db.session.add(profile)
        
        # Update profile fields
        profile.age = data.get('age')
        profile.gender = data.get('gender')
        profile.occupation = data.get('occupation')
        profile.education = data.get('education')
        profile.budget_min = data.get('budget_min')
        profile.budget_max = data.get('budget_max')
        profile.location_preference = data.get('location_preference')
        profile.room_type = data.get('room_type')
        profile.cleanliness_level = data.get('cleanliness_level')
        profile.social_level = data.get('social_level')
        profile.noise_tolerance = data.get('noise_tolerance')
        profile.pet_preference = data.get('pet_preference')
        profile.smoking_preference = data.get('smoking_preference')
        profile.bio = data.get('bio')
        
        # Handle JSON fields
        if data.get('lifestyle_preferences'):
            profile.lifestyle_preferences = json.dumps(data['lifestyle_preferences'])
        if data.get('interests'):
            profile.interests = json.dumps(data['interests'])
        if data.get('deal_breakers'):
            profile.deal_breakers = json.dumps(data['deal_breakers'])
        
        # Check if profile is complete
        required_fields = ['age', 'gender', 'budget_min', 'budget_max', 'location_preference', 
                          'cleanliness_level', 'social_level', 'noise_tolerance']
        profile.is_complete = all(getattr(profile, field) for field in required_fields)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'is_complete': profile.is_complete
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/matches', methods=['GET'])
@jwt_required()
def get_matches():
    """Get user's matches"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.profile or not user.profile.is_complete:
            return jsonify({'error': 'Complete your profile to see matches'}), 400
        
        # Get all matches for this user
        matches = Match.query.filter(
            (Match.user1_id == user_id) | (Match.user2_id == user_id)
        ).all()
        
        match_data = []
        for match in matches:
            # Get the other user
            other_user_id = match.user2_id if match.user1_id == user_id else match.user1_id
            other_user = User.query.get(other_user_id)
            
            if other_user and other_user.profile:
                match_data.append({
                    'id': match.id,
                    'user': {
                        'id': other_user.id,
                        'first_name': other_user.first_name,
                        'last_name': other_user.last_name,
                        'age': other_user.profile.age,
                        'occupation': other_user.profile.occupation,
                        'bio': other_user.profile.bio
                    },
                    'compatibility_score': match.compatibility_score,
                    'match_reason': match.match_reason,
                    'status': match.status,
                    'created_at': match.created_at.isoformat()
                })
        
        return jsonify({'matches': match_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/matches/generate', methods=['POST'])
@jwt_required()
def generate_matches():
    """Generate new matches for user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.profile or not user.profile.is_complete:
            return jsonify({'error': 'Complete your profile to generate matches'}), 400
        
        # Find potential matches
        potential_matches = UserProfile.query.filter(
            UserProfile.user_id != user_id,
            UserProfile.is_complete == True
        ).all()
        
        new_matches = []
        
        for potential_profile in potential_matches:
            # Check if match already exists
            existing_match = Match.query.filter(
                ((Match.user1_id == user_id) & (Match.user2_id == potential_profile.user_id)) |
                ((Match.user1_id == potential_profile.user_id) & (Match.user2_id == user_id))
            ).first()
            
            if existing_match:
                continue
            
            # Calculate compatibility score
            score = calculate_compatibility_score(user.profile, potential_profile)
            
            # Only create matches with score > 0.6
            if score > 0.6:
                match_reason = generate_match_reason(user.profile, potential_profile, score)
                
                match = Match(
                    user1_id=user_id,
                    user2_id=potential_profile.user_id,
                    compatibility_score=score,
                    match_reason=match_reason
                )
                
                db.session.add(match)
                new_matches.append({
                    'user_id': potential_profile.user_id,
                    'compatibility_score': score,
                    'match_reason': match_reason
                })
        
        db.session.commit()
        
        return jsonify({
            'message': f'Generated {len(new_matches)} new matches',
            'new_matches': new_matches
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/matches/<int:match_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_match():
    """Respond to a match (accept/reject)"""
    try:
        user_id = get_jwt_identity()
        match_id = request.view_args['match_id']
        data = request.get_json()
        
        match = Match.query.get(match_id)
        if not match:
            return jsonify({'error': 'Match not found'}), 404
        
        if match.user1_id != user_id and match.user2_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        response = data.get('response')  # 'accept' or 'reject'
        if response not in ['accept', 'reject']:
            return jsonify({'error': 'Invalid response'}), 400
        
        match.status = response
        db.session.commit()
        
        return jsonify({
            'message': f'Match {response}ed successfully',
            'status': match.status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/waitlist', methods=['POST'])
def join_waitlist():
    """Join the waitlist (for non-registered users)"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        # In a real implementation, you'd store this in a waitlist table
        # For now, we'll just return a success message
        
        return jsonify({
            'message': 'Successfully joined the waitlist! We\'ll notify you when Roommatch launches.',
            'email': data['email']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Database initialization
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
