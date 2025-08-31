from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user
from flask import redirect, url_for, request, flash, current_app
import json
import os

class PersonaConfigView(BaseView):
    @expose('/')
    def index(self):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))
        
        config_path = os.path.join(current_app.root_path, '..', 'persona_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return self.render('admin/persona_config.html', config=config)
    
    @expose('/update', methods=['POST'])
    def update(self):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))
        
        config_path = os.path.join(current_app.root_path, '..', 'persona_config.json')
        
        # Get form data and update config
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Update persona info
            config['persona']['name'] = request.form.get('persona_name', config['persona']['name'])
            config['persona']['tagline'] = request.form.get('persona_tagline', config['persona']['tagline'])
            config['persona']['book_title'] = request.form.get('book_title', config['persona']['book_title'])
            config['persona']['book_link'] = request.form.get('book_link', config['persona']['book_link'])
            config['persona']['logo_text'] = request.form.get('logo_text', config['persona']['logo_text'])
            
            # Update theme colors
            config['theme']['accent_color'] = request.form.get('accent_color', config['theme']['accent_color'])
            config['theme']['primary_bg'] = request.form.get('primary_bg', config['theme']['primary_bg'])
            
            # Update content
            config['content']['hero_headline'] = request.form.get('hero_headline', config['content']['hero_headline'])
            config['content']['mastermind_price'] = request.form.get('mastermind_price', config['content']['mastermind_price'])
            
            # Save updated config
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            flash('Persona configuration updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating configuration: {str(e)}', 'error')
        
        return redirect(url_for('personaconfig.index'))
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class VideoContentView(BaseView):
    @expose('/')
    def index(self):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))
        
        # In production, this would load from database
        # For now, we'll use the config file
        config_path = os.path.join(current_app.root_path, '..', 'persona_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        premium_titles = config['content']['premium_video_titles']
        
        return self.render('admin/video_content.html', premium_titles=premium_titles)
    
    @expose('/update-premium-titles', methods=['POST'])
    def update_premium_titles(self):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))
        
        config_path = os.path.join(current_app.root_path, '..', 'persona_config.json')
        
        try:
            # Get the new titles from form
            titles = request.form.get('premium_titles', '').strip().split('\n')
            titles = [t.strip() for t in titles if t.strip()]
            
            # Update config
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            config['content']['premium_video_titles'] = titles
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            flash('Premium video titles updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating titles: {str(e)}', 'error')
        
        return redirect(url_for('videocontent.index'))
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))