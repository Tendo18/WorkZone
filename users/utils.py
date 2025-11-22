from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_welcome_email(user):
    """
    Send a welcome email to newly registered users
    """
    subject = "Welcome to WorkZone! 🎉"
    
    # Plain text email content
    message = f"""
Hi {user.get_full_name() or user.username},

Welcome to WorkZone! Thank you for joining our job portal community.

Here's how WorkZone works:

📋 REGISTRATION COMPLETE
Your account has been successfully created with the role: {user.get_role_display()}

🔐 LOGIN TO GET STARTED
- Visit our platform and login with your email: {user.email}
- You'll receive JWT tokens for secure access
- Keep your tokens safe for API access

👤 YOUR PROFILE
- Complete your profile with additional information
- Upload a profile picture to make your account stand out
- Add your skills, experience, and preferences

🎯 WHAT YOU CAN DO:
- Browse and search for job opportunities
- Apply to jobs that match your skills
- Track your application status
- Receive email notifications for updates

📧 STAY CONNECTED
You'll receive email notifications for:
- New job postings that match your preferences
- Application status updates
- Important platform announcements

🔒 SECURITY
- Your account is protected with JWT authentication
- Never share your login credentials
- Logout properly to secure your session

Need help? Contact our support team.

Best regards,
The WorkZone Team

---
WorkZone - Connecting Talent with Opportunity
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False

def send_role_specific_welcome_email(user):
    """
    Send role-specific welcome emails with additional information
    """
    if user.is_employer:
        return send_employer_welcome_email(user)
    elif user.is_applicant:
        return send_applicant_welcome_email(user)
    elif user.is_admin:
        return send_admin_welcome_email(user)
    else:
        return send_welcome_email(user)

def send_employer_welcome_email(user):
    """
    Send welcome email specifically for employers
    """
    subject = "Welcome to WorkZone - Employer Account Activated! 🏢"
    
    message = f"""
Hi {user.get_full_name() or user.username},

Welcome to WorkZone! Your employer account has been successfully created.

🏢 EMPLOYER FEATURES:
- Post job opportunities for your company
- Review and manage applications
- Connect with talented candidates
- Track application statuses
- Receive notifications for new applications

📝 NEXT STEPS:
1. Complete your company profile
2. Add your company logo and description
3. Start posting job opportunities
4. Review incoming applications

💼 POSTING JOBS:
- Create detailed job descriptions
- Set job requirements and preferences
- Choose job types (Full-time, Remote, etc.)
- Set application deadlines

📊 MANAGE APPLICATIONS:
- Review candidate profiles and resumes
- Update application status (Approved/Rejected/Pending)
- Send status notifications to applicants
- Track application metrics

Need help getting started? Contact our support team.

Best regards,
The WorkZone Team

---
WorkZone - Connecting Employers with Talent
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send employer welcome email to {user.email}: {str(e)}")
        return False

def send_applicant_welcome_email(user):
    """
    Send welcome email specifically for applicants
    """
    subject = "Welcome to WorkZone - Start Your Job Search! 💼"
    
    message = f"""
Hi {user.get_full_name() or user.username},

Welcome to WorkZone! Your applicant account has been successfully created.

💼 APPLICANT FEATURES:
- Browse and search for job opportunities
- Apply to jobs that match your skills
- Track your application status
- Receive job alerts and notifications
- Build your professional profile

📝 NEXT STEPS:
1. Complete your professional profile
2. Add your skills and experience
3. Set your job preferences
4. Start browsing and applying to jobs

🔍 FINDING JOBS:
- Search by job title, location, or company
- Filter by job type (Full-time, Remote, etc.)
- Save interesting jobs for later
- Set up job alerts for new opportunities

📄 APPLYING TO JOBS:
- Submit your resume and cover letter
- Track application status in real-time
- Receive notifications for status updates
- Manage multiple applications

📱 PROFILE TIPS:
- Add a professional headline
- List your key skills and experience
- Include your education background
- Add links to your portfolio or LinkedIn

Need help getting started? Contact our support team.

Best regards,
The WorkZone Team

---
WorkZone - Connecting Talent with Opportunity
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send applicant welcome email to {user.email}: {str(e)}")
        return False

def send_admin_welcome_email(user):
    """
    Send welcome email specifically for admin users
    """
    subject = "Welcome to WorkZone - Admin Account Activated! ⚙️"
    
    message = f"""
Hi {user.get_full_name() or user.username},

Welcome to WorkZone! Your admin account has been successfully created.

⚙️ ADMIN FEATURES:
- Manage all users and profiles
- Monitor platform activity
- Handle user verifications
- Manage job postings and applications
- System configuration and maintenance

🔧 ADMIN DASHBOARD:
- User management and statistics
- Platform analytics and reports
- Content moderation tools
- System health monitoring

📊 MONITORING:
- Track user registrations and activity
- Monitor job posting and application metrics
- Handle user support requests
- Maintain platform security

Need help with admin functions? Contact the system administrator.

Best regards,
The WorkZone Team

---
WorkZone - Admin Portal
    """
    
    try:
        send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        return True
    except Exception as e:
        print(f"Failed to send admin welcome email to {user.email}: {str(e)}")
        return False 