
def save_to(data, db):
    db.session.add(data)
    db.session.commit()
        
def delete_data(data, db):
    db.session.delete(data)
    db.session.commit()
