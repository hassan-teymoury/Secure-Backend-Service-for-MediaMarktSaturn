from sqlalchemy import Boolean, Column, ForeignKey, Integer, \
    String, Float, DateTime, Select
from sqlalchemy.orm import relationship
from database import Base






class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, name="user_name")
    user_phone = Column(String, name="user_phone", unique=True)
    user_identity_code = Column(String, name="user_id_code", unique=True)
    user_email = Column(String, name="user_email", unique=True)
    user_password = Column(String, name="user_password")
    user_address = Column(String, name="user_address", unique=True)
    last_login = Column(DateTime, name="last_login")
    last_fp_app_code = Column(String, name="last_fp_app_code")
    last_fp_req = Column(DateTime, name="last_fp_req")
    last_fp_req_token = Column(String, name="last_fp_req_token")
    last_login_token = Column(String, name="last_login_token")
    date_created =  Column(DateTime, name="date_created")
    date_updated =  Column(DateTime, name="date_updated")
    user_bookmark_id = Column(Integer, ForeignKey("user_bookmarks.id"), name="user_bookmark_id")
    user_bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), name="user_bank_account_id", unique=True)
    user_is_company = Column(Boolean, name="user_is_company", default=False)
    user_company_id = Column(Integer, ForeignKey("companies.id"), name="user_company_id", nullable=True)
    
    bookmarks = relationship("UserBookmark", back_populates="user")
    user_bank_account = relationship("BankAccount", back_populates="user")
    invoice = relationship("Invoice", back_populates="user")
    company = relationship("Company", back_populates="user")
    
class ProductTag(Base):
    __tablename__ = 'product_tags'
    
    id = Column(Integer, name="id", primary_key=True, index=True)
    tag_name = Column(String, name="tag_name")
    create_date = Column(DateTime, name="create_date")
    update_date = Column(DateTime, name="update_date")
    
    product = relationship("Product", back_populates="product_tag")
    


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, name="product_name")
    product_tag_id = Column(String, ForeignKey('product_tags.id'), name="product_tag_id")
    product_price = Float(String, name="product_price")
    company_id = Column(Integer, ForeignKey("companies.id"), name="company_id")
    create_date = Column(DateTime, name="create_date")
    update_date = Column(DateTime, name="update_date")
    
    product_tag = relationship("ProductTag", back_populates="product")
    bookmarks = relationship("UserBookmark", back_populates="product")
    invoice = relationship("Invoice", back_populates="product")
    
    
class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.'), name="user_id")
    bank_name = Column(String, name="bank_name", nullable=False)
    bank_account_no = Column(String, name="bank_account_no", nullable=True)
    bank_phone_number = Column(String, name="bank_phone_number", nullable=True)
    bank_address = Column(String, name="bank_address", nullable=True)
    bank_city = Column(String, name="bank_city", nullable=True)
    bank_province = Column(String, name="bank_province", nullable=True)
    bank_card_no = Column(String, name="bank_card_no", nullable=True)
    create_date = Column(DateTime, name="create_date")
    update_date = Column(DateTime, name="update_date")
    
    user = relationship("User", back_populates="user_bank_account")



class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, name="id", index=True)
    company_name = Column(String, name="company_name", nullable=False, )
    company_address = Column(String, name="company_address", nullable=True)
    company_phone = Column(String, name="company_phone", nullable=True)
    create_date = Column(DateTime, name="create_date")
    update_date = Column(DateTime, name="update_date")
    user_id = Column(Integer, ForeignKey('users.id'), name="user_id", nullable=True)
    
    invoice = relationship("Invoice", back_populates="company")
    user = relationship("User", back_populates="company")



class UserBookmark(Base):
    __tablename__ = "user_bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_favorite = Column(Boolean, name="is_important", default=False)
    create_date = Column(DateTime, name="create_date")
    
    user = relationship("User", back_populates="bookmarks")
    product = relationship("Product", back_populates="bookmarks")
    


class Invoice(Base):
    
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), name="product_id")
    user_id = Column(Integer, ForeignKey("users.id"), name="user_id")
    company_id = Column(Integer, ForeignKey("companies.id"), name="company_id")
    status = Column(String, name="status") # Selections: {"apporoved", "shipped", "delivered"}
    create_date = Column(DateTime, name="create_date")
    
    deliver_date = Column(DateTime, name="deliver_date")
    
    product = relationship("Product", back_populates="invoice")
    user = relationship("User", back_populates="invoice")
    company = relationship("Company", back_populates="invoice")
    
    