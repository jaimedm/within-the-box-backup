from sqlalchemy import Column, Table, ForeignKey, Boolean, Integer, String, DECIMAL, ARRAY, DateTime, Uuid
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship, backref, validates
import uuid
from database.database import Base

#------------------------------------------------------------------------------------------------------------------------------------
# MUDAR O NOME DO FICHEIRO 
# Example to delete
class UserForTab1(Base):
    __tablename__ = "tab1"

    name = Column("name", String, primary_key=True, index=True)
    age = Column("age", Integer, index=True)
    active = Column("active", Boolean, index=True, default=False)

    #Column(name="name", type=String, nullable=False, primary_key=True)

#------------------------------------------------------------------------------------------------------------------------------------

# Association table: it has foreign key constraints
# established that refer to products and sets' tables.
product_previous_sets = Table(
    "product_previous_sets",
    Base.metadata,
    Column("previous_sets", Uuid, ForeignKey("previous_sets.id")),
    Column("products", Uuid, ForeignKey("products.id")),
)

# Product model
class Product(Base):
    __tablename__ = "products"

    # UUID is created automatically
    id = Column("id", Uuid, primary_key=True, unique=True, index=True, nullable=False, default= uuid.uuid4)
    name = Column("name", String(25), index=True, nullable=False)
    url = Column("url", URLType, index=True, nullable=False)
    image_source = Column("image_source", URLType, index=True, nullable=False)
    description = Column("description", String(50), index=True, nullable=True, default=None)
    # 8 digits in total, 3 decimal places
    length = Column("length", DECIMAL(8, 3), index=True, nullable=False)
    width = Column("width", DECIMAL(8, 3), index=True, nullable=False)
    height = Column("height", DECIMAL(8, 3), index=True, nullable=False)
    weight = Column("weight", DECIMAL(8, 3), index=True, nullable=False)
    lidded = Column("lidded", Boolean, index=True, nullable=False, default=False)
    price = Column("price", DECIMAL(7, 3), index=True, nullable=False)
    currency = Column("currency", String(5), index=True, nullable=False)
    materials = Column("materials", ARRAY(String(15)), index=True, nullable=True, default=None)
    colors = Column("colors", ARRAY(String(15)), index=True, nullable=True, default=None)
    brand = Column("brand", String(15), index=True, nullable=True, default=None)

    # Validator for the read-only property of id. When creating 
    # a new object, the id must be None, since UUID is generated internally
    @validates("id")
    def check_id_readonly(self, key, id) -> Uuid:
        if id is not None:
            raise ValueError(f"Model: You can't set 'id', it is read-only!")
        return id

    # def __repr__(self):
    #     return f"Product(id = {self.id}, name = {self.name}, url = {self.ur}, description = {self.description}, \
    #                 length = {self.length}, width = {self.width}, height = {self.height}, \
    #                 weight = {self.weight}, lidded = {self.lidded}, price = {self.price}, \
    #                 currency = {self.currency}, materials = {self.materials}, brand = {self.brand},)"

# Model for the calculated sets stored
class ProductSet(Base):
    __tablename__ = "previous_sets"

    id = Column("id", Uuid, primary_key=True, unique=True, index=True, nullable=False, default= uuid.uuid4)
    timestamp = Column("timestamp", DateTime, index=True, nullable=False)
    # The relationship is not loaded until 
    # accessed (the default lazy=True). If a product
    # is deleted, the product sets with that product
    # in their product list with it will be deleted too.
    product_list = relationship("Product", secondary=product_previous_sets, backref=backref("product_sets", cascade="all, delete"), lazy=True)
    # Configurations
    n = Column("n", Integer, index=True, nullable=False)
    container_dimensions = Column("container", ARRAY(DECIMAL(8, 3)), index=True, nullable=False)
    # NOTE: this is relative to the previous version
    #layout = Column("layout", ARRAY(Integer), index=True, nullable=False)

    # Filters
    # TODO
    #filters = None