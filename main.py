import random

import requests
from operations.ai_photoshoot_generation import generate_photoshoot_background_task
from operations.mongo_operation import mongoOperation
from operations.mail_sending import emailOperation
from utils.constant import constant_dict
import os, json, re
from flask import (Flask, render_template, request, flash, session, send_file, jsonify, send_from_directory, url_for)
from flask_cors import CORS
import uuid
from werkzeug.utils import secure_filename, redirect
from utils.html_format import htmlOperation
from functools import wraps
from datetime import datetime, timedelta
import tempfile
import zipfile
import razorpay
from dotenv import load_dotenv
from concurrent.futures import ProcessPoolExecutor

load_dotenv()

# Razorpay client setup with version-specific configuration
razorpay_client = razorpay.Client(
    auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET'))
)

# For razorpay v1.4.1+, you can also set additional configurations
razorpay_client.set_app_details({
    "title": "Stylic AI",
    "version": "1.0.0"
})

COUPONS = {
    "HAGH56SD": 15,
    "WELCOME50": 10,
    "SAVE10": 10
}

executor = ProcessPoolExecutor(max_workers=5)

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = constant_dict.get("secreat_key")
UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Utility to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        login_dict = session.get("login_dict", {})
        if login_dict:
            all_company_data = list(mongoOperation().get_spec_data_from_coll("company_data", {"id": login_dict.get("id")}))
            login_dict["credit"] = all_company_data[0]["credit"]
            pass
        else:
            flash("Please login first...", "danger")
            return redirect("/")
        return func(*args, **kwargs)

    return decorated

@app.route("/api/check-coupon")
def check_coupon():
    code = request.args.get("code", "").upper()
    if code in COUPONS:
        return jsonify({"valid": True, "discount": COUPONS[code]})
    return jsonify({"valid": False, "discount": 0})


@app.route("/", methods=["GET", "POST"])
def login():
    try:
        login_dict = session.get("login_dict", {})
        print(login_dict)
        if login_dict:
            print("coming")
            return redirect("/dashboard")
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            print(email, password)
            if not email or not password:
                flash("Email and password are required", "danger")
                print("coming")
                return redirect("/")

            all_data = list(
                mongoOperation().get_spec_data_from_coll("login_mapping", {"email": email, "password": password}))
            if all_data:
                is_active = all_data[0]["is_active"]
                if is_active:
                    session["login_dict"] = {"id": all_data[0]["id"], "email": email, "role": all_data[0]["role"]}
                    print("coming")
                    return redirect("/dashboard")
                else:
                    print("coming")
                    flash("Please activate your account", "danger")
                    return redirect("/")
            else:
                print("coming")
                flash("Please enter correct credentials", "danger")
                return redirect("/")
        else:
            print("coming")
            return render_template("login.html")

    except Exception as e:
        print(f"{datetime.now()}: Error in login route: {str(e)}")
        flash("An error occurred during login", "danger")
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == 'POST':
            first_name = request.form.get('first_name', '').lower()
            last_name = request.form.get('last_name', '').lower()
            company_name = request.form.get('company_name', '').lower()
            email = request.form.get('email', '')
            is_privacy = request.form.get('is_privacy', '')
            password = request.form.get('password', '')
            phone = request.form.get('phone', '')

            TEMP_EMAIL_DOMAINS = {
                '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
                'tempmail.org', 'yopmail.com', 'throwaway.email',
                'temp-mail.org', 'dispostable.com', 'fakemailgenerator.com'
            }
            domain = email.split("@")[-1]
            if domain in TEMP_EMAIL_DOMAINS:
                flash("Email not valid...", "danger")
                return redirect("/")

            all_data = list(mongoOperation().get_all_data_from_coll("login_mapping"))
            allemails = [user_data["email"] for user_data in all_data]

            if email in allemails:
                flash("Company already exits. Please login with your credential...", "success")
                return redirect("/")

            allids = [user_data["id"] for user_data in all_data]
            uid = str(uuid.uuid4())
            while uid in allids:
                uid = str(uuid.uuid4())

            company_data = {
                "id": uid,
                "first_name": first_name,
                "last_name": last_name,
                "company_name": company_name,
                "email": email,
                "password": password,
                "phone": phone,
                "is_privacy_accepted": is_privacy,
                "credit": 5,
                "plan": "",
                "role": "company",
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            login_mapping_data = {
                "id": uid,
                "email": email,
                "password": password,
                "role": "company",
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            generated_otp = random.randint(100000, 999999)
            otp_html_template = htmlOperation().otp_verification_process(generated_otp)
            emailOperation().send_email(company_data["email"], "Account OTP Verification: Stylic AI", otp_html_template)
            session["register_dict"] = {"otp":generated_otp, "company_data": company_data, "login_mapping_data": login_mapping_data}
            # mongoOperation().insert_data_from_coll("company_data", company_data)
            # mongoOperation().insert_data_from_coll("login_mapping", login_mapping_data)
            flash("Do OTP Verification, Check your mail", "success")
            return redirect("/otp-verification")
        else:
            return render_template("register.html")
    except Exception as e:
        print(f"{datetime.now()}: Error in register route: {str(e)}")
        flash("An error occurred while register", "danger")
        return redirect("/register")

@app.route("/otp-verification", methods=["GET", "POST"])
def otp_verification():
    try:
        if request.method == 'POST':
            entered_otp = int(request.form.get('otp', '').lower())
            print(entered_otp, session["register_dict"]["otp"])
            if entered_otp==session["register_dict"]["otp"]:
                registered_dict = session["register_dict"]
                company_data = registered_dict["company_data"]
                login_mapping_data = registered_dict["login_mapping_data"]
                mongoOperation().insert_data_from_coll("company_data", company_data)
                try:
                    del company_data["_id"]
                except:
                    pass
                mongoOperation().insert_data_from_coll("login_mapping", login_mapping_data)
                try:
                    del login_mapping_data["_id"]
                except:
                    pass
                welcome_html = htmlOperation().welcome_user_mail(company_data["first_name"])
                emailOperation().send_email(company_data["email"], f"Welcome {company_data['first_name']}", welcome_html)
                flash("Register successful..", "success")
                return redirect("/")
            else:
                flash("Wrong OTP, Please try again..", "danger")
                return redirect("/otp-verification")
        else:
            return render_template("otp-verification.html")

    except Exception as e:
        print(f"{datetime.now()}: Error in otp verification route: {str(e)}")
        flash("An error occurred while otp verification", "danger")
        return redirect("/otp-verification")

@app.route("/resend-otp", methods=["GET", "POST"])
def resend_otp():
    try:
        company_data = session.get("register_dict", {}).get("company_data",  {})
        generated_otp = random.randint(100000, 999999)
        session["register_dict"]["otp"] = generated_otp
        otp_html_template = htmlOperation().otp_verification_process(generated_otp)
        emailOperation().send_email(company_data["email"], "Account OTP Verification: Stylic AI", otp_html_template)
        flash("OTP Sent Successfully...", "success")
        return redirect("/otp-verification")

    except Exception as e:
        print(f"{datetime.now()}: Error in resend otp route: {str(e)}")
        flash("An error occurred in OTP sending", "danger")
        return redirect("/otp-verification")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    try:
        if request.method == "POST":
            email = request.form.get("email", "").strip()

            email_condition_dict = {"email": email}
            email_data = mongoOperation().get_spec_data_from_coll("login_mapping", email_condition_dict)
            if email_data:
                if email_data[0]["is_active"]:
                    forgot_password_link = f"{constant_dict.get('domain_url', 'https://app.stylic.ai')}/reset-password?email={email}"
                    html_format = htmlOperation().forgot_password_mail_template(forgot_password_link)
                    emailOperation().send_email(email, "Stylic: Your Reset Password Link", html_format)
                    flash("Reset link sent successfully. Please check your mail", "success")
                    return redirect("/")
                else:
                    flash("Your account was disabled, Contact administration", "danger")
                    return redirect("/forgot-password")
            else:
                flash("Account not found, please do register...", "danger")
                return redirect("/forgot-password")
        else:
            return render_template("forgot-password.html")

    except Exception as e:
        print(f"{datetime.now()}: Error in forgot-password route: {str(e)}")
        flash("An error occurred during password reset", "danger")
        return render_template("forgot-password.html")

# @app.route('/payment')
# def payment():
#     return render_template('payment.html')

@app.route('/create-order', methods=['POST'])
@token_required
def create_order():
    try:
        user_id = session.get("login_dict").get("id")
        amount = int(request.json['amount']) * 100  # Convert to paisa
        currency = 'INR'
        payment_request_mapping = {
            "id": user_id,
            "credit": int(request.json['credit']),
            "order_id": str(uuid.uuid4()),
            "amount": int(request.json['amount']),
            "currency": currency,
            "created_at": datetime.utcnow()
        }
        session[f"order_{user_id}"] = payment_request_mapping
        print(payment_request_mapping)

        # Create Razorpay order - syntax for v1.4.1
        order_data = {
            'amount': amount,
            'currency': currency,
            'payment_capture': 1,  # Auto capture payment
            'notes': {
                'created_by': 'Flask App',
                'version': 'v1.4.1'
            }
        }


        order = razorpay_client.order.create(data=order_data)

        return jsonify({
            'success': True,
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
            'key_id': os.getenv('RAZORPAY_KEY_ID')
        })

    except razorpay.errors.BadRequestError as e:
        return jsonify({
            'success': False,
            'error': f'Bad Request: {str(e)}'
        }), 400
    except razorpay.errors.ServerError as e:
        return jsonify({
            'success': False,
            'error': f'Server Error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/verify-payment', methods=['POST'])
@token_required
def verify_payment():
    # Verify signature - updated method for v1.4.1
    user_id = session.get("login_dict", {}).get("id", "")
    payment_mapping = session[f"order_{user_id}"]
    mapping_dict = {
        "id": user_id,
        "order_id": "",
        "payment_id": "",
        "credit": payment_mapping.get("credit"),
        "amount": payment_mapping.get("amount"),
        "currency": payment_mapping.get("currency"),
        "status": "failed",
        "created_at": datetime.utcnow()
    }
    try:
        # Get payment details from frontend
        payment_id = request.form['razorpay_payment_id']
        order_id = request.form['razorpay_order_id']
        signature = request.form['razorpay_signature']

        # Verify payment signature using v1.4.1 syntax
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        mapping_dict["order_id"] = order_id
        mapping_dict["payment_id"] = payment_id
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            # Payment is successful
            # Here you can update your database, send confirmation emails, etc.
            print(f"Payment successful: {payment_id}")
            all_company_data = list(mongoOperation().get_spec_data_from_coll("company_data", {"id": user_id}))
            addited_credit = int(all_company_data[0]["credit"])+int(mapping_dict["credit"])
            mongoOperation().update_mongo_data("company_data", {"id": user_id}, {"credit": addited_credit})
            mapping_dict["status"]="success"
            mongoOperation().insert_data_from_coll("order_data", mapping_dict)
            flash("Payment successfully...", "success")
            return redirect('/dashboard')

        except razorpay.errors.SignatureVerificationError:
            print(f"Payment verification failed for: {payment_id}")
            mapping_dict["status"] = "failed"
            mongoOperation().insert_data_from_coll("order_data", mapping_dict)
            return redirect("/dashboard")

    except Exception as e:
        print(f"Error in payment verification: {str(e)}")
        mongoOperation().insert_data_from_coll("order_data", mapping_dict)
        return redirect("/dashboard")
#
# # Get payment details (v1.4.1 feature)
# @app.route('/payment-details/<payment_id>')
# def get_payment_details(payment_id):
#     try:
#         payment = razorpay_client.payment.fetch(payment_id)
#         return jsonify({
#             'success': True,
#             'payment': payment
#         })
#     except razorpay.errors.BadRequestError as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400
#
#
# # Refund payment (v1.4.1 syntax)
# @app.route('/refund-payment', methods=['POST'])
# def refund_payment():
#     try:
#         payment_id = request.json['payment_id']
#         amount = request.json.get('amount')  # Optional partial refund
#
#         refund_data = {}
#         if amount:
#             refund_data['amount'] = int(amount) * 100  # Convert to paisa
#
#         refund = razorpay_client.payment.refund(payment_id, refund_data)
#
#         return jsonify({
#             'success': True,
#             'refund': refund
#         })
#
#     except razorpay.errors.BadRequestError as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400
#
#
# # Get all orders (useful for admin dashboard)
# @app.route('/orders')
# def get_orders():
#     try:
#         orders = razorpay_client.order.all()
#         return jsonify({
#             'success': True,
#             'orders': orders
#         })
#     except razorpay.errors.BadRequestError as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400
#
#
# # Check payment status by order ID
# @app.route('/check-payment-status/<order_id>')
# def check_payment_status(order_id):
#     try:
#         # Get order details
#         order = razorpay_client.order.fetch(order_id)
#
#         # Get payments for this order
#         payments = razorpay_client.order.payments(order_id)
#
#         return jsonify({
#             'success': True,
#             'order': order,
#             'payments': payments
#         })
#     except razorpay.errors.BadRequestError as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    try:
        email = request.args.get("email")
        if request.method == "POST":
            password = request.form.get("password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()

            if not password or not confirm_password:
                flash("Password doesn't match", "danger")
                return redirect(f"/reset-password?email={email}")

            if len(password) < 8:
                flash("Password must be at least 8 characters long", "danger")
                return redirect(f"/reset-password?email={email}")

            if password == confirm_password:
                mongoOperation().update_mongo_data("login_mapping", {"email": email},
                                                   {"password": password})
                mongoOperation().update_mongo_data("company_data", {"email": email},
                                                   {"password": password})
                flash("Password updated successfully", "success")
                return redirect("/")
            else:
                flash("Passwords don't match", "danger")
                return redirect(f"/reset-password?email={email}")
        else:
            return render_template("reset-password.html", email=email)

    except Exception as e:
        print(f"{datetime.now()}: Error in reset-password route: {str(e)}")
        flash("An error occurred during password reset", "danger")
        return render_template("reset-password.html")

@app.route("/change-password", methods=["GET", "POST"])
@token_required
def change_password():
    try:
        email = request.args.get("email")
        if request.method == "POST":
            password = request.form.get("password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()

            if not password or not confirm_password:
                flash("Password doesn't match", "danger")
                return redirect("/dashboard")

            if len(password) < 8:
                flash("Password must be at least 8 characters long", "danger")
                return redirect("/dashboard")

            if password == confirm_password:
                mongoOperation().update_mongo_data("login_mapping", {"email": email},
                                                   {"password": password})
                mongoOperation().update_mongo_data("company_data", {"email": email},
                                                   {"password": password})
                flash("Password updated successfully", "success")
                return redirect("/dashboard")
            else:
                flash("Passwords don't match", "danger")
                return redirect(f"/dashboard")

    except Exception as e:
        print(f"{datetime.now()}: Error in change-password route: {str(e)}")
        flash("An error occurred during password change", "danger")
        return redirect("/dashboard")

@app.route("/dashboard", methods=["GET", "POST"])
@token_required
def dashboard():
    try:
        user_id = session.get("login_dict", {}).get("id", "")
        photoshoot_data = list(mongoOperation().get_spec_data_from_coll("photoshoot_data", {"id": user_id}))
        mapping_dict = {}
        mapping_dict["total_photoshoot"]=len(photoshoot_data)
        total_photos = 0
        pending_photoshoot = 0
        for photoshoot in photoshoot_data:
            status = photoshoot["status"]
            if status=="completed":
                total_photos+=len(photoshoot["selected_poses"])
            else:
                pending_photoshoot+=1

        mapping_dict["total_photos"]=total_photos
        mapping_dict["pending_photoshoot"]=pending_photoshoot
        return render_template("index.html", login_dict=session.get("login_dict", {}), mapping_dict=mapping_dict)

    except Exception as e:
        print(f"{datetime.now()}: Error in dashboard route: {str(e)}")
        return redirect("/dashboard")


@app.route("/ai-photoshoot", methods=["GET", "POST"])
@token_required
def ai_photoshoot():
    try:
        login_dict = session.get("login_dict", {})
        if request.method == "POST":
            credit = int(login_dict.get("credit"))
            user_id = login_dict.get("id")
            upper_garment_image = request.files.get("upper_garment_image")
            lower_garment_image = request.files.get("lower_garment_image")
            garment_upload_type = request.form.get("garment_upload_type")
            age_group = request.form.get("age_group")
            gender = request.form.get("gender")
            ethnicity = request.form.get("ethnicity")
            height = request.form.get("height")
            width = request.form.get("width")
            fitting = request.form.get("fitting")
            age = request.form.get("age")
            upper_garment_type = request.form.get("upper_garment_type")
            lower_garment_type = request.form.get("lower_garment_type")
            selected_poses = request.form.get("selected_poses")
            selected_poses = selected_poses.replace('["', "").replace('"]', "").replace('"', '')
            selected_poses = selected_poses.split(",") if selected_poses else []
            age = int(age) if age else 25
            print(selected_poses)

            photoshoot_data = list(mongoOperation().get_spec_data_from_coll("photoshoot_data", {"id": user_id}))
            total_pending_photos = 0
            for photoshoot in photoshoot_data:
                status = photoshoot["status"]
                if status != "completed":
                    total_pending_photos += len(photoshoot["selected_poses"])

            credit = credit - total_pending_photos
            if credit<=0:
                flash("You don't have sufficient credits..", "danger")
                return redirect("ai-photoshoot")

            photoshoot_id = str(uuid.uuid4())
            all_images = []
            os.makedirs(f"static/photoshoots_folders/{photoshoot_id}", exist_ok=True)
            lower_garment_filename = ""
            upper_garment_filename = ""

            if garment_upload_type == "upper_garment":
                exten = upper_garment_image.filename.split(".")[-1]
                if upper_garment_image and allowed_file(upper_garment_image.filename):
                    upper_garment_filename = f"{uuid.uuid4()}uppergarment.{exten}"
                    filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", upper_garment_filename)
                    upper_garment_image.save(filepath)
                    upper_garment_image_url = url_for('static',
                                                      filename=f'photoshoots_folders/{photoshoot_id}/{upper_garment_filename}',
                                                      _external=True)
                    all_images.append(upper_garment_image_url)
                else:
                    flash("Your upper garment image not valid...", "danger")
                    return redirect("/ai-photoshoot")

            elif garment_upload_type == "lower_garment":
                exten = lower_garment_image.filename.split(".")[-1]
                if lower_garment_image and allowed_file(lower_garment_image.filename):
                    lower_garment_filename = f"{uuid.uuid4()}lowergarment.{exten}"
                    filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", lower_garment_filename)
                    lower_garment_image.save(filepath)
                    lower_garment_image_url = url_for('static',
                                                      filename=f'photoshoots_folders/{photoshoot_id}/{lower_garment_filename}',
                                                      _external=True)
                    all_images.append(lower_garment_image_url)
                else:
                    flash("Your lower garment image not valid...", "danger")
                    return redirect("/ai-photoshoot")

            elif garment_upload_type == "full_body_garment":
                exten1 = upper_garment_image.filename.split(".")[-1]
                if upper_garment_image and allowed_file(upper_garment_image.filename):
                    upper_garment_filename = f"{uuid.uuid4()}uppergarment.{exten1}"
                    filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", upper_garment_filename)
                    upper_garment_image.save(filepath)
                    upper_garment_image_url = url_for('static',
                                                      filename=f'photoshoots_folders/{photoshoot_id}/{upper_garment_filename}',
                                                      _external=True)
                    all_images.append(upper_garment_image_url)
                else:
                    flash("Your upper garment image not valid...", "danger")
                    return redirect("/ai-photoshoot")

                exten = lower_garment_image.filename.split(".")[-1]
                if lower_garment_image and allowed_file(lower_garment_image.filename):
                    lower_garment_filename = f"{uuid.uuid4()}lowergarment.{exten}"
                    filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", lower_garment_filename)
                    lower_garment_image.save(filepath)
                    lower_garment_image_url = url_for('static',
                                                      filename=f'photoshoots_folders/{photoshoot_id}/{lower_garment_filename}',
                                                      _external=True)
                    all_images.append(lower_garment_image_url)
                else:
                    flash("Your lower garment image not valid...", "danger")
                    return redirect("/ai-photoshoot")

            elif garment_upload_type == "one_piece_garment":
                exten1 = upper_garment_image.filename.split(".")[-1]
                if upper_garment_image and allowed_file(upper_garment_image.filename):
                    upper_garment_filename = f"{uuid.uuid4()}uppergarment.{exten1}"
                    filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", upper_garment_filename)
                    upper_garment_image.save(filepath)
                    upper_garment_image_url = url_for('static',
                                                      filename=f'photoshoots_folders/{photoshoot_id}/{upper_garment_filename}',
                                                      _external=True)
                    all_images.append(upper_garment_image_url)
                else:
                    flash("Your one-piece garment image not valid...", "danger")
                    return redirect("/ai-photoshoot")
            else:  # Default case for other garment types
                if upper_garment_image:
                    exten1 = upper_garment_image.filename.split(".")[-1]
                    if allowed_file(upper_garment_image.filename):
                        upper_garment_filename = f"{uuid.uuid4()}uppergarment.{exten1}"
                        filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", upper_garment_filename)
                        upper_garment_image.save(filepath)
                        upper_garment_image_url = url_for('static',
                                                          filename=f'photoshoots_folders/{photoshoot_id}/{upper_garment_filename}',
                                                          _external=True)
                        all_images.append(upper_garment_image_url)
                    else:
                        flash("Your upper garment image not valid...", "danger")
                        return redirect("/ai-photoshoot")

                if lower_garment_image:
                    exten = lower_garment_image.filename.split(".")[-1]
                    if allowed_file(lower_garment_image.filename):
                        lower_garment_filename = f"{uuid.uuid4()}lowergarment.{exten}"
                        filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", lower_garment_filename)
                        lower_garment_image.save(filepath)
                        lower_garment_image_url = url_for('static',
                                                          filename=f'photoshoots_folders/{photoshoot_id}/{lower_garment_filename}',
                                                          _external=True)
                        all_images.append(lower_garment_image_url)
                    else:
                        flash("Your lower garment image not valid...", "danger")
                        return redirect("/ai-photoshoot")



            mapping_dict = {
                "id": user_id,
                "photoshoot_id": photoshoot_id,
                "upload_garment_type": garment_upload_type,
                "age_group": age_group,
                "gender": gender,
                "ethnicity": ethnicity,
                "height": height,
                "fitting": fitting,
                "width": width,
                "age": age,
                "lower_garment_type": lower_garment_type,
                "upper_garment_type": upper_garment_type,
                "selected_poses": selected_poses,
                "all_images": all_images,
                "total_credit": 0,
                "is_credit_debited": False,
                "is_completed": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            mongoOperation().insert_data_from_coll("photoshoot_data", mapping_dict)
            try:
                del mapping_dict["_id"]
            except:
                pass

            with app.app_context():
                executor.submit(generate_photoshoot_background_task, mapping_dict, photoshoot_id, upper_garment_filename, lower_garment_filename)

            flash("Photoshoot Generation started successfully...", "success")
            return redirect("/ai-photoshoot")
        else:
            return render_template("ai-photoshoot.html", login_dict=login_dict)

    except Exception as e:
        print(f"{datetime.now()}: Error in ai photoshoot route: {str(e)}")
        return redirect("/ai-photoshoot")


@app.route('/photoshoot/<photoshoot_id>')
@token_required
def photoshoot_detail(photoshoot_id):
    return render_template('details-photoshoot.html', photoshoot_id=photoshoot_id, login_dict=session.get("login_dict", {}),)


@app.route('/api/photoshoot/<photoshoot_id>')
def get_photoshoot_detail(photoshoot_id):
    try:
        user_id = session.get("login_dict", {}).get("id", "")
        photoshoot = list(mongoOperation().get_spec_data_from_coll("photoshoot_data", {'id': user_id, 'photoshoot_id': photoshoot_id}))
        photoshoot = photoshoot[0]
        if not photoshoot:
            return jsonify({
                'success': False,
                'error': 'Photoshoot not found'
            }), 404

        # Convert ObjectId to string and format data
        photoshoot['_id'] = str(photoshoot['_id'])

        # Handle different datetime formats
        if 'created_at' in photoshoot:
            if isinstance(photoshoot['created_at'], dict) and '$date' in photoshoot['created_at']:
                photoshoot['created_at'] = photoshoot['created_at']['$date']
            elif hasattr(photoshoot['created_at'], 'isoformat'):
                photoshoot['created_at'] = photoshoot['created_at'].isoformat()

        # Ensure all_images is a list
        if 'all_images' in photoshoot and not isinstance(photoshoot['all_images'], list):
            photoshoot['all_images'] = []

        # Handle selected_poses if it's not properly formatted
        if 'selected_poses' in photoshoot and isinstance(photoshoot['selected_poses'], list):
            cleaned_poses = []
            for pose in photoshoot['selected_poses']:
                if isinstance(pose, str):
                    cleaned_pose = pose.replace('[', '').replace(']', '').replace('"', '').split(',')
                    cleaned_poses.extend([p.strip() for p in cleaned_pose if p.strip()])
            photoshoot['selected_poses'] = cleaned_poses

        return jsonify({
            'success': True,
            'data': photoshoot
        })

    except Exception as e:
        print(f"Error in get_photoshoot_detail: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/photoshoots')
def get_photoshoots():
    try:
        user_id = session.get("login_dict", {}).get("id", "")
        status = request.args.get('status', 'all')
        garment_type = request.args.get('garment_type', 'all')
        gender = request.args.get('gender', 'all')
        age_group = request.args.get('age_group', 'all')

        # Build query
        query = {"id": user_id}
        if status != 'all':
            query['status'] = status
        if garment_type != 'all':
            query['upload_garment_type'] = garment_type
        if gender != 'all':
            query['gender'] = gender
        if age_group != 'all':
            query['age_group'] = age_group

        print(f"MongoDB query: {query}")  # Debug print

        # Get data from MongoDB
        db = mongoOperation().get_specific_db("stylic")
        coll = db["photoshoot_data"]
        photoshoots = list(coll.find(query).sort("_id", -1))
        # photoshoots = list(mongoOperation().get_spec_data_from_coll("photoshoot_data", query))
        print(f"Found {len(photoshoots)} photoshoots")  # Debug print

        # Convert ObjectId to string and format data
        for photoshoot in photoshoots:
            photoshoot['_id'] = str(photoshoot['_id'])

            # Handle different datetime formats
            if 'created_at' in photoshoot:
                if isinstance(photoshoot['created_at'], dict) and '$date' in photoshoot['created_at']:
                    photoshoot['created_at'] = photoshoot['created_at']['$date']
                elif hasattr(photoshoot['created_at'], 'isoformat'):
                    photoshoot['created_at'] = photoshoot['created_at'].isoformat()

            # Ensure all_images is a list
            if 'all_images' in photoshoot and not isinstance(photoshoot['all_images'], list):
                photoshoot['all_images'] = []

            # Handle selected_poses if it's not properly formatted
            if 'selected_poses' in photoshoot and isinstance(photoshoot['selected_poses'], list):
                # Clean up selected_poses format
                cleaned_poses = []
                for pose in photoshoot['selected_poses']:
                    if isinstance(pose, str):
                        # Remove brackets and quotes, split by comma
                        cleaned_pose = pose.replace('[', '').replace(']', '').replace('"', '').split(',')
                        cleaned_poses.extend([p.strip() for p in cleaned_pose if p.strip()])
                photoshoot['selected_poses'] = cleaned_poses

        return jsonify({
            'success': True,
            'data': photoshoots,
            'total': len(photoshoots)
        })

    except Exception as e:
        print(f"Error in get_photoshoots: {str(e)}")  # Debug print
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download/<photoshoot_id>')
def download_single_image(photoshoot_id):
    try:
        image_url = request.args.get('url')
        if not image_url:
            return jsonify({'error': 'Image URL required'}), 400

        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.write(response.content)
            temp_file.close()

            # Get filename from URL
            filename = os.path.basename(image_url)

            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=filename,
                mimetype='image/png'
            )
        else:
            return jsonify({'error': 'Failed to download image'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-all/<photoshoot_id>')
def download_all_images(photoshoot_id):
    try:
        user_id = session.get("login_dict", {}).get("id", "")
        print(user_id)
        photoshoot = mongoOperation().get_spec_data_from_coll("photoshoot_data", {'id': user_id, 'photoshoot_id': photoshoot_id})
        if not photoshoot:
            return jsonify({'error': 'Photoshoot not found'}), 404

        # Create temporary zip file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_zip.close()

        with zipfile.ZipFile(temp_zip.name, 'w') as zip_file:
            for i, image_url in enumerate(photoshoot[0].get('all_images', [])):
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        filename = f"image_{i + 1}_{os.path.basename(image_url)}"
                        zip_file.writestr(filename, response.content)
                except Exception as e:
                    print(f"Error downloading image {image_url}: {e}")
                    continue

        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name=f"photoshoot_{photoshoot_id}.zip",
            mimetype='application/zip'
        )

    except Exception as e:
        print(f"error coming in download all images in zip file: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/filters')
def get_filters():
    try:
        user_id = session.get("login_dict", {}).get("id", "")
        database = mongoOperation().get_specific_db("stylic")
        collection = database["photoshoot_data"]
        # Get unique values for filters
        statuses = list(collection.find({"id": user_id}).distinct('status'))
        garment_types = list(collection.find({"id": user_id}).distinct('upload_garment_type'))
        genders = list(collection.find({"id": user_id}).distinct('gender'))
        age_groups = list(collection.find({"id": user_id}).distinct('age_group'))

        return jsonify({
            'statuses': [s for s in statuses if s],  # Filter out None/empty values
            'garment_types': [g for g in garment_types if g],
            'genders': [g for g in genders if g],
            'age_groups': [a for a in age_groups if a]
        })
    except Exception as e:
        print(f"Error in get_filters: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route("/ai-video-generation", methods=["GET", "POST"])
@token_required
def ai_video_generation():
    try:
        return render_template("ai-video-generation.html", login_dict=session.get("login_dict", {}))

    except Exception as e:
        print(f"{datetime.now()}: Error in ai video generation route: {str(e)}")
        return redirect("/ai-video-generation")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    try:
        del session["login_dict"]
        flash("logout successfully...", "success")
        return redirect("/")

    except Exception as e:
        print(f"{datetime.now()}: Error in logout route: {str(e)}")
        return redirect("/logout")


@app.route("/image-upscaler", methods=["GET", "POST"])
@token_required
def image_upscaler():
    try:
        return render_template("image-upscaler.html", login_dict=session.get("login_dict", {}))

    except Exception as e:
        print(f"{datetime.now()}: Error in image upscaler route: {str(e)}")
        return redirect("/image-upscaler")


@app.route("/background-replacer", methods=["GET", "POST"])
@token_required
def background_replacer():
    try:
        return render_template("background-replacer.html", login_dict=session.get("login_dict", {}))

    except Exception as e:
        print(f"{datetime.now()}: Error in background replacer route: {str(e)}")
        return redirect("/background-replacer")


@app.route("/my-creation-history", methods=["GET", "POST"])
@token_required
def my_creation_history():
    try:
        return render_template("my-creations.html", login_dict=session.get("login_dict", {}))

    except Exception as e:
        print(f"{datetime.now()}: Error in my creation history route: {str(e)}")
        return redirect("/my-creation-history")

@app.route("/order-history", methods=["GET", "POST"])
@token_required
def order_history():
    try:
        user_id = session.get("login_dict", {}).get("id", "")
        photoshoot_data = list(mongoOperation().get_spec_data_from_coll("photoshoot_data", {"id": user_id}))
        mapping_dict = {}
        mapping_dict["total_photoshoot"]=len(photoshoot_data)
        total_photos = 0
        pending_photoshoot = 0
        for photoshoot in photoshoot_data:
            status = photoshoot["status"]
            if status=="completed":
                total_photos+=len(photoshoot["selected_poses"])
            else:
                pending_photoshoot+=1

        mapping_dict["total_photos"]=total_photos
        mapping_dict["pending_photoshoot"]=pending_photoshoot
        return render_template("order-history.html", login_dict=session.get("login_dict", {}), mapping_dict=mapping_dict)

    except Exception as e:
        print(f"{datetime.now()}: Error in dashboard route: {str(e)}")
        return redirect("/order-history")


@app.route("/credit-history", methods=["GET", "POST"])
@token_required
def credit_history():
    try:
        return render_template("credit-history.html", login_dict=session.get("login_dict", {}))

    except Exception as e:
        print(f"{datetime.now()}: Error in credit history route: {str(e)}")
        return redirect("/credit-history")


@app.errorhandler(400)
def bad_request(error):
    flash("Bad request - please check your input", "danger")
    return redirect("/dashboard")


@app.errorhandler(500)
def internal_error(error):
    flash("An internal error occurred", "danger")
    return redirect("/dashboard")


@app.route("/developer-api", methods=["GET", "POST"])
def developer_api():
    try:
        photoshoot_id = request.args.get("photoshoot_id")
        user_id = request.args.get("id")
        photoimage = request.files.get("photoimage")
        photoshoot_data = list(mongoOperation().get_spec_data_from_coll("photoshoot_data", {"id": user_id, "photoshoot_id": photoshoot_id}))
        all_images = photoshoot_data[0]["all_images"]
        total_credit = photoshoot_data[0]["total_credit"]
        is_credit_debited = photoshoot_data[0]["is_credit_debited"]
        output_filename = f"{uuid.uuid4()}_photoshoot.png"
        filepath = os.path.join(f"static/photoshoots_folders/{photoshoot_id}", output_filename)
        photoimage.save(filepath)
        upper_garment_image_url = url_for('static',
                                          filename=f'photoshoots_folders/{photoshoot_id}/{output_filename}',
                                          _external=True)
        all_images.append(upper_garment_image_url)

        if is_credit_debited:
            photoshoot_mapping = {
                "is_credit_debited": True,
                "is_completed": True,
                "all_images": all_images,
                "status": "completed"
            }
        else:
            user_data = list(mongoOperation().get_spec_data_from_coll("company_data", {"id": user_id}))

            user_credit = int(user_data[0]["credit"])
            remaining_credit = user_credit - 1
            mongoOperation().update_mongo_data("company_data", {"id": user_id}, {"credit": remaining_credit})

            photoshoot_mapping = {
                "is_credit_debited": True,
                "is_completed": True,
                "total_credit": total_credit+1,
                "all_images": all_images,
                "status": "completed"
            }

        mongoOperation().update_mongo_data("photoshoot_data", {"id": user_id, "photoshoot_id": photoshoot_id},
                                           photoshoot_mapping)

        return {"photoshoot": "complete uploaded"}

    except Exception as e:
        print(f"{datetime.now()}: Error in upload photo manual route: {str(e)}")
        return {"photoshoot": f"not complete uploaded: {e}"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8060)