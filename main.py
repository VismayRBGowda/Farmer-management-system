from flask import Flask, render_template, request, session, redirect, url_for, flash,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_manager, LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import io
import xlwt
from sqlalchemy import text

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='vvy'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'



app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost:4136/farm'

db=SQLAlchemy(app)




class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    role = db.Column(db.String(20), nullable=False, default='user')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))



class trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    farmer_id=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))



class farmers(db.Model):
    __tablename__ = 'farmers'
    farmer_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    farming_experience = db.Column(db.Integer, nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    town_village = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    


class LandDetails(db.Model):
    __tablename__ = 'land_details'
    land_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    soil_type = db.Column(db.String(255), nullable=False)
    irrigation_system = db.Column(db.String(255), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.farmer_id'), nullable=False)
    farmer = db.relationship('farmers', backref='land_details')

class Crops(db.Model):
    __tablename__ = 'crops'
    crop_id = db.Column(db.Integer, primary_key=True)
    crop_type = db.Column(db.String(255), nullable=False)
    planting_date = db.Column(db.Date, nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    expected_yield = db.Column(db.Integer, nullable=False)
    actual_yield = db.Column(db.Integer, nullable=False)
    fertilizers_used = db.Column(db.String(255), nullable=False)
    land_id = db.Column(db.Integer, db.ForeignKey('land_details.land_id'))
    
    # Define the relationship with the land_details table
    land = db.relationship('LandDetails', backref=db.backref('crops', lazy=True))
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.farmer_id'), nullable=False)
    farmer = db.relationship('farmers')

class addagroproducts(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)





class farm_equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.farmer_id'), nullable=False)
    farmer = db.relationship('farmers')


class farm_animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    breed = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    health_status = db.Column(db.String(255), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.farmer_id'), nullable=False)
    farmer = db.relationship('farmers')



class labour(db.Model):
    labour_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    town_village = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)


class labour_hired(db.Model):
    hiring_id= db.Column(db.Integer, primary_key=True)
    hiring_date = db.Column(db.Date, nullable=False)
    no_of_days_worked = db.Column(db.Integer, nullable=False)
    labour_cost = db.Column(db.DECIMAL(10, 2), nullable=False)
    labour_id = db.Column(db.Integer, db.ForeignKey('labour.labour_id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.farmer_id'), nullable=False)
    farmer = db.relationship('farmers')


class MyStoredProcedures:
    @staticmethod
    def create_select_farmers_by_state_procedure():
        procedure_sql = """
        DELIMITER //
        CREATE PROCEDURE SelectFarmersByState(IN state_param VARCHAR(255))
        BEGIN
            SELECT * FROM farmers WHERE state = state_param;
        END //
        DELIMITER ;
        """
        db.session.execute(procedure_sql)
        db.session.commit()


    

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/statewisefarmers', methods=['GET', 'POST'])
def select_farmers_by_state():
    if request.method == 'POST':
        state_param = request.form.get('state')  # Get the state parameter from the form

        # Use text function to declare the SQL expression
        sql_expression = text("CALL SelectFarmersByState(:state_param)")

        # Call the stored procedure
        result = db.session.execute(sql_expression, {"state_param": state_param})

        # Fetch the results
        farmers_by_state = result.fetchall()

        return render_template('farmers_by_state.html', farmers=farmers_by_state)

    return render_template('farmers_by_state.html')


@app.route('/crops', methods=['POST', 'GET'])
@login_required
def addcrop():
     

     if request.method == "POST":
  


            # Your other form data retrieval logic
            crop_type = request.form.get('type')
            land_id_value=request.form.get('land_id')
            planting_date = request.form.get('planting_date')
            harvest_date = request.form.get('harvest_date')
            expected_yield = request.form.get('expected_yield')
            actual_yield = request.form.get('actual_yield')
            fertilizers_used = request.form.get('fertilizers_used')

            # Create an instance of Crops with the retrieved values
            crop = Crops(
                land_id=land_id_value,
                crop_type=crop_type,
                planting_date=planting_date,
                harvest_date=harvest_date,
                expected_yield=expected_yield,
                actual_yield=actual_yield,
                fertilizers_used=fertilizers_used,
                farmer_id=current_user.id
            )

            # Add the crop to the session and commit the changes
            db.session.add(crop)
            db.session.commit()

            flash("Crop Added", "success")

     crop_entry = Crops.query.filter_by(farmer_id=current_user.id).all()


     return render_template('crops.html', query=crop_entry)


@app.route('/farmequipments', methods=['POST', 'GET'])
@login_required
def addfarmequipment():
   

    if request.method == "POST":
        equipment_type = request.form.get('type')
        model = request.form.get('model')
        price = request.form.get('price')
        purchase_date = request.form.get('purchase_date')

        farm_equipments = farm_equipment(
            type=equipment_type,
            model=model,
            price=price,
            purchase_date=purchase_date,
            farmer_id=current_user.id
        )

        db.session.add(farm_equipments)
        db.session.commit()

        flash("Farm Equipment Added", "success")

    farm_equipments_entry = farm_equipment.query.filter_by(farmer_id=current_user.id).all()
    


    return render_template('farm_equipments.html', query=farm_equipments_entry)


@app.route('/labour', methods=['POST', 'GET'])
@login_required
def addlabour():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gender = request.form.get('gender')
        phone_no = request.form.get('phone_no')
        state = request.form.get('state')
        district = request.form.get('district')
        town_village = request.form.get('town_village')
        pincode = request.form.get('pincode')

        # Create a new labor instance
        labor_entry = labour(
            fname=fname,
            lname=lname,
            gender=gender,
            phone_no=phone_no,
            state=state,
            district=district,
            town_village=town_village,
            pincode=pincode,
        )

        # Add the labor entry to the database
        db.session.add(labor_entry)
        db.session.commit()

       

        flash("Labour Added", "success")

    # Fetch the list of labor entries for display
    labor_entries = labour.query.all()

    return render_template('labour.html', query=labor_entries)


@app.route('/labourhiring', methods=['POST', 'GET'])
@login_required
def hirelabour():
    if request.method == "POST":
        # Assuming you have the necessary form data to create a labour_hired entry
        labour_hirings = labour_hired(
            labour_id=request.form.get('labour_id'),
            hiring_date=request.form.get('hiring_date'),
            no_of_days_worked=request.form.get('no_of_days_worked'),
            labour_cost=request.form.get('labour_cost'),
            farmer_id=current_user.id  # Assuming you want to associate it with the current user
        )

        db.session.add(labour_hirings)
        db.session.commit()

        flash("Labour Hired", "success")

    # Fetch the list of labour_hired entries for display
    labour_hired_entries = labour_hired.query.filter_by(farmer_id=current_user.id).all()

    return render_template('labour_hiring.html', query=labour_hired_entries)


@app.route('/farmanimals', methods=['POST', 'GET'])
@login_required
def addfarmanimal():
    
    if request.method == "POST":
        name = request.form.get('name')
        breed = request.form.get('breed')
        gender = request.form.get('gender')
        age = request.form.get('age')
        health_status = request.form.get('health_status')

        farm_animal = farm_animals(
            name=name,
            breed=breed,
            gender=gender,
            age=age,
            health_status=health_status,
            farmer_id=current_user.id
           
        )

        db.session.add(farm_animal)
        db.session.commit()
        
        farm_animal = farm_animals.query.all()

        flash("Farm Animal Added", "success")
    farm_animals_entry = farm_animals.query.filter_by(farmer_id=current_user.id).all()
    return render_template('farm_animals.html',query=farm_animals_entry)  

@app.route('/agroproducts')
def agroproducts():
    # query=db.engine.execute(f"SELECT * FROM `addagroproducts`") 
    query=addagroproducts.query.all()
    return render_template('agroproducts.html',query=query)

@app.route("/addagroproducts/<int:farmer_id>", methods=['POST', 'GET'])
@login_required
def addagroproduct(farmer_id):
    farmer = farmers.query.get(farmer_id)

        # Check if the logged-in user has the correct permission
    if current_user.id != farmer.farmer_id:
        flash("You don't have permission to edit this entry", "danger")
        return redirect('/farmerdetails')

    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        productname = request.form.get('productname')
        productdesc = request.form.get('productdesc')
        price = request.form.get('price')

        # Create an instance of addagroproducts
        product = addagroproducts(
            username=username,
            email=email,
            productname=productname,
            productdesc=productdesc,
            price=price,
        )

        # Add the product to the database
        db.session.add(product)
        db.session.commit()

        flash("Product Added", "info")
        return redirect(url_for('agroproducts'))

    return render_template('addagroproducts.html', farmer=farmer)


@app.route('/triggers')
@login_required
def triggers():
    # query=db.engine.execute(f"SELECT * FROM `trig`") 
    query=trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/farmerdetails')
@login_required
def farmerdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=farmers.query.all()
    return render_template('farmerdetails.html',query=query)

@app.route('/landdetails')
@login_required
def land_details():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=LandDetails.query.filter_by(farmer_id=current_user.id).all()
    return render_template('land_details.html',query=query)

@app.route('/labour')
@login_required
def labourdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=labour.query.all()
    return render_template('labour.html',query=query)

@app.route('/crops')
@login_required
def cropdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=crops.query.filter_by(farmer_id=current_user.id).all()
    return render_template('crops.html',query=query)

@app.route('/farmequipments')
@login_required
def farmequipmentsdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=farm_equipment.query.filter_by(farmer_id=current_user.id).all()
    return render_template('farm_equipments.html',query=query)

@app.route('/farmanimals')
@login_required
def farmanimalsdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=farm_animals.query.filter_by(farmer_id=current_user.id).all()
    return render_template('farm_animals.html',query=query)


@app.route('/labourhiring')
@login_required
def hiredlabourdetails():

    query=labour_hired.query.filter_by(farmer_id=current_user.id).all()
    return render_template('labour_hiring.html',query=query)





@app.route("/delete/<string:farmer_id>",methods=['POST','GET'])
@login_required
def delete(farmer_id):
    # db.engine.execute(f"DELETE FROM `register` WHERE `register`.`rid`={rid}")
    farmer=farmers.query.filter_by(farmer_id=farmer_id).first()
# Check if the logged-in user has the correct permission
    if current_user.id != farmer.farmer_id and current_user.role != 'admin':
        flash("You don't have permission to edit this entry", "danger")
        return redirect('/farmerdetails')

    db.session.delete(farmer)
    db.session.commit()
    flash("Slot Deleted Successful","warning")
    return redirect('/farmerdetails')

@app.route("/editfarmer/<int:farmer_id>", methods=['POST', 'GET'])
@login_required
def edit_farmer(farmer_id):
    farmer = farmers.query.get(farmer_id)

    # Check if the logged-in user has the correct permission
 # Check if the logged-in user has the correct permission
    if current_user.id != farmer.farmer_id and current_user.role != 'admin':
        flash("You don't have permission to edit this entry", "danger")
        return redirect('/farmerdetails')
    if request.method == "POST":
        farmername = request.form.get('farmername')
        lname = request.form.get('lname')
        dob = request.form.get('dob')
        farming_experience = request.form.get('farming_experience')
        phonenumber = request.form.get('phonenumber')
        state = request.form.get('state')
        district = request.form.get('district')
        town_village = request.form.get('town_village')
        pincode = request.form.get('pincode')
        

        farmer = farmers.query.get(farmer_id)
        farmer.fname = farmername
        farmer.lname = lname
        farmer.dob = dob
        farmer.farming_experience = farming_experience
        farmer.phone_no = phonenumber
        farmer.state = state
        farmer.district = district
        farmer.town_village = town_village
        farmer.pincode = pincode
        

        db.session.commit()
        flash("Farmer details updated successfully", "success")
        return redirect('/farmerdetails')

    farmer = farmers.query.get(farmer_id)
    return render_template('editfarmer.html', farmer=farmer)



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)
        if User.query.count() == 0:
            role = 'admin'
        else:
            role = 'user'
        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        newuser=User(username=username,email=email,password=encpassword,role=role)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            session['current_role'] = user.role  # Store the user's role in the session
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","warning")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('current_role', None)  # Remove the user's role from the session
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/farmerRegister', methods=['POST', 'GET'])
@login_required
def farmer_Register():
    if request.method == "POST":
        farmername = request.form.get('fname')
        lname = request.form.get('lname') 
        dob = request.form.get('dob')
        farming_experience = request.form.get('farming_experience')
        phonenumber = request.form.get('phone_no')
        state = request.form.get('state')
        district = request.form.get('district')
        town_village = request.form.get('town_village')
        pincode = request.form.get('pincode')

        # Create a new instance of the Farmers class
        new_farmer = farmers(
            fname=farmername,
            lname=lname,
            dob=dob,
            farming_experience=farming_experience,
            phone_no=phonenumber,
            state=state,
            district=district,
            town_village=town_village,
            pincode=pincode
        )

        # Add the new farmer to the database
        db.session.add(new_farmer)
        db.session.commit()

        # Set the farmer ID in the session
        session['current_farmer_id'] = new_farmer.farmer_id

        flash("Farmer registered successfully", "success")

        # Redirect to the same route to display the form again
        return redirect(url_for('farmer_Register'))

    # Retrieve the current farmer ID from the session
    autofill_farmer_id = session.get('current_farmer_id', '')

    return render_template('farmer.html', autofill_farmer_id=autofill_farmer_id)

    
@app.route('/landdetails', methods=['POST', 'GET'])
@login_required
def landdetails():
    if request.method == "POST":

        size = request.form.get('size')
        location = request.form.get('location')
        soil_type = request.form.get('soil_type')
        irrigation_system = request.form.get('irrigation_system')

        
               # Get the current farmer ID from the session
        current_farmer_id = session.get('current_farmer_id')

        # Delete existing land details for the current farmer ID
        LandDetails.query.filter_by(farmer_id=current_farmer_id).delete()

        land_details_entry = LandDetails(
            farmer_id=current_user.id,
            size=size,
            location=location,
            soil_type=soil_type,
            irrigation_system=irrigation_system,
        )
        db.session.add(land_details_entry)
        db.session.commit()

        flash("Land Details Added", "success")

    land_entry = LandDetails.query.all()
    return render_template('land_details.html',query=land_entry)  

@app.route('/report')
def download_report():
    # Fetch data from the database
    data = db.session.query(
        farmers.fname, farmers.lname, farmers.dob, farmers.farming_experience,
        farmers.phone_no, farmers.state, farmers.district, farmers.town_village,
        farmers.pincode, LandDetails.size, Crops.crop_type, Crops.planting_date,
        Crops.harvest_date, Crops.expected_yield, Crops.actual_yield, Crops.fertilizers_used
    ).join(LandDetails, farmers.farmer_id == LandDetails.farmer_id, isouter=True)\
     .join(Crops, LandDetails.land_id == Crops.land_id, isouter=True).all()

    # Output in bytes
    output = io.BytesIO()
    # Create Workbook object
    workbook = xlwt.Workbook()
    # Add a sheet
    sh = workbook.add_sheet('Farm Report')

    # Add headers
    headers = ['First Name', 'Last Name', 'DOB', 'Farming Experience', 'Phone Number', 'State', 'District',
               'Town/Village', 'Pincode', 'Land Size', 'Crop Type', 'Planting Date', 'Harvest Date',
               'Expected Yield', 'Actual Yield', 'Fertilizers Used']

    for col_num, header in enumerate(headers):
        sh.write(0, col_num, header)

    # Add data to the sheet
    for row_num, row_data in enumerate(data, start=1):
        for col_num, value in enumerate(row_data):
            sh.write(row_num, col_num, str(value))

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=farm_report.xls"})






@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    



