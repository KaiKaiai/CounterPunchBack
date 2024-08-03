import os
from ultralytics import YOLO

# database stuff

from app import db
from datetime import datetime

class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    avatarURL = db.Column(db.String(200), nullable=False)

class FighterScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thrown = db.Column(db.Integer, default=0)
    hits = db.Column(db.Integer, default=0)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    fighter_id = db.Column(db.Integer, db.ForeignKey('fighter.id'), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    fighter1_id = db.Column(db.Integer, db.ForeignKey('fighter.id'), nullable=False)
    fighter2_id = db.Column(db.Integer, db.ForeignKey('fighter.id'), nullable=False)
    fighter1_score = db.relationship('FighterScore', foreign_keys=[FighterScore.match_id, FighterScore.fighter_id], 
                                     primaryjoin="and_(Match.id==FighterScore.match_id, Match.fighter1_id==FighterScore.fighter_id)",
                                     uselist=False, cascade="all, delete-orphan")
    fighter2_score = db.relationship('FighterScore', foreign_keys=[FighterScore.match_id, FighterScore.fighter_id],
                                     primaryjoin="and_(Match.id==FighterScore.match_id, Match.fighter2_id==FighterScore.fighter_id)",
                                     uselist=False, cascade="all, delete-orphan")
    fighter1 = db.relationship('Fighter', foreign_keys=[fighter1_id])
    fighter2 = db.relationship('Fighter', foreign_keys=[fighter2_id])
