from app import db
import datetime

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime, default=(datetime.date.today()+datetime.timedelta(days=7)))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True,nullable=False)
    customer = db.relationship("Customer", back_populates="rentals")
    video = db.relationship("Video", back_populates="rentals")

    def to_dict(self):
        rental_dict = {}
        rental_dict["id"] = self.id
        rental_dict["customer_id"] = self.customer_id
        rental_dict["video_id"] = self.video_id
        rental_dict["due_date"] = self.due_date
        return rental_dict

    @classmethod
    def from_dict(cls, rental_data):
        new_rental = Rental(
            customer_id = rental_data["customer_id"],
            video_id = rental_data["video_id"]
        )
        return new_rental


