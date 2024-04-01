from src import create_app, db

application = create_app()

if __name__ == '__main__':
    with application.app_context():
        db.create_all()
        application.run(debug=False, port=5000, host='0.0.0.0')