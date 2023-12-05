from flask import Flask, request, jsonify
from sqlalchemy import Table, Column, MetaData, Integer, create_engine, JSON, String, insert, ForeignKey, DateTime, select
import os
import logging

app = Flask(__name__)

CONNECTION_STRING = "developeriq.cgfn0rdytwyv.ap-southeast-1.rds.amazonaws.com"
DB_USER = "postgres"
DB_PASSWORD = "dEbpMuh1YPXZu21SxR4t"

db_uri = os.environ.get(
    "DB_URI", "postgresql://postgres:dEbpMuh1YPXZu21SxR4t@developeriq.cgfn0rdytwyv.ap-southeast-1.rds.amazonaws.com:5432/developeriq?sslmode=require")
engine = create_engine(db_uri, echo=True)
conn = engine.connect()

metadata = MetaData()

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
    Column('email', String, unique=True)
)

commits = Table(
    'commits',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('developer_id', ForeignKey('developer.id'), nullable=False),
    Column('commit_date', String, nullable=False),
    Column('commit_message', String, nullable=False)
)

issues = Table(
    'issues',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('developer_id', ForeignKey('developer.id'), nullable=False),
    Column('issue_type', String, nullable=False),
    Column('issue_date', DateTime, nullable=False)
)

pull_requests = Table(
    'pull_requests',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('developer_id', ForeignKey('developer.id'), nullable=False),
    Column('pr_type', String, nullable=False),
    Column('pr_date', String, nullable=False),
    Column('pr_comments_count', Integer, nullable=False, default=0),
    Column('pr_commits_count', Integer, nullable=False, default=0),
)

metadata.create_all(engine)


@app.route("/webhook", methods=["POST"])
def webhook():
    db_uri = os.environ.get(
        "DB_URI", "postgresql://postgres:dEbpMuh1YPXZu21SxR4t@developeriq.cgfn0rdytwyv.ap-southeast-1.rds.amazonaws.com:5432/developeriq?sslmode=require")
    engine = create_engine(db_uri, echo=True)
    conn = engine.connect()
    data = request.get_json()

    query = insert(github_event).values(payload=data)
    conn.execute(query)
    conn.commit()

    return jsonify({"status": "success"})


@app.route("/commit-analyse/<id>", methods=["GET"])
def commit_analyse(id):
    db_uri = os.environ.get(
        "DB_URI", "postgresql://postgres:dEbpMuh1YPXZu21SxR4t@developeriq.cgfn0rdytwyv.ap-southeast-1.rds.amazonaws.com:5432/developeriq?sslmode=require")
    engine = create_engine(db_uri, echo=True)
    conn = engine.connect()
    query = select(github_event.c["payload"]).where(
        github_event.c.id == id)
    row = conn.execute(query).fetchone()
    logging.info("==============")
    logging.info(row)
    logging.info(type(row))
    logging.info("==============")
    return jsonify({"result": row.payload})


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "service is healthy"})
