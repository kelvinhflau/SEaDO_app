from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from src.core.models import Products, Purchases
from .forms import CreateProductsForm, DeleteProductsForm, UpdateProductsForm, CreatePurchasesForm, UpdatePurchasesForm, DeletePurchasesForm
from src import db

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
@login_required
def home():
    return render_template("core/index.html")

@core_bp.route("/products_create", methods=["GET", "POST"])
@login_required
def products_create():  
    products = Products.query

    form = CreateProductsForm(request.form)
    if form.validate_on_submit():
        product = Products(name=form.name.data,
                           price=form.price.data,
                           manufacturer=form.manufacturer.data)
        db.session.add(product)
        db.session.commit()

        flash("Product added into database")
        return render_template("core/products_create.html", products=products, form=form)

    return render_template("core/products_create.html", products=products, form=form)

@core_bp.route("/products_read", methods=["GET", "POST"])
@login_required
def products_read():
    products = Products.query
    return render_template("core/products_read.html", products = products)

@core_bp.route("/products_update", methods=["GET", "POST"])
@login_required
def products_update():
    products = Products.query

    form = UpdateProductsForm(request.form)
    if form.validate_on_submit():
        product = Products.query.filter_by(product_id=form.product_id.data).first()
        if form.name.data:
            product.name = form.name.data
        if form.price.data:
            product.price = form.price.data
        if form.manufacturer.data:
            product.manufacturer = form.manufacturer.data
        db.session.commit()

        flash("Product updated in database")
        return render_template("core/products_update.html", products=products, form=form)

    return render_template("core/products_update.html", products=products, form=form)

@core_bp.route("/products_delete", methods=["GET", "POST"])
@login_required
def products_delete():
    products = Products.query

    form = DeleteProductsForm(request.form)

    if not current_user.is_admin:
        flash("Only admins can perform this action")
        return render_template("core/products_delete.html", products=products, form=form)

    if form.validate_on_submit():
        Products.query.filter_by(product_id=form.product_id.data).delete()
        db.session.commit()

        flash("Product deleted in database")
        return render_template("core/products_delete.html", products=products, form=form)

    return render_template("core/products_delete.html", products=products, form=form)

@core_bp.route("/purchases_create", methods=["GET", "POST"])
@login_required
def purchases_create():
    purchases = db.session.query(Purchases, Products).filter(Purchases.product_id == Products.product_id)

    form = CreatePurchasesForm(request.form)
    if form.validate_on_submit():
        purchase = Purchases(purchase_date=form.purchase_date.data,
                             number_of_purchases=form.number_of_purchases.data,
                             product_id=form.product_id.data)
        db.session.add(purchase)
        db.session.commit()

        flash("Purchase added into database")
        return render_template("core/purchases_create.html", purchases=purchases, form=form)

    return render_template("core/purchases_create.html", purchases=purchases, form=form)

@core_bp.route("/purchases_read", methods=["GET", "POST"])
@login_required
def purchases_read():
    purchases = db.session.query(Purchases, Products).filter(Purchases.product_id == Products.product_id)
    return render_template("core/purchases_read.html", purchases = purchases)

@core_bp.route("/purchases_update", methods=["GET", "POST"])
@login_required
def purchases_update():
    purchases = db.session.query(Purchases, Products).filter(Purchases.product_id == Products.product_id)

    form = UpdatePurchasesForm(request.form)
    if form.validate_on_submit():
        purchase = Purchases.query.filter_by(purchase_id=form.purchase_id.data).first()
        if form.purchase_date.data:
            purchase.purchase_date = form.purchase_date.data
        if form.number_of_purchases.data:
            purchase.number_of_purchases = form.number_of_purchases.data
        if form.product_id.data:
            purchase.product_id = form.product_id.data
        db.session.commit()

        flash("Purchase updated in database")
        return render_template("core/purchases_update.html", purchases=purchases, form=form)

    return render_template("core/purchases_update.html", purchases=purchases, form=form)


@core_bp.route("/purchases_delete", methods=["GET", "POST"])
@login_required
def purchases_delete():
    purchases = db.session.query(Purchases, Products).filter(Purchases.product_id == Products.product_id)

    form = DeletePurchasesForm(request.form)
    if not current_user.is_admin:
        flash("Only admins can perform this action")
        return render_template("core/purchases_delete.html", purchases=purchases, form=form)
    
    if form.validate_on_submit():
        Purchases.query.filter_by(purchase_id=form.purchase_id.data).delete()
        db.session.commit()

        flash("Purchase deleted in database")
        return render_template("core/purchases_delete.html", purchases=purchases, form=form)

    return render_template("core/purchases_delete.html", purchases=purchases, form=form)