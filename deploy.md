# Deployment Guide for DigitalOcean App Platform

## Prerequisites
1. GitHub account with your project pushed to a public or private repository
2. DigitalOcean account (create one at https://www.digitalocean.com)
3. Custom domain (optional but recommended)

## Step-by-Step Deployment

### 1. Prepare Your Project
- All files have been configured for deployment
- `app.yaml` contains the deployment configuration
- `Procfile` defines how to run the application
- `requirements.txt` includes all necessary dependencies including Gunicorn

### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Prepare for DigitalOcean deployment"
git remote add origin https://github.com/your-username/real_estate_project
git push -u origin main
```

### 3. Deploy on DigitalOcean

#### Option A: Using DigitalOcean Console (Recommended)
1. Go to https://cloud.digitalocean.com
2. Click "Apps" in the left sidebar
3. Click "Create App"
4. Select "GitHub" as source
5. Authorize GitHub and select your repository
6. Choose branch: `main`
7. DigitalOcean may auto-detect the app.yaml. If not:
   - Click "Edit Configuration" and paste the contents of app.yaml
8. Set environment variables:
   - `SECRET_KEY`: Generate a new Django secret key
   - `EMAIL_HOST_USER`: Your email for sending emails
   - `EMAIL_HOST_PASSWORD`: App-specific password
   - `DEFAULT_FROM_EMAIL`: Your email domain
9. Click "Deploy"

#### Option B: Using DigitalOcean CLI
```bash
doctl apps create --spec app.yaml
```

### 4. Configure Environment Variables
In DigitalOcean Console:
1. Go to your App
2. Select "Settings"
3. Add the following environment variables:

| Key | Value |
|-----|-------|
| SECRET_KEY | Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| EMAIL_HOST_USER | Your Gmail/SMTP email |
| EMAIL_HOST_PASSWORD | Gmail app-specific password |
| DEFAULT_FROM_EMAIL | Your domain email |

### 5. Set Up Custom Domain (Optional)
1. In your App settings, go to "Domain"
2. Click "Add Domain"
3. Enter your domain and follow DNS instructions
4. Update your DNS provider with the CNAME record

### 6. Database Migrations
After first deployment:
1. Open your App console
2. Run: `python manage.py migrate`

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

## Important Notes

### Security
- Never commit `.env` file to GitHub
- Use environment variables for all sensitive data
- Enable HTTPS (automatic on DigitalOcean)
- Set `SECRET_KEY` to a strong, random value

### Static Files & Media
- Static files are collected during build
- Place static files in `static/` directory
- Media files are uploaded to `media/` directory
- For production, consider using DigitalOcean Spaces for media storage

### Scaling
- Monitor resource usage in DigitalOcean dashboard
- Increase worker count in `app.yaml` if needed
- Use database backups from DigitalOcean

## Troubleshooting

### Deployment fails
- Check build logs in DigitalOcean console
- Verify all environment variables are set
- Ensure requirements.txt is up to date

### Database connection issues
- Verify DATABASE_URL is correct
- Check if PostgreSQL database is running
- Ensure database IP whitelist allows your app

### Static files not loading
- Run: `python manage.py collectstatic --noinput`
- Check STATIC_URL and STATIC_ROOT settings

## Additional Resources
- [DigitalOcean App Platform Docs](https://docs.digitalocean.com/products/app-platform/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
