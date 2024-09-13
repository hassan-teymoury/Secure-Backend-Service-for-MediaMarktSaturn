from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
import uvicorn
import os
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import secrets


JWT_SECRET_KEY = secrets.token_hex(32)
if not os.environ["JWT_SECRET_KEY"]:
    os.environ["JWT_SECRET_KEY"] = JWT_SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
APP_PORT = int(os.getenv("APP_PORT"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, db: Session = Depends(get_db)):
    all_users = crud.get_users(db=db)
    all_user_names = [user.user_name for user in all_users]
    if username in all_user_names:
        user_idx = all_user_names.index(username)
        return all_users[user_idx]


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.user_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv(
            "JWT_SECRET_KEY"), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
) -> schemas.Token:
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )

    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[models.User, Depends(get_current_user)]):
    users = crud.get_users(db=db)
    return users


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int,
                   db: Annotated[Session, Depends(get_db)],
                   current_user: Annotated[models.User, Depends(get_current_user)]):

    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found"
        )

    return user


@app.get("/product_tags", status_code=status.HTTP_200_OK)
async def get_all_product_tags(db: Annotated[Session, Depends(get_db)],
                               current_user: Annotated[models.User, Depends(get_current_user)]):
    product_tags = crud.get_product_tags(db=db)
    return product_tags


@app.get("/product_tags/{tag_id}", status_code=status.HTTP_200_OK)
async def get_product_tag(tag_id,
                          db: Annotated[Session, Depends(get_db)],
                          current_user: Annotated[models.User, Depends(get_current_user)]):
    product_tag = crud.get_product_tag(db=db, tag_id=tag_id)
    if not product_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product tag with id {tag_id} not found"
        )
    return product_tag


@app.get("/companies", status_code=status.HTTP_200_OK)
async def get_all_companies(db: Annotated[Session, Depends(get_db)],
                            current_user: Annotated[models.User, Depends(get_current_user)]):
    companies = crud.get_companies(db=db)
    return companies


@app.get("/companies/{company_id}", status_code=status.HTTP_200_OK)
async def get_company(company_id,
                      db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)]):
    company = crud.get_company(db=db, company_id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found"
        )
    return company


@app.get("/products", status_code=status.HTTP_200_OK)
async def get_all_products(db: Annotated[Session, Depends(get_db)],
                           current_user: Annotated[models.User, Depends(get_current_user)]):
    products = crud.get_products(db=db)
    return products


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: int,
                      db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)]):
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found"
        )
    return product


@app.get("/invoices", status_code=status.HTTP_200_OK)
async def get_all_invoices(db: Annotated[Session, Depends(get_db)],
                           current_user: Annotated[models.User, Depends(get_current_user)]):
    invoices = crud.get_invoices(db=db)
    return invoices


@app.get("/invoices/{invoice_id}", status_code=status.HTTP_200_OK)
async def get_invoice(invoice_id: int,
                      db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)]):
    invoice = crud.get_invoice(db=db, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with id {invoice_id} not found"
        )
    return invoice


@app.get("/bank_accounts", status_code=status.HTTP_200_OK)
async def get_all_bank_accounts(db: Annotated[Session, Depends(get_db)],
                                current_user: Annotated[models.User, Depends(get_current_user)]):
    bank_accounts = crud.get_bank_accounts(db=db)
    return bank_accounts


@app.get("/bank_accounts/{user_id}", status_code=status.HTTP_200_OK)
async def get_bank_account(user_id: int,
                           db: Annotated[Session, Depends(get_db)],
                           current_user: Annotated[models.User, Depends(get_current_user)]):
    bank_account = crud.get_bank_account(db=db, user_id=user_id)
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Bank Account for user with id {user_id} not found"
        )
    return bank_account


@app.get("/user_bookmarks", status_code=status.HTTP_200_OK)
async def get_all_user_bookmarks(db: Annotated[Session, Depends(get_db)],
                                 current_user: Annotated[models.User, Depends(get_current_user)]):
    user_bookmarks = crud.get_bookmarks(db=db)
    return user_bookmarks


@app.get("/user_bookmarks/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_bookmark(user_id: int,
                            db: Annotated[Session, Depends(get_db)],
                            current_user: Annotated[models.User, Depends(get_current_user)]):

    user_bookmark = crud.get_bookmark(db=db, user_id=user_id)
    if not user_bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User bookmark for user with id {user_id} not found"
        )
    return user_bookmark


@app.post("/users/create", status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)],
                      user: Annotated[schemas.UserCreate, Depends()]):
    all_users = crud.get_users(db=db)
    user_emails = [db_user.user_email for db_user in all_users]
    if user.user_email in user_emails:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"User with email {user.user_email} already exists"
        )
    created_user = crud.create_user(db=db, user=user)
    return created_user


@app.put("/users/update", status_code=status.HTTP_201_CREATED)
async def update_user(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)],
                      user: Annotated[schemas.UserUpdate, Depends()]):
    updated_user = crud.update_user(db=db, user=user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user.id} not found"
        )
    return updated_user


@app.post("/product_tags/create", status_code=status.HTTP_201_CREATED)
async def create_product_tag(db: Annotated[Session, Depends(get_db)],
                             current_user: Annotated[models.User, Depends(get_current_user)],
                             product_tag: Annotated[schemas.ProductTag, Depends()]):
    product_tags = crud.get_product_tags(db=db)
    tag_names = [db_p_tag.tag_name for db_p_tag in product_tags] if len(
        product_tags) > 0 else []

    if product_tag.tag_name in tag_names:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Product tag with name {product_tag.tag_name} already exists"
        )
    created_product_tag = crud.create_product_tag(db=db, user=product_tag)
    return created_product_tag


@app.put("/product_tags/update", status_code=status.HTTP_201_CREATED)
async def update_product_tag(db: Annotated[Session, Depends(get_db)],
                             current_user: Annotated[models.User, Depends(get_current_user)],
                             product_tag: Annotated[schemas.ProductTagUpdate, Depends()]):

    updated_product_tag = crud.update_product_tag(
        db=db, product_tag=product_tag)
    if not updated_product_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product Tag with id {updated_product_tag.id} not found"
        )
    return updated_product_tag


@app.post("/products/create", status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Depends(get_current_user)],
                         product: Annotated[schemas.ProductBase, Depends()]):

    created_product = crud.create_product(db=db, product=product)
    return created_product


@app.put("/products/update", status_code=status.HTTP_201_CREATED)
async def update_product(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Depends(get_current_user)],
                         product: Annotated[schemas.ProductTagUpdate, Depends()]):

    updated_product = crud.update_product(db=db, product=product)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {updated_product.id} not found"
        )
    return updated_product


@app.post("/companies/create", status_code=status.HTTP_201_CREATED)
async def create_company(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Depends(get_current_user)],
                         company: Annotated[schemas.CompanyBase, Depends()]):
    all_companies = crud.get_companies(db=db)
    company_names = [db_company.company_name for db_company in all_companies] if len(
        all_companies) > 0 else []
    if company.company_name in company_names:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Company with name {company.company_name} already exists"
        )
    created_company = crud.create_company(db=db, company=company)
    return created_company


@app.put("/companies/update", status_code=status.HTTP_201_CREATED)
async def update_company(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Depends(get_current_user)],
                         company: Annotated[schemas.CompanyUpdate, Depends()]):

    updated_company = crud.update_company(db=db, company=company)
    if not updated_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company.id} not found"
        )
    return updated_company


@app.post("/bank_accounts/create", status_code=status.HTTP_201_CREATED)
async def create_bank_account(db: Annotated[Session, Depends(get_db)],
                              current_user: Annotated[models.User, Depends(get_current_user)],
                              bank_account: Annotated[schemas.BankAccountBase, Depends()]):
    all_bank_accounts = crud.get_bank_accounts(db=db)
    bank_account_numbers = [db_bank_account.bank_account_no for db_bank_account in all_bank_accounts] if len(
        all_bank_accounts) > 0 else []
    if bank_account.bank_account_no in bank_account_numbers:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Bank with account number {bank_account.bank_account_no} already exists"
        )
    created_bank_account = crud.create_bank_account(
        db=db, bank_account=bank_account)
    return created_bank_account


@app.put("/bank_accounts/update", status_code=status.HTTP_201_CREATED)
async def update_bank_account(db: Annotated[Session, Depends(get_db)],
                              current_user: Annotated[models.User, Depends(get_current_user)],
                              bank_account: Annotated[schemas.BankAccountUpdate, Depends()]):

    updated_bank_account = crud.update_bank_account(
        db=db, bank_account=bank_account)
    if not updated_bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Bank account with id {bank_account.id} not found"
        )
    return updated_bank_account


@app.post("/user_bookmarks/create", status_code=status.HTTP_201_CREATED)
async def create_user_bookmark(db: Annotated[Session, Depends(get_db)],
                               current_user: Annotated[models.User, Depends(get_current_user)],
                               user_bookmark: Annotated[schemas.UserBookMark, Depends()]):

    user_bookmarks = crud.get_bookmark(db=db, user_id=user_bookmark.user_id)
    bookmark_products = [db_user_bookmark.product_id for db_user_bookmark in user_bookmarks] if len(
        user_bookmarks) > 0 else []
    if user_bookmark.product_id in bookmark_products:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Bookmark with product id {user_bookmark.product_id} for user with id {user_bookmark.user_id} already exists"
        )
    created_bookmark = crud.create_bookmark(db=db, user_bookmark=user_bookmark)
    return created_bookmark


@app.post("/invoices/create_invoice", status_code=status.HTTP_200_OK)
async def create_invoice(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Depends(get_current_user)],
                         invoice: Annotated[schemas.Invoice, Depends()]):
    created_invoice = crud.create_invoice(db=db, invoice=invoice)
    return created_invoice


@app.put("/invoices/update_invoice", status_code=status.HTTP_200_OK)
async def update_invoices(db: Annotated[Session, Depends(get_db)],
                          current_user: Annotated[models.User, Depends(get_current_user)],
                          invoice: Annotated[schemas.InvoiceUpdate, Depends()]):
    updated_invoice = crud.update_invoice(db=db, invoice=invoice)
    if not updated_invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with id {updated_invoice.id} not found"
        )
    return updated_invoice


@app.delete("/users/remove/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)],
                      user_id: int):
    user_ = crud.get_user(db=db, user_id=user_id)
    if not user_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found"
        )

    deleted_user = crud.delete_user(db=db, user_id=user_id)
    return deleted_user


@app.delete("/products/remove/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Depends(get_current_user)],
                         product_id: int):
    product_ = crud.get_product(db=db, product_id=product_id)
    if not product_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found"
        )

    deleted_product = crud.delete_product(db=db, product_id=product_id)
    return deleted_product


@app.delete("/companies/remove/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Depends(get_current_user)],
                         company_id: int):
    company_ = crud.get_company(db=db, company_id=company_id)
    if not company_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found"
        )

    deleted_company = crud.delete_company(db=db, company_id=company_id)
    return deleted_company


@app.delete("/product_tags/remove/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_tag(db: Annotated[Session, Depends(get_db)],
                             current_user: Annotated[models.User, Depends(get_current_user)],
                             tag_id: int):
    tag_ = crud.get_product_tag(db=db, tag_id=tag_id)
    if not tag_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product Tag with id {tag_id} not found"
        )

    deleted_tag = crud.delete_product_tag(db=db, tag_id=tag_id)
    return deleted_tag


@app.delete("/bookmarks/remove/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)],
                      user_id: int):
    user_bookmark = crud.get_bookmark(db, user_id)
    if not user_bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Bookmark for user with id {user_id} not found"
        )

    deleted_bookmark = crud.delete_bookmark(
        db=db, bookmark_id=user_bookmark.id)
    return deleted_bookmark


@app.delete("/bank_accounts/remove/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)],
                      user_id: int):
    user_bank_account = crud.get_bank_account(db=db, user_id=user_id)
    if not user_bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Bank account for user with id {user_id} not found"
        )

    deleted_bank_account = crud.delete_bank_account(
        db=db, bank_account_id=user_bank_account.id)
    return deleted_bank_account


@app.delete("/invoices/remove/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[models.User, Depends(get_current_user)],
                      invoice_id: int):
    invoice_ = crud.get_invoice(db=db, invoice_id=invoice_id)
    if not invoice_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with id {invoice_id} not found"
        )

    deleted_invoice = crud.delete_invoice(db=db, invoice_id=invoice_id)
    return deleted_invoice


if __name__ == "__main__":
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=APP_PORT)
