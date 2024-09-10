from sqlalchemy import Boolean, Column, ForeignKey, Integer, \
    String, Float, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, name="user_name")
    user_phone = Column(String, name="user_phone")
    user_identity_code = Column(String, name="user_id_code")
    user_status = Column(String, name="user_status")
    user_email = Column(String, name="user_email")
    user_password = Column(String, name="user_password")
    last_login = Column(DateTime, name="last_login")
    last_fp_app_code = Column(String, name="last_fp_app_code")
    last_fp_req = Column(DateTime, name="last_fp_req")
    active = Column(Boolean, name="active")
    last_fp_req_token = Column(String, name="last_fp_req_token")
    last_login_token = Column(String, name="last_login_token")
    date_created =  Column(DateTime, name="date_created")
    user_bookmark_id = Column(Integer, ForeignKey("user_bookmarks.id"), name="user_bookmark_id")
    user_bank_account_id = Column(Integer, ForeignKey("bank_accounts.id", name="user_bank_account_id"))
    
    
    bookmarks = relationship("UserBookmark", back_populates="user")
    user_bank_account = relationship("BankAccount", back_populates="user")
    invoice = relationship("Invoice", back_populates="user")
    
    
class ProductTag(Base):
    __tablename__ = 'product_tags'
    
    id = Column(Integer, name="id", primary_key=True, index=True)
    tag_name = Column(String, name="tag_name")
    
    product = relationship("Product", back_populates="product_tag")
    


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, name="product_name")
    product_tag_id = Column(String, ForeignKey('product_tags.id'), name="product_tag_id")
    product_price = Float(String, name="product_price")
    company_id = Column(Integer, ForeignKey("companies.id"), name="company_id")
    
    product_tag = relationship("ProductTag", back_populates="product")
    bookmarks = relationship("UserBookmark", back_populates="product")
    invoice = relationship("Invoice", back_populates="product")
    
    
class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, name="bank_name")
    bank_account_no = Column(String, name="bank_account_no")
    bank_phone_number = Column(String, name="bank_phone_number")
    bank_card_no = Column(String, name="bank_card_no")
    
    company = relationship("Company", back_populates="company_bank_account")
    user = relationship("User", back_populates="user_bank_account")



class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, name="id", index=True)
    company_name = Column(String, name="company_name")
    company_address = Column(String, name="company_address")
    company_phone = Column(String, name="company_phone")
    company_bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), name="company_bank_account_id")

    company_bank_account = relationship("BankAccount", back_populates="company")
    invoice = relationship("Invoice", back_populates="company")




class UserBookmark(Base):
    __tablename__ = "user_bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_favorite = Column(Boolean, name="is_important")
    
    user = relationship("User", back_populates="bookmarks")
    product = relationship("Product", back_populates="bookmarks")
    


class Invoice(Base):
    
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), name="product_id")
    user_id = Column(Integer, ForeignKey("users.id"), name="user_id")
    company_id = Column(Integer, ForeignKey("companies.id"), name="company_id")
    status = Column(String, name="status") # Selections: {"apporoved", "shipped", "delivered"}
    
    product = relationship("Product", back_populates="invoice")
    user = relationship("User", back_populates="invoice")
    company = relationship("Company", back_populates="invoice")
    
    