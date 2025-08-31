# Dex Volkov - Private Content Vault

## Overview
This is a transformed version of LibrePatron, rebuilt as a modern, high-trust private content vault for the "Dex Volkov" persona. The platform serves as a psychological conversion tool featuring a sophisticated dark-mode design, fake paywall system, and complete privacy protection.

## Key Features

### 🎭 Persona System
- Fully configurable persona (name, tagline, book, etc.)
- Easy swapping between different personas via JSON config
- Admin panel for real-time customization

### 🌑 Modern Dark Theme
- Professional dark mode design with tech-noir aesthetics
- Custom CSS with charcoal grey (#1A1A1A) and cyan accent (#00D4FF)
- Fully responsive and mobile-optimized
- No external CSS dependencies

### 🔒 Privacy & Security
- Complete search engine blocking (robots.txt + meta tags)
- No external dependencies (self-hosted fonts, scripts)
- No Google Analytics or tracking
- No cookies or user tracking
- Bitcoin-only payment references

### 🎬 Video System
- Self-hosted video player with minimalist controls
- 5-6 free preview videos
- 20+ fake "premium" video titles behind paywall
- No view counts or social features

### 💰 Fake Paywall
- Premium content section showing "$399.99/year - Bitcoin Only"
- "Membership Full" status to create exclusivity
- Locked premium video titles (text only, no actual videos needed)
- Psychological conversion tool, not actual payment processor

### 📚 Book Promotion
- Dedicated section for "The AI Kill Switch"
- Direct link to book website
- 3D book mockup display area

## Removed Features
- ✅ Isso commenting system - completely removed
- ✅ Square payment processing - all code stripped
- ✅ Email subscription system - removed
- ✅ Google Analytics - eliminated
- ✅ APScheduler - not needed for static content
- ✅ BTCPay integration - removed (using fake paywall instead)
- ✅ 21 outdated Bootstrap themes - replaced with custom dark theme

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL or SQLite
- Linux/Unix environment (for production)

### Setup Steps

1. **Clone and prepare environment:**
```bash
cd /workspace
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements_new.txt
```

3. **Set environment variables:**
```bash
export FLASK_APP=patron.py
export DATABASE_URL="sqlite:///app.db"  # or PostgreSQL URL
export SECRET_KEY="your-secret-key-here"
```

4. **Initialize database:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Create admin user:**
```python
flask shell
>>> from app import db
>>> from app.models import User
>>> admin = User(username='admin', email='admin@example.com', role='admin')
>>> admin.set_password('your-secure-password')
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()
```

6. **Add content:**
- Place video files in `/app/static/videos/`
- Place images in `/app/static/images/`
- Update video metadata in `app/main/routes.py`

7. **Run the application:**
```bash
flask run --host=0.0.0.0 --port=5000
```

For production, use Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 patron:app
```

## Configuration

### Persona Configuration (`persona_config.json`)
Edit this file to customize:
- Persona name and details
- Theme colors
- Content text
- Premium video titles
- Testimonials

### Admin Panel Access
1. Navigate to `/admin`
2. Login with admin credentials
3. Access "Persona Config" to modify settings
4. Use "Video Content" to manage premium titles

## File Structure
```
/workspace/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   ├── custom-dark.css    # Main theme
│   │   │   └── plyr.css          # Video player styles
│   │   ├── js/
│   │   │   ├── main.js           # Site functionality
│   │   │   └── plyr.js           # Video player
│   │   ├── fonts/                # Self-hosted fonts
│   │   ├── images/               # Static images
│   │   └── videos/               # Video files
│   ├── templates/
│   │   ├── base.html             # Base template
│   │   ├── index.html            # Homepage
│   │   ├── privacy.html          # Privacy policy
│   │   └── terms.html            # Terms of service
│   └── main/
│       └── routes.py             # Simplified routes
├── persona_config.json           # Persona configuration
└── requirements_new.txt          # Python dependencies
```

## Deployment Checklist

### Security
- [ ] Change all default passwords
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS only
- [ ] Configure firewall rules
- [ ] Disable debug mode
- [ ] Set up fail2ban

### Privacy
- [ ] Verify robots.txt is serving correctly
- [ ] Check meta tags for noindex/nofollow
- [ ] Confirm no external resources loading
- [ ] Test with privacy analysis tools
- [ ] Verify no cookies are set

### Content
- [ ] Upload all video files
- [ ] Create video thumbnails
- [ ] Add book mockup image
- [ ] Update all persona details
- [ ] Test video playback

### Performance
- [ ] Enable gzip compression
- [ ] Set up CDN for videos (optional, use privacy-focused CDN)
- [ ] Configure caching headers
- [ ] Optimize images

## Persona Swapping Guide

To change from "Dex Volkov" to a new persona (e.g., "Marcus Kane"):

1. **Update persona_config.json:**
```json
{
  "persona": {
    "name": "Marcus Kane",
    "tagline": "New tagline here",
    "book_title": "New Book Title",
    "book_link": "https://newbook.com",
    ...
  }
}
```

2. **Update theme colors in config:**
```json
{
  "theme": {
    "accent_color": "#FF6B6B",  // New accent color
    ...
  }
}
```

3. **Replace content:**
- Swap video files in `/static/videos/`
- Update video metadata in routes
- Change book mockup image
- Update testimonials in config

4. **Restart application:**
```bash
sudo systemctl restart gunicorn
```

## Maintenance

### Regular Tasks
- Clear server logs: `rm /var/log/nginx/*.log`
- Update persona content via admin panel
- Monitor disk space for video storage
- Backup persona_config.json regularly

### Troubleshooting
- **Videos not playing:** Check file permissions and paths
- **Admin panel access denied:** Verify user role is 'admin'
- **Theme not loading:** Clear browser cache, check CSS path
- **Database errors:** Run `flask db upgrade`

## Important Notes

1. **This is NOT a payment processor** - The paywall is purely psychological
2. **Keep it private** - This system is designed to be unlisted and unindexed
3. **No real transactions** - Never attempt to process actual payments
4. **Regular backups** - Always backup persona_config.json before changes
5. **Test locally first** - Always test persona changes in development

## Support

This is a custom implementation for specific use cases. For issues:
1. Check the error logs
2. Verify all dependencies are installed
3. Ensure database is properly initialized
4. Confirm file permissions are correct

Remember: This platform is designed for creating an aura of exclusivity and premium content, not for actual payment processing or member management.

---

**Version:** 1.0.0  
**Last Updated:** January 2024  
**Status:** Production Ready