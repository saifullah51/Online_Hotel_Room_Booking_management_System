from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection
from datetime import datetime

app = Flask(__name__)

# Secret key for login sessions
app.secret_key = "hotel_management_secret_key"


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():
    return render_template("index.html")


# ==================================================
# ROOMS
# ==================================================

@app.route("/rooms")
def rooms():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Room")

    rooms = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "rooms.html",
        rooms=rooms
    )


# ==================================================
# CUSTOMER REGISTRATION
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor()

        # Check whether email already exists
        cursor.execute(
            """
            SELECT customer_id
            FROM Customer
            WHERE email = %s
            """,
            (email,)
        )

        existing_customer = cursor.fetchone()

        if existing_customer:

            cursor.close()
            connection.close()

            return "Email already registered. Please use another email."

        # Insert customer
        query = """
        INSERT INTO Customer
        (
            name,
            email,
            phone,
            password
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                name,
                email,
                phone,
                password
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ==================================================
# CUSTOMER LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM Customer
        WHERE email = %s
        AND password = %s
        """

        cursor.execute(
            query,
            (
                email,
                password
            )
        )

        customer = cursor.fetchone()

        cursor.close()
        connection.close()

        if customer:

            # Store customer information
            # in the login session
            session["customer_id"] = customer["customer_id"]
            session["customer_name"] = customer["name"]

            return redirect(url_for("rooms"))

        return "Invalid email or password."

    return render_template("login.html")


# ==================================================
# BOOK ROOM
# ==================================================

@app.route("/booking/<int:room_id>", methods=["GET", "POST"])
def booking(room_id):

    # Check whether customer is logged in
    customer_id = session.get("customer_id")

    if not customer_id:

        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get selected room
    cursor.execute(
        """
        SELECT *
        FROM Room
        WHERE room_id = %s
        """,
        (room_id,)
    )

    room = cursor.fetchone()

    # Check if room exists
    if room is None:

        cursor.close()
        connection.close()

        return "Room not found."

    # ==================================================
    # PROCESS BOOKING
    # ==================================================

    if request.method == "POST":

        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        try:

            # Convert dates
            check_in_date = datetime.strptime(
                check_in,
                "%Y-%m-%d"
            )

            check_out_date = datetime.strptime(
                check_out,
                "%Y-%m-%d"
            )

        except ValueError:

            cursor.close()
            connection.close()

            return "Invalid date format."

        # Calculate number of nights
        nights = (
            check_out_date - check_in_date
        ).days

        # Check dates
        if nights <= 0:

            cursor.close()
            connection.close()

            return "Check-out date must be after check-in date."

        # ==================================================
        # CHECK ROOM AVAILABILITY FOR THE SELECTED DATES
        # ==================================================

        cursor.execute(
            """
            SELECT booking_id
            FROM Booking
            WHERE room_id = %s
            AND status = 'Confirmed'
            AND check_in < %s
            AND check_out > %s
            """,
            (
                room_id,
                check_out,
                check_in
            )
        )

        existing_booking = cursor.fetchone()

        if existing_booking:

            cursor.close()
            connection.close()

            return """
            <h2>Room Not Available</h2>
            <p>This room is already booked for the selected dates.</p>
            <a href="/rooms">Back to Rooms</a>
            """

        # Calculate total amount
        total_amount = nights * float(room["price"])

        # Insert booking
        query = """
        INSERT INTO Booking
        (
            customer_id,
            room_id,
            check_in,
            check_out,
            total_amount,
            status
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            query,
            (
                customer_id,
                room_id,
                check_in,
                check_out,
                total_amount,
                "Confirmed"
            )
        )

        connection.commit()

        # Get newly created booking ID
        booking_id = cursor.lastrowid

        cursor.close()
        connection.close()

        # Show booking success page
        return render_template(
            "booking_success.html",
            booking_id=booking_id,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_amount=total_amount
        )

    # ==================================================
    # SHOW BOOKING PAGE
    # ==================================================

    cursor.close()
    connection.close()

    return render_template(
        "booking.html",
        room=room
    )


# ==================================================
# MY BOOKINGS
# ==================================================

@app.route("/bookings")
def bookings():

    # Check login
    customer_id = session.get("customer_id")

    if not customer_id:

        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        b.booking_id,
        r.room_number,
        r.room_type,
        b.check_in,
        b.check_out,
        b.total_amount,
        b.status

    FROM Booking b

    INNER JOIN Room r
        ON b.room_id = r.room_id

    WHERE b.customer_id = %s

    ORDER BY b.booking_id DESC
    """

    cursor.execute(
        query,
        (customer_id,)
    )

    bookings = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "bookings.html",
        bookings=bookings
    )


# ==================================================
# CANCEL BOOKING
# ==================================================

@app.route("/cancel-booking/<int:booking_id>")
def cancel_booking(booking_id):

    # Check login
    customer_id = session.get("customer_id")

    if not customer_id:

        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor()

    # Only cancel the booking belonging
    # to the logged-in customer
    query = """
    UPDATE Booking
    SET status = 'Cancelled'
    WHERE booking_id = %s
    AND customer_id = %s
    AND status = 'Confirmed'
    """

    cursor.execute(
        query,
        (
            booking_id,
            customer_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("bookings"))

@app.route("/debug")
def debug():

    return f"""
    <h2>Session Debug</h2>

    <p>Customer ID: {session.get("customer_id")}</p>

    <p>Customer Name: {session.get("customer_name")}</p>

    <p>
        <a href="/bookings">My Bookings</a>
    </p>
    """
# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    # Clear login session
    session.clear()

    return redirect(url_for("home"))


# ==================================================
# START FLASK SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5005,
        debug=False
    )