from flask import Flask, request, jsonify
from sqlalchemy import create_engine, \
    Table, \
    Column, \
    MetaData, \
    Integer, \
    String, \
    JSON, \
    insert, \
    ForeignKey, \
    text, \
    DateTime
import os
from datetime import datetime

app = Flask(__name__)

db_uri = os.environ["DB_URI"]
engine = create_engine(db_uri, echo=True)
metadata = MetaData()

# Define Tables
github_event = Table(
    "github_events",
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('payload', JSON),
)

developer = Table(
    'developer',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String, unique=True),
)

pull_requests = Table(
    'pull_requests',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('developer_id', ForeignKey('developer.id'), nullable=False),
    Column('repo', String, nullable=False),
    Column('created_at', DateTime,
           default=datetime.now()),
)

push = Table(
    'push',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('developer_id', ForeignKey('developer.id'), nullable=False),
    Column('repo', String, nullable=False),
    Column('commits_count', Integer, nullable=False),
    Column('created_at', DateTime,
           default=datetime.now()),
)

commits = Table(
    'commits',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('developer_id', ForeignKey('developer.id'), nullable=False),
    Column('push_id', ForeignKey('push.id'), nullable=False),
    Column('repo', String, nullable=False),
    Column('files_added', Integer, nullable=False),
    Column('files_removed', Integer, nullable=False),
    Column('files_modified',
           Integer, nullable=False),
    Column('created_at', DateTime,
           default=datetime.now()),
)

metadata.create_all(engine)


@app.route("/pull-request", methods=['POST'])
def handle_pull_request():
    data = request.get_json()
    repo = data["pull_request"]["head"]["repo"]["full_name"]
    creator_name = data["pull_request"]["user"]["login"]

    developer_id = get_or_create_developer_id(creator_name)
    insert_pull_request(developer_id, repo)

    return jsonify({"status": "success"})


@app.route("/push", methods=['POST'])
def handle_push():
    data = request.get_json()
    pusher_name = data["pusher"]["name"]
    repo = data["repository"]["full_name"]

    developer_id = get_or_create_developer_id(pusher_name)
    insert_push_data(data, developer_id, repo)
    return jsonify({"status": "success"})


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    insert_github_event(data)
    return jsonify({"status": "success"})


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "service is healthy"})

# Helper function to get or create developer ID


def get_or_create_developer_id(developer_name):
    with engine.connect() as conn:
        developer_id = conn.execute(
            text(f"SELECT id FROM developer WHERE username = '{developer_name}'")
        ).scalar()

    if not developer_id:
        with engine.connect() as conn:
            result = conn.execute(insert(developer).values(username=developer_name))
            conn.commit()
        developer_id = result.inserted_primary_key[0]

    return developer_id

# Helper function to insert pull request data


def insert_pull_request(developer_id, repo):
    with engine.connect() as conn:
        ins = insert(pull_requests).values(
            developer_id=developer_id,
            repo=repo,
        )
        conn.execute(ins)
        conn.commit()

# Helper function to insert push data


def insert_push_data(data, developer_id, repo):
    commits_data = data["commits"]
    commits_count = len(commits_data)
    with engine.connect() as conn:
        push_id = conn.execute(push.insert().values(
            developer_id=developer_id,
            repo=repo,
            commits_count=commits_count
        )).inserted_primary_key[0]
        conn.commit()

    for commit_data in commits_data:
        developer_name = commit_data["author"]["username"]
        developer_id = get_or_create_developer_id(developer_name)

        with engine.connect() as conn:
            conn.execute(commits.insert().values(
                developer_id=developer_id,
                repo=repo,
                push_id=push_id,
                files_added=len(commit_data["added"]),
                files_removed=len(commit_data["removed"]),
                files_modified=len(commit_data["modified"])
            ))
            conn.commit()

# Helper function to insert GitHub event data


def insert_github_event(data):
    with engine.connect() as conn:
        query = insert(github_event).values(payload=data)
        conn.execute(query)
        conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
