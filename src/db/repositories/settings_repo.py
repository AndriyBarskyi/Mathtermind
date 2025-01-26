from sqlalchemy.orm import Session
from src.db.models import Setting
import uuid


def create_settings(db: Session, key: str, value: str):
    setting = Setting(id=uuid.uuid4(), key=key, value=value)
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def delete_settings(db: Session, setting_id: uuid.UUID):
    setting = db.query(Setting).filter(Setting.id == setting_id).first()
    db.delete(setting)
    db.commit()
    return setting


def get_settings(db: Session, setting_id: uuid.UUID):
    return db.query(Setting).filter(Setting.id == setting_id).first()


def update_settings(db: Session, setting_id: uuid.UUID, key: str, value: str):
    setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if setting is None:
        return None  # or raise an exception
    setattr(setting, "key", key)
    setattr(setting, "value", value)
    db.commit()
    db.refresh(setting)
    return setting
