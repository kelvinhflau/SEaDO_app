from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from src.core.models import Products, Purchases
from datetime import date


class CreateProductsForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=5, max=30)]
    )
    price = DecimalField(
        "Price (£)", places=2, validators=[NumberRange(min=0, message="Price must be greater than 0")]
    )
    manufacturer = StringField(
        "Manufacturer", validators=[DataRequired(), Length(min=3, max=30)]
    )

    def validate(self, extra_validators=None):
        initial_validation = super(CreateProductsForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        price_data = str(self.price.data)
        if "." in price_data:
            decimals = price_data[price_data.index(".")+1:]
            if len(decimals)>2:
                self.price.errors.append("You cannot input fractions of pennies.")
                return False
        
        if self.price.data > 1000000:
            self.price.errors.append("It seems like a big purchase. Are you sure you typed in the price correctly?")
            return False

        product = Products.query.filter_by(name=self.name.data,
                                           price=self.price.data,
                                           manufacturer=self.manufacturer.data).first()
        if product:
            self.name.errors.append("Product already registered")
            return False
        return True
    
class UpdateProductsForm(FlaskForm):
    product_id = IntegerField(
        "Product_id", validators=[DataRequired(), NumberRange(min=1, message="ID must be greater than 0")]
    )
    name = StringField(
        "Name", validators=[Optional(), Length(min=5, max=30)]
    )
    price = DecimalField(
        "Price", places=2, validators=[Optional(), NumberRange(min=0, message="Price must be greater than 0")]
    )
    manufacturer = StringField(
        "Manufacturer", validators=[Optional(), Length(min=3, max=30)]
    )

    
    def validate(self, extra_validators=None):
        initial_validation = super(UpdateProductsForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        price_data = str(self.price.data)
        if "." in price_data:
            decimals = price_data[price_data.index(".")+1:]
            if len(decimals)>2:
                self.price.errors.append("You cannot input fractions of pennies.")
                return False
        
        if len(price_data) > 10:
            self.price.errors.append("It seems like a big purchase. Are you sure you typed in the price correctly?")
            return False
        
        product = Products.query.filter_by(product_id=self.product_id.data).first()
        if not product:
            self.product_id.errors.append("Product does not exist. Select a correct ID")
            return False
        
        if self.name.data is not None:
            if self.name.data == product.name:
                self.name.errors.append("Same name already in the database")
        if self.price.data is not None:
            if self.price.data == product.price:
                self.price.errors.append("Same price already in the database")
        if self.manufacturer.data is not None:
            if self.manufacturer.data == product.manufacturer:
                self.manufacturer.errors.append("Same manufacturer already in the database")
        return True
    
class DeleteProductsForm(FlaskForm):
    product_id = IntegerField(
        "Product_id", validators=[DataRequired(), NumberRange(min=1, message="ID must be greater than 0")]
    )

    def validate(self, extra_validators=None):
        initial_validation = super(DeleteProductsForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        product = Products.query.filter_by(product_id=self.product_id.data).first()
        if not product:
            self.product_id.errors.append("id doesn't exist")
            return False
        return True

class CreatePurchasesForm(FlaskForm):
    purchase_date = DateField(
        "Purchase date", validators=[DataRequired()]
    )
    number_of_purchases = IntegerField(
        "Number of Purchases ", validators=[DataRequired(), NumberRange(min=1, message="Purchase amount must be greater than 0")]
    )
    product_id = IntegerField(
        "Product id", validators=[DataRequired(), NumberRange(min=1, message="ID must be greater than 0")]
    )

    def validate(self, extra_validators=None):
        initial_validation = super(CreatePurchasesForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        if self.purchase_date.data < date(1970,1,1):
            self.purchase_date.errors.append("Purchase is a long time ago. Is the date correct?")
            return False
        
        if self.purchase_date.data > date.today():
            self.purchase_date.errors.append("Only input purchase after you've bought the assets")
            return False
        
        if self.number_of_purchases.data > 1000000:
            self.number_of_purchases.errors.append("You have ordered a lot of this asset. Is this correct?")
            return False

        purchase = Purchases.query.filter_by(purchase_date=self.purchase_date.data,
                                             number_of_purchases=self.number_of_purchases.data,
                                             product_id=self.product_id.data).first()
        if purchase:
            self.purchase_date.errors.append("Purchase already in database")
            return False

        product_exist = Products.query.filter_by(product_id=self.product_id.data).first()
        if not product_exist:
            self.product_id.errors.append("Product ID does not exist in the database")
            return False
        
        return True
    
class UpdatePurchasesForm(FlaskForm):
    purchase_id = IntegerField(
        "Purchase_id", validators=[DataRequired(), NumberRange(min=1, message="ID must be greater than 0")]
    )
    purchase_date = DateField(
        "Purchase date", validators=[Optional()]
    )
    number_of_purchases = IntegerField(
        "Number of Purchases ", validators=[Optional(), NumberRange(min=1, message="Purchase amount must be greater than 0")]
    )
    product_id = IntegerField(
        "Product id", validators=[Optional(), NumberRange(min=1, message="ID must be greater than 0")]
    )

    def validate(self, extra_validators=None):
        initial_validation = super(UpdatePurchasesForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        purchase = Purchases.query.filter_by(purchase_id=self.purchase_id.data).first()
        if not purchase:
            self.purchase_id.errors.append("Purchase does not exist. Select a correct ID")
            return False
        
        if self.purchase_date.data is not None:
            
            if self.purchase_date.data < date(1970,1,1):
                self.purchase_date.errors.append("Purchase is a long time ago. Is the date correct?")
                return False
            
            if self.purchase_date.data > date.today():
                self.purchase_date.errors.append("Only update purchase after you've bought the assets")
                return False
            
            if self.purchase_date.data == purchase.purchase_date:
                self.purchase_date.errors.append("Same purchase date already in the database")
        

        if self.number_of_purchases.data is not None:
            if self.number_of_purchases.data > 1000000:
                self.number_of_purchases.errors.append("You have ordered a lot of this asset. Is this correct?")
                return False
            
            if self.number_of_purchases.data == purchase.number_of_purchases:
                self.number_of_purchases.errors.append("Same number of purchases already in the database")

        product = Products.query.filter_by(product_id=self.product_id.data).first()
        product_id_missing = (self.product_id.data is None) 
        if (not product_id_missing) and (not product):
            self.product_id.errors.append("Product ID does not exist in the database")
            return False
        
        if self.product_id.data is not None:
            if self.product_id.data == purchase.product_id:
                self.product_id.errors.append("Same product id for purchase already in the database")
        return True


class DeletePurchasesForm(FlaskForm):
    purchase_id = IntegerField(
        "Purchase_id", validators=[DataRequired(), NumberRange(min=1, message="ID must be greater than 0")]
    )

    def validate(self, extra_validators=None):
        initial_validation = super(DeletePurchasesForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        purchase = Purchases.query.filter_by(purchase_id=self.purchase_id.data).first()
        if not purchase:
            self.purchase_id.errors.append("id doesn't exist")
            return False
        return True