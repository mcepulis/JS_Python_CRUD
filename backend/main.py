from flask import request, jsonify
from config import db, app
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    phone = request.json.get("phone")

    if not first_name or not last_name or not email or not phone:
        return jsonify({"error": "All fields are required"}), 400
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}, 400)
    
    return jsonify({"message": "Contact created successfully"}), 201

@app.route("/update_contact/<int:user_id>", methods=["PUT"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    
    data=request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    contact.phone = data.get("phone", contact.phone)

    db.session.commit()

    return jsonify({"message": "Contact updated successfully"}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "Contact deleted successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

app.run(debug=True)