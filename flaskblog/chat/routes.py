from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify, session)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Chat, User
import json
from dataclasses import dataclass
from sqlalchemy import text




chat = Blueprint('chat', __name__)


@login_required
@chat.route("/profile/<username>/<room>")
def profile(username=None, room=None):
    user = current_user.username
    room = room.strip()
    session['room'] = room if room else "GLOBAL"
    username = User.query.filter_by(username=username).first()
    chats = Chat.query.filter(Chat.rooms.like(f'%{room}%')).order_by(Chat.date_created.desc()).all()
    if room == "GLOBAL":
      return render_template('chat_page.html', username=username, chats=chats, room=room)
    else:
      members = room.split("-")
      if (current_user.username in members):
        return render_template('chat_page.html', username=username, chats=chats, room=room)
      else:
        flash('You do not have permission to enter this room', 'danger')
        return redirect(url_for('main.home'))
       

@login_required
@chat.route("/new_message/", methods=["POST"]) 
def new_message(): 
	message = request.form.get('message')
	author = request.form.get('author')
	room = request.form.get('room')
	new_chat = Chat(author=author, rooms=room, message=message)
	try:
		db.session.add(new_chat)
		db.session.commit()
		addChat = {'author': author, 'message': message, 'room': room}
		return json.dumps(addChat)
		return redirect(url_for('profile', username=author, room=room))
	except Exception as e:
		print(e)
		return 'There was an error adding your chat message'
	
#@login_required
@chat.route("/messages/", methods=["GET","POST"])
def messages():  
    room = session.get('room')#session['room']
    if room:
            all_chats = Chat.query.filter(Chat.rooms.like(f'%{room}%')).order_by(Chat.date_created.desc()).all()
            all_chats_json = { }
            for index, element in enumerate(all_chats):
                all_chats_json[index] = { }
                all_chats_json[index]['author'] = element.author
                all_chats_json[index]['message'] = element.message
               # all_chats_json[index]['room'] = element.rooms
                all_chats_json[index]['datetime'] = element.date_created.date()
            return jsonify(all_chats_json)
                #return json.dumps(all_chats_json)   
    else:
        return jsonify({"message":"something went wrong"})
     #   return redirect(url_for('main.home'))
    


@chat.route("/create_room/", methods=['POST'])
@login_required
def create_room():
    text = request.form.get('text').strip()
    user1 = current_user.username
    room = Chat.query.filter(Chat.rooms.like(f'%{text}%')).filter(Chat.rooms.like(f'%{user1}%')).first()
    if room:
        return redirect(url_for('chat.profile' ,username = current_user.username, room = room.rooms))
    else:
          user = User.query.filter_by(username=text).first()
          room = text + "-" + current_user.username
          if user:
            chats = Chat.query.filter(Chat.rooms.like(f'%{text}%')).order_by(Chat.date_created.desc()).all()
            username = current_user.username
            return redirect(url_for('chat.profile' ,username = current_user.username, room = room))
          else:
             flash('This user does not exist', 'danger')
             return redirect(url_for('chat.profile' ,username = current_user.username, room = "GLOBAL"))

@chat.context_processor
def room_list():
     user = current_user.username
     #rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).with_entities(Chat.rooms).distinct().order_by(Chat.date_created.desc())
     #rooms = db.session.query(text("distinct rooms from Chat"))
     rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)
     return dict(rooms=rooms) # find how to implement exactly alike

               
         


