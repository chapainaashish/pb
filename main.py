from website import create_app
from flask_apscheduler import APScheduler
from website import db
from website.models import User

app = create_app()

scheduler = APScheduler()

def update_key_uses():
    with app.app_context():
        # Get all users
        users = User.query.all()

        # Iterate through users and update api_key_uses to 5
        for user in users:
            user.api_key_uses = 5
            db.session.commit()
        print("Database Updated")

# Schedule the update_key_uses function to run on the first day of each month
scheduler.add_job(id='Update key', func=update_key_uses, trigger='cron', year='*', month='*', day=1)

# Start the scheduler
scheduler.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)