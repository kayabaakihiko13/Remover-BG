from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Halaman Beranda"""
    return render_template('index.html')


@main_bp.route('/about')
def about():
    """Halaman Tentang"""
    return render_template('view/about.html')


@main_bp.route('/health')
def health_check():
    """Endpoint untuk cek kesehatan server"""
    return jsonify({'status': 'healthy', 'service': 'remover-bg'})