from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime


def get_product_tags(db: Session):
    res = db.query(models.ProductTag).all()
    return res


def get_product_tag(db: Session, tag_id: int):
    res = db.query(models.ProductTag).filter(
        models.ProductTag.id == tag_id).first()
    return res


def get_companies(db: Session):
    res = db.query(models.Company).all()
    return res


def get_company(db: Session, company_id: int):
    res = db.query(models.Company).filter(
        models.Company.id == company_id).first()
    return res


def get_users(db: Session):
    res = db.query(models.User).all()
    return res


def get_user(db: Session, user_id: int):
    res = db.query(models.User).filter(models.User.id == user_id).first()
    return res


def get_products(db: Session):
    res = db.query(models.Product).all()
    return res


def get_product(db: Session, product_id: int):
    res = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    return res


def get_invoices(db: Session):
    res = db.query(models.Invoice).all()
    return res


def get_invoice(db: Session, invoice_id: int):
    res = db.query(models.Invoice).filter(
        models.Invoice.id == invoice_id).first()
    return res


def get_bookmarks(db: Session):
    res = db.query(models.UserBookmark).all()
    return res


def get_bookmark(db: Session, user_id: int):
    res = db.query(models.UserBookmark).filter(
        models.UserBookmark.user_id == user_id).all()
    return res


def get_bank_accounts(db: Session):
    res = db.query(models.BankAccount).all()
    return res


def get_bank_account(db: Session, user_id: int):
    res = db.query(models.BankAccount).filter(
        models.UserBookmark.user_id == user_id).first()
    return res


def create_user(db: Session, user: schemas.UserCreate):
    user_db_model = models.User()
    user_db_model.user_name = user.username
    user_db_model.user_address = user.user_address
    user_db_model.user_email = user.user_email
    user_db_model.user_phone = user.user_phone
    user_db_model.user_identity_code = user.user_identity_code
    user_db_model.user_password = user.password
    user_db_model.date_created = datetime.now()
    db.add(user_db_model)
    db.commit()
    db.refresh(user_db_model)
    return user_db_model


def update_user(db: Session, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if not db_user:
        return None
    db_user.user_name = user.username
    db_user.user_password = user.password
    db_user.user_address = user.user_address
    db_user.user_email = user.user_email
    db_user.user_phone = user.user_phone
    db_user.user_identity_code = user.user_identity_code
    db_user.date_updated = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def create_product_tag(db: Session, product_tag: schemas.ProductTag):
    db_product_tag = models.ProductTag()
    db_product_tag.tag_name = product_tag.tag_name
    db_product_tag.create_date = datetime.now()

    db.add(db_product_tag)
    db.commit()
    db.refresh(db_product_tag)
    return db_product_tag


def update_product_tag(db: Session, product_tag: schemas.ProductTagUpdate):
    db_product_tag = db.query(models.ProductTag).filter(
        models.ProductTag.id == product_tag.id).first()
    db_product_tag.tag_name = product_tag.tag_name
    db_product_tag.update_date = datetime.now()

    db.commit()
    db.refresh(db_product_tag)
    return db_product_tag


def create_product(db: Session, product: schemas.ProductBase):
    db_product = models.Product()
    db_product.product_name = product.product_name
    db_product.product_price = product.product_price
    db_product.product_tag_id = product.product_tag_id
    db_product.create_date = datetime.now()
    db_product.update_date = datetime.now()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(
        models.Product.id == product.id).first()
    db_product.product_name = product.product_name
    db_product.product_price = product.product_price
    db_product.product_tag_id = product.product_tag_id
    db_product.update_date = datetime.now()
    db.commit()
    db.refresh(db_product)
    return db_product


def create_company(db: Session, company: schemas.CompanyBase):
    db_company = models.Company()
    db_company.company_name = company.company_name
    db_company.user_id = company.user_id
    db_company.company_address = company.company_address
    db_company.company_phone = company.company_phone
    db_company.create_date = datetime.now()
    db_company.update_date = datetime.now()
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, company: schemas.CompanyUpdate):
    db_company = db.query(models.Company).filter(
        models.Company.id == company.id).first()
    db_company.company_name = company.company_name
    db_company.company_address = company.company_address
    db_company.company_phone = company.company_phone
    db_company.user_id = company.user_id
    db_company.update_date = datetime.now()
    db.commit()
    db.refresh(db_company)
    return db_company


def create_bookmark(db: Session, user_bookmark: schemas.UserBookMark):
    db_user_bookmark = models.UserBookmark()
    db_user_bookmark.create_date = datetime.now()
    db_user_bookmark.product_id = user_bookmark.product_id
    db_user_bookmark.user_id = user_bookmark.user_id
    db_user_bookmark.is_favorite = user_bookmark.is_favorite
    db.add(db_user_bookmark)
    db.commit()
    db.refresh(db_user_bookmark)
    return db_user_bookmark


def add_bookmark_to_user(db: Session, user_bookmark: schemas.UserBookMark):
    related_user = db.query(models.User).filter(
        models.User.id == user_bookmark.user_id).first()
    created_bookmark = create_bookmark(db=db, user_bookmark=user_bookmark)
    related_user.user_bookmark_id = created_bookmark.id
    db.commit()
    db.refresh(related_user)
    return related_user


def create_bank_account(db: Session, bank_account: schemas.BankAccountBase):
    db_bank_account = models.BankAccount()
    db_bank_account.bank_name = bank_account.bank_name
    db_bank_account.bank_address = bank_account.bank_address
    db_bank_account.bank_account_no = bank_account.bank_account_no
    db_bank_account.bank_phone_number = bank_account.bank_phone_number
    db_bank_account.bank_province = bank_account.bank_province
    db_bank_account.bank_city = bank_account.bank_city
    db_bank_account.bank_card_no = bank_account.bank_card_no
    db_bank_account.user_id = bank_account.user_id
    db.add(db_bank_account)
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account


def update_bank_account(db: Session, bank_account: schemas.BankAccountUpdate):
    db_bank_account = db.query(models.BankAccount).filter(
        models.BankAccount.id == bank_account.id).first()
    db_bank_account.bank_name = bank_account.bank_name
    db_bank_account.bank_address = bank_account.bank_address
    db_bank_account.bank_account_no = bank_account.bank_account_no
    db_bank_account.bank_phone_number = bank_account.bank_phone_number
    db_bank_account.bank_province = bank_account.bank_province
    db_bank_account.bank_city = bank_account.bank_city
    db_bank_account.bank_card_no = bank_account.bank_card_no
    db_bank_account.user_id = bank_account.user_id
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account


def add_bank_account_to_user(db: Session, bank_account: schemas.BankAccountBase):
    related_user = db.query(models.User).filter(models.User.id==bank_account.user_id).first()
    created_bank_account = create_bank_account(db=db, bank_account=bank_account)
    related_user.user_bank_account_id = created_bank_account.id
    db.commit()
    db.refresh(related_user)
    return related_user


def create_invoice(db: Session, invoice = schemas.Invoice):
    db_invoice = models.Invoice()
    db_invoice.user_id = invoice.user_id
    db_invoice.product_id = invoice.product_id
    db_invoice.company_id = invoice.company_id
    db_invoice.status = invoice.status
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def update_invoice(db: Session, invoice = schemas.InvoiceUpdate):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id==invoice.id).first()
    db_invoice.user_id = invoice.user_id
    db_invoice.product_id = invoice.product_id
    db_invoice.company_id = invoice.company_id
    db_invoice.status = invoice.status
    db.commit()
    db.refresh(db_invoice)
    return db_invoice



def delete_user(db:Session, user_id:int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user



def delete_product(db:Session, product_id:int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product


def delete_company(db:Session, company_id:int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    db.delete(db_company)
    db.commit()
    return db_company


def delete_product_tag(db:Session, tag_id:int):
    db_tag = db.query(models.ProductTag).filter(models.ProductTag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()
    return db_tag



def delete_bookmark(db:Session, bookmark_id:int):
    db_bookmark = db.query(models.UserBookmark).filter(models.UserBookmark.id == bookmark_id).first()
    db.delete(db_bookmark)
    db.commit()
    return db_bookmark



def delete_bank_account(db:Session, bank_account_id:int):
    db_bank_account = db.query(models.BankAccount).filter(models.BankAccount.id == bank_account_id).first()
    db.delete(db_bank_account)
    db.commit()
    return db_bank_account


def delete_invoice(db: Session, invoice_id:int):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    db.delete(db_invoice)
    db.commit()
    return db_invoice


