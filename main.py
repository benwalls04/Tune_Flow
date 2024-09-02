import urllib.parse
import filterSongs
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import getSongMetrics as getMetrics
import numpy as numpy
import requests
import os
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from train import train_model

from datetime import datetime
from flask import Flask, redirect, request, jsonify, session, url_for, render_template

load_dotenv
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
CLIENT_ID = '3b548122d04e4af0b64f1f6d473efc38'
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
  return "Welcome to my Spotify App <a href='/login'>Login with Spofity</a>"

@app.route('/login')
def login():
  scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private'

  params = {
    'client_id': CLIENT_ID,
    'response_type': 'code', 
    'scope': scope, 
    'redirect_uri': REDIRECT_URI, 
    'show_dialog': True
  }

  auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

  return redirect(auth_url)

@app.route('/form')
def form(): 
  return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
  session['old_playlist_name'] = request.form['old_playlist_name']
  session['new_playlist_name'] = request.form['new_playlist_name']
  session['mood'] = request.form['mood']

  return redirect('/playlists')
  
@app.route('/callback')
def callback():
  if 'error' in request.args:
    return jsonify({"error": request.args['error']})
  
  if 'code' in request.args: 
    req_body = {
      'code': request.args['code'], 
      'grant_type': 'authorization_code',
      'redirect_uri': REDIRECT_URI, 
      'client_id': CLIENT_ID, 
      'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=req_body)
    token_info = response.json()

    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

    return redirect('/form')
  
@app.route('/playlists')
def get_playlists():
  if 'access_token' not in session:
    return redirect('/login')

  if datetime.now().timestamp() > session['expires_at']:
    return redirect('/refresh-token')
  
  headers = {
    'Authorization': f"Bearer {session['access_token']}"
  }

  response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
  playlists = response.json()  
  items = playlists.get('items', [])

  for playlist in items: 
    playlist_name = playlist.get('name')
    if playlist_name == session['old_playlist_name']:
      session['playlist_id'] = playlist.get('id')
      return redirect('/train')
  
  return render_template('index.html', message='Playlist not found. Make sure the name you entered for Old Playlist Name matches exactly with a playlist on your profile')

@app.route('/train')
def train():
  train_model(session['access_token'], session['playlist_id'])
  return render_template('index.html', message='training started')

@app.route('/create')
def create(): 
  return 

@app.route('/refresh-token')
def refresh_token():
  if 'refresh_token' not in session:
    return redirect('/login')

  if datetime.now().timestamp() > session['expires_at']:
    req_body = {
      'grant_type': 'refresh_token', 
      'refresh_token': session['refresh_token'], 
      'client_id': CLIENT_ID, 
      'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return redirect('/playlists')
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8000)
