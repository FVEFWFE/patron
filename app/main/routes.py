from app import db
from app.main import bp
from app.models import User, PriceLevel
from flask import render_template, current_app, jsonify, request
from flask_login import current_user, login_required
import json
import os

@bp.route('/')
@bp.route('/index')
def index():
    """
    Main homepage displaying all sections for Dex Volkov persona
    """
    # Load free videos from database or config
    free_videos = get_free_videos()
    intro_video = get_intro_video()
    
    return render_template(
        'index.html',
        free_videos=free_videos,
        intro_video=intro_video
    )

@bp.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')

@bp.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('terms.html')

@bp.route('/api/video/<int:video_id>')
@login_required
def get_video(video_id):
    """API endpoint for video streaming (free videos only)"""
    # Check if user has access to this video
    video = get_video_by_id(video_id)
    if not video or not video.get('is_free'):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({
        'url': video.get('url'),
        'title': video.get('title')
    })

def get_free_videos():
    """Get list of free preview videos"""
    # This would normally come from database
    # For now, return sample data
    return [
        {
            'id': 1,
            'title': 'Introduction: My Journey from Wall Street to Freedom',
            'description': 'Discover how I escaped the corporate matrix and built a location-independent empire.',
            'thumbnail': '/static/images/video-thumb-1.jpg',
            'url': '/static/videos/intro.mp4'
        },
        {
            'id': 2,
            'title': 'GPU Arbitrage 101: The Basics',
            'description': 'Learn the fundamental concepts behind GPU arbitrage and why it\'s the ultimate asymmetric bet.',
            'thumbnail': '/static/images/video-thumb-2.jpg',
            'url': '/static/videos/gpu-basics.mp4'
        },
        {
            'id': 3,
            'title': 'The Thailand Advantage',
            'description': 'Why Southeast Asia is the perfect base for digital nomad traders.',
            'thumbnail': '/static/images/video-thumb-3.jpg',
            'url': '/static/videos/thailand.mp4'
        },
        {
            'id': 4,
            'title': 'Bitcoin: The Only Real Money',
            'description': 'My thesis on why Bitcoin is the only cryptocurrency that matters.',
            'thumbnail': '/static/images/video-thumb-4.jpg',
            'url': '/static/videos/bitcoin.mp4'
        },
        {
            'id': 5,
            'title': 'Risk Management Philosophy',
            'description': 'How to think about risk in a world of black swans and AI disruption.',
            'thumbnail': '/static/images/video-thumb-5.jpg',
            'url': '/static/videos/risk.mp4'
        }
    ]

def get_intro_video():
    """Get the main intro/hero video"""
    return {
        'url': '/static/videos/hero-intro.mp4',
        'title': 'Welcome to the Vault'
    }

def get_video_by_id(video_id):
    """Get video by ID"""
    videos = get_free_videos()
    for video in videos:
        if video['id'] == video_id:
            video['is_free'] = True
            return video
    return None