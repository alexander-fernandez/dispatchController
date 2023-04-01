from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any, List, Optional
import sqlalchemy as sa
import random
import string


allowed = "".join((string.ascii_uppercase, string.digits, '-', '_'))
db = SQLAlchemy()


class CModel(db.Model):
    __tablename__ = "CModel"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)

    def __init__(self, name, **kw: Any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def json_rep(self):
        pair = dict()
        pair["id"] = self.id
        pair["name"] = self.name
        return jsonify(pair)


class CState(db.Model):
    __tablename__ = "CState"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)

    def __init__(self, name, **kw: Any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Drone(db.Model):
    __tablename__ = 'Drone'
    id = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    serial: Mapped[str] = mapped_column(sa.String(100))
    max_weight: Mapped[int]
    battery: Mapped[int]

    # Relationships
    model_id: Mapped[int] = mapped_column(sa.ForeignKey("CModel.id"))
    state_id: Mapped[int] = mapped_column(sa.ForeignKey("CState.id"))
    medications: Mapped[List["Medication"]] = relationship(back_populates="drone")

    def __init__(self, serial, max_weight, battery, **kw: Any):
        super().__init__(**kw)
        if len(serial) > 100:
            raise Exception("Serial Number is too long")
        self.serial = serial
        self.max_weight = max_weight
        self.battery = battery

    def __repr__(self):
        return self.serial

    def __str__(self):
        return self.serial


"""
name (allowed only letters, numbers, ‘-‘, ‘_’);
weight (in grams);
code (allowed only upper case letters, underscore and numbers);
image (picture of the medication case)
"""


class Medication(db.Model):
    __tablename__ = 'Medication'

    id = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]
    weight: Mapped[int]
    code: Mapped[str]
    done: Mapped[bool]
    image = mapped_column(sa.BLOB)


    # Relationships
    drone_id: Mapped[Optional[int]] = mapped_column(sa.ForeignKey("Drone.id"))
    drone: Mapped[Optional["Drone"]] = relationship(back_populates="medications")

    def __init__(self, name, weight, code, done, image, drone, **kw: Any):
        super().__init__(**kw)
        test = code.translate({ord(i): None for i in allowed})
        if len(test) > 0:
            raise Exception("The code contains characters not allowed")
        self.name = name
        self.weight = weight
        self.code = code
        self.done = done
        self.image = image
        self.drone = drone

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


def db_populate():
    # state (IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING).
    s1 = CState("IDLE")
    s2 = CState("LOADING")
    s3 = CState("LOADED")
    s4 = CState("DELIVERING")
    s5 = CState("DELIVERED")
    s6 = CState("RETURNING")

    db.session.add_all([s1, s2, s3, s4, s5, s6])
    db.session.commit()

    # model (Lightweight, Middleweight, Cruiserweight, Heavyweight);
    m1 = CModel("Lightweight")
    m2 = CModel("Middleweight")
    m3 = CModel("Cruiserweight")
    m4 = CModel("Heavyweight")

    db.session.add_all([m1, m2, m3, m4])
    db.session.commit()

    d1 = Drone("5699f6e4-29f5-4f55-b905-3d671b7ea01a", 400, 100)
    d1.model_id = m1.id
    d1.state_id = s1.id

    d2 = Drone("050460c1-03e0-4fd1-9ca9-773df7cddf2e", 450, 100)
    d2.model_id = m2.id
    d2.state_id = s1.id

    d3 = Drone("2dfcfb09-a3c4-4ffc-a98a-50fee3c2228e", 475, 100)
    d3.model_id = m3.id
    d3.state_id = s1.id

    d4 = Drone("11921a43-2ef2-4b5b-814a-089ddb6afac6", 500, 100)
    d4.model_id = m4.id
    d4.state_id = s1.id

    d5 = Drone("9216bbba-6fe6-44ac-8c67-92572e4ca9f5", 420, 100)
    d5.model_id = m1.id
    d5.state_id = s1.id

    d6 = Drone("f167dc54-a672-4279-aefe-0088f7fdbfd6", 440, 100)
    d6.model_id = m2.id
    d6.state_id = s1.id

    d7 = Drone("255fe9cd-f3f7-490d-8c2c-84e3289c61b2", 480, 100)
    d7.model_id = m3.id
    d7.state_id = s1.id

    d8 = Drone("fab64f7d-6c00-4b4f-9128-cb47da4a9297", 500, 100)
    d8.model_id = m4.id
    d8.state_id = s1.id

    d9 = Drone("75177b23-aff8-4d21-9a3b-2d3f046ddab1", 485, 100)
    d9.model_id = m3.id
    d9.state_id = s1.id

    d0 = Drone("b3b96530-7b0c-4ba2-a1f8-a15f23c8e867", 490, 100)
    d0.model_id = m4.id
    d0.state_id = s1.id

    db.session.add_all([d0, d1, d2, d3, d4, d5, d6, d7, d8, d9])
    db.session.commit()

    p01 = Medication("Vitamin D", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p02 = Medication("Amoxicillin", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p03 = Medication("Levothyroxine", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p04 = Medication("Lisinopril", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p05 = Medication("Ibuprofen", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p06 = Medication("Amphetamine", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p07 = Medication("Amlodipine", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p08 = Medication("Albuterol HFA", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p09 = Medication("Prednisone", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p10 = Medication("Gabapentin", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p11 = Medication("Benzonatate", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p12 = Medication("Alprazolam", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p13 = Medication("Cyclobenzaprine", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p14 = Medication("Azithromycin", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p15 = Medication("Atorvastatin", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p16 = Medication("Cetirizine", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p17 = Medication("Losartan", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p18 = Medication("Amoxicillin", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p19 = Medication("Cephalexin", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p20 = Medication("Metformin", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p21 = Medication("Metoprolol Succinate ER", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p22 = Medication("Folic Acid", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p23 = Medication("Hydrochlorothiazide", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p24 = Medication("Sildenafil", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p25 = Medication("Trazodone", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p26 = Medication("Zolpidem Tartrate ", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p27 = Medication("Escitalopram", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p28 = Medication("Clonazepam", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p29 = Medication("Methylprednisolone", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p30 = Medication("Tadalafil", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p31 = Medication("Methocarbamol", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p32 = Medication("Fluconazole", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p33 = Medication("Sertraline", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p34 = Medication("Doxycycline Hyclate", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p35 = Medication("Furosemide", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p36 = Medication("Fluoxetine", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p37 = Medication("Metronidazole", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p38 = Medication("Freestyle", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p39 = Medication("Omeprazole", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p40 = Medication("FeroSul", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p41 = Medication("Sulfamethoxazole", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p42 = Medication("Phenobarbital", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p43 = Medication("Armour", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p44 = Medication("Bromphen", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p45 = Medication("Metoprolol", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p46 = Medication("Meloxicam", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p47 = Medication("Pantoprazole", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p48 = Medication("Lisinopril", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p49 = Medication("Estradiol", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)
    p50 = Medication("Famotidine", random.randint(20, 50), "".join(random.choice(allowed) for _ in range(40)), False, None, None)

    db.session.add_all([p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15])
    db.session.commit()
    db.session.add_all([p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30])
    db.session.commit()
    db.session.add_all([p31, p32, p33, p34, p35, p36, p37, p38, p39, p40, p41, p42, p43, p44, p45])
    db.session.commit()
    db.session.add_all([p46, p47, p48, p49, p50])
    db.session.commit()
