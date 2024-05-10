import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def display_booking_analysis():
    # Load the hotelreservation dataset into a pandas DataFrame
    df = pd.read_csv('hotelsreservation.csv')  # Replace 'hotelreservation.csv' with the actual filename

    # Extract the booking_status column
    booking_status = df['booking_status']

    # Count the occurrences of each booking status
    status_counts = booking_status.value_counts()

    # Calculate the total loss due to cancellations (assuming avg room price is $200)
    cancellation_loss = status_counts.get('Canceled', 0) * 200

    # Format the total loss with commas
    formatted_loss = "{:,}".format(cancellation_loss)

    # Create a bar plot to visualize the booking statuses
    fig, ax = plt.subplots(figsize=(8, 6))
    status_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Booking Status Analysis')
    ax.set_xlabel('Booking Status')
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent clipping of labels

    # Display the plot in the Streamlit app
    st.pyplot(fig)

    # Display the total loss due to cancellations with formatting
    st.markdown(
        f"<span style='font-size:40px; color:red; font-style:italic;'>Total loss due to last minute cancellations till date: ${formatted_loss}</span>",
        unsafe_allow_html=True
    )

# Example usage:
# display_booking_analysis()


# Example usage:
# display_booking_analysis()


def display_booking_details():
    st.image('checkin1.jpeg', caption="Providing you the best stay")
    st.title("Room allotment")
    try:
        # Connect to MySQL server and database
        cnx = mysql.connector.connect(user='root', password='Mohit9944.',
                                      host='localhost', port=3306,
                                      database='reservepro')
        
        # Create a cursor
        cursor = cnx.cursor()

        # Execute the SQL query
        cursor.execute("""
                        SELECT r.booking_id,c.customer_id, c.name, r.roomnumber, ch.arrival_date, ch.checkoutdate 
                         FROM reservations r 
                        JOIN customers c ON r.customer_id = c.customer_id 
                        JOIN checkins ch ON ch.booking_id = r.booking_id 
                        ORDER BY ch.arrival_date DESC;
                    """)


        # Fetch all the records
        results = cursor.fetchall()

        # Convert the results into a DataFrame
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

        # Display the DataFrame in Streamlit
        st.write(df)

    except mysql.connector.Error as err:
        st.error(f"MySQL error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
def display_blacklisted_customers():
    st.title("Blacklisted Customers who have cancelled more than 5 times")
    try:
        # Connect to MySQL server and database
        cnx = mysql.connector.connect(user='root', password='Mohit9944.',
                                      host='localhost', port=3306,
                                      database='reservepro')
        
        # Create a cursor
        cursor = cnx.cursor()

        # Execute the SQL query
        cursor.execute('''select customer_id, name ,no_of_previous_cancellations
                        from customers
                    where no_of_previous_cancellations>5;''')

        # Fetch all the records
        results = cursor.fetchall()

        # Convert the results into a DataFrame
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

        # Display the DataFrame in Streamlit
        st.write(df)

    except mysql.connector.Error as err:
        st.error(f"MySQL error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
import streamlit as st
import mysql.connector


def display_change_room_number():
    st.title("Enter the booking ID and updated room number")
    # Add unique keys for each text_input widget
    bid = st.text_input("Booking ID", key="booking_id")
    updated_room_number = st.text_input("New room number", key="new_room_number")
    
    if st.button('Update Room Number') and bid and updated_room_number:
        try:
            # Connect to MySQL server and database
            cnx = mysql.connector.connect(user='root', password='Mohit9944.',
                                          host='localhost', database='reservepro')
            # Create a cursor
            cursor = cnx.cursor()

            # Formulate the update statement
            update_stmt = (
                "UPDATE reservations "
                "SET roomnumber = %s "
                "WHERE booking_id = %s;"
            )
            data = (updated_room_number, bid)

            # Execute the SQL query
            cursor.execute(update_stmt, data)
            
            # Commit the changes
            cnx.commit()
            
            st.success(f"Room number updated to {updated_room_number} for booking ID {bid}.")
        
        except mysql.connector.Error as err:
            st.error(f"MySQL error: {err}")
        
        finally:
            # Close the cursor and connection
            cursor.close()
            cnx.close()






def display_meal_plans():
    st.image('mp.jpeg')
    st.title("Meal Plan Allotment")
    try:
        # Connect to MySQL server and database
        cnx = mysql.connector.connect(user='root', password='Mohit9944.',
                                      host='localhost', port=3306,
                                      database='reservepro')
        
        # Create a cursor
        cursor = cnx.cursor()

        # Execute the SQL query
        cursor.execute('''
    SELECT r.booking_id, c.name, r.roomnumber, r1.mealtype
    FROM reservations r
    JOIN customers c ON r.customer_id = c.customer_id
    JOIN restaurants r1 ON r1.booking_id = r.booking_id
''')

        # Fetch all the records
        results = cursor.fetchall()

        # Convert the results into a DataFrame
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

        # Display the DataFrame in Streamlit using Plotly's table
        
        fig = go.Figure(data=[go.Table(header=dict(values=list(df.columns)),
                                       cells=dict(values=[df[col] for col in df.columns]))])
        st.plotly_chart(fig)

    except mysql.connector.Error as err:
        st.error(f"MySQL error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        cnx.close()

def display_parking_space():
    
    st.image('valetparking.jpeg')
    st.title("For the Valets")
    try:
        # Connect to MySQL server and database
        cnx = mysql.connector.connect(user='root', password='Mohit9944.',
                                      host='localhost', port=3306,
                                      database='reservepro')
        
        # Create a cursor
        cursor = cnx.cursor()

        # Execute the SQL query
        cursor.execute(''' select  r.booking_id, c.name,r.roomnumber,p.carparking,ch.arrival_date,ch.checkoutdate
                            from reservations r join customers c on r.customer_id=c.customer_id join ParkingSpace p join Checkins ch on p.booking_id=ch.booking_id
                            on p.booking_id=r.booking_id
                            where p.carparking=1;''')

        # Fetch all the records
        results = cursor.fetchall()

        # Convert the results into a DataFrame
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

        # Display the DataFrame in Streamlit
        st.write(df)

    except mysql.connector.Error as err:
        st.error(f"MySQL error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
import uuid
def main():
    # Check if user has logged in
    if "logged_in" not in st.session_state:
        # Display the background image
        st.image('img.jpeg', caption="Providing you the best stay")

        # Header and login form
        st.header(":green[_ReservePro: Streamlining Hotel Management_]", divider='rainbow')
        st.title('Login with your credentials')

        # Input fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Login button
        if st.button("Login"):
            if username == "admin" and password == "password":
                st.success("Logged in as {}".format(username))
                st.session_state.logged_in = True
            else:
                st.error("Invalid username or password")
    else:
        # Create left sidebar
        st.sidebar.title("Navigation Pane")

        # Display buttons for different options
        selected_option = st.sidebar.radio("Go to", ["Booking Details", "Meal Plans", "Parking Space", "Enter Booking","Booking Analysis","Blacklisted Customers","Change Room Number","Delete Bookings"])

        # Based on the selected option, display relevant content
        if selected_option == "Booking Details":
            display_booking_details()
        elif selected_option == "Meal Plans":
            display_meal_plans()
        elif selected_option == "Parking Space":
            display_parking_space()
        elif selected_option =="Change Room Number":
            display_change_room_number()
        elif selected_option == "Booking Analysis":
            display_booking_analysis()
        elif selected_option=="Blacklisted Customers":
            display_blacklisted_customers()
        elif selected_option=="Delete Bookings":
            st.subheader("Click on submit button to delete the reservations made by the customer")
            customer_id = st.text_input("Customer ID")
            if st.button("Submit"):
                display_delete_bookings(customer_id)

        elif selected_option == "Enter Booking":
            st.subheader("Enter Booking Details")
            customer_name = st.text_input("Customer Name")
            date_of_arrival = st.date_input("Arrival Date")
            checkout_date=st.date_input("Checkout Date")
            no_of_adults = st.text_input("Number of Adults")
            no_of_children = st.text_input("Number of Children")
            
            meal_plan_options = ["Meal Plan 1", "Meal Plan 2", "Not Selected"]
            meal_plan = st.selectbox("Choose a Meal Plan", meal_plan_options)
            parking_space_options = [0,1]
            pspace = st.selectbox("Do you require parking space", parking_space_options)
            if st.button("Submit"):
                enter_booking_details(customer_name, date_of_arrival,checkout_date,no_of_adults,no_of_children,meal_plan,pspace )

def enter_booking_details(customer_name, date_of_arrival,checkout_date,no_of_adults,no_of_children,meal_plan,pspace ):
    try:
        
        cnx = mysql.connector.connect(user='root', password='Mohit9944.',
                                      host='localhost', port=3306,
                                      database='reservepro')

       
        cursor = cnx.cursor()

       
        cursor.execute("INSERT INTO customers (name,repeated_guest,no_of_previous_cancellations,no_of_previous_bookings_not_canceled) VALUES (%s, %s, %s,%s)",
                       (customer_name,0,0,0))
        customer_id = cursor.lastrowid

        
        cnx.commit()
        booking_id = "INN"+str(customer_id+1)
        query = """INSERT INTO reservations 
                    (booking_id, customer_id,roomnumber,employee_id, no_of_adults, no_of_children,no_of_weekend_nights,no_of_week_nights) 
                   VALUES 
                    (%s, %s, %s, %s, %s, %s,%s,%s)"""
        cursor.execute(query, (booking_id, customer_id,600,1001,no_of_adults, no_of_children,0,0))

        
        checkins_query = """INSERT INTO Checkins 
                            (booking_id,lead_time, arrival_date, checkoutdate) 
                            VALUES 
                            (%s, %s, %s,%s)"""
        cursor.execute(checkins_query, (booking_id,0, date_of_arrival, checkout_date))

        mealplans_query = """INSERT INTO restaurants 
                            (booking_id,mealtype) 
                            VALUES 
                            (%s, %s)"""
        cursor.execute(mealplans_query, (booking_id,meal_plan))

        pspace_query = """INSERT INTO ParkingSpace
                            (booking_id,customername,carparking) 
                            VALUES 
                            (%s, %s,%s)"""
        cursor.execute(pspace_query, (booking_id,customer_name,pspace))


        st.success("Booking details successfully added!")
        
        cnx.commit()


    except mysql.connector.Error as err:
        st.error(f"MySQL error: {err}")

    finally:
        cursor.close()
        cnx.close()




def display_delete_bookings(customer_id):
    try:
        
        cnx = mysql.connector.connect(user='root', password='Mohit9944.',
                                      host='localhost', port=3306,
                                      database='reservepro')

      
        cursor = cnx.cursor()
        delete_query = "DELETE FROM customers WHERE customer_id = %s;"
        cursor.execute(delete_query, (customer_id,))
        cnx.commit()  
        st.success(f"{customer_id} has been deleted and the reservations have been removed and an email has been sent with the reasons")
        

    except mysql.connector.Error as err:
        st.error(f"MySQL error: {err}")

    finally:
        cursor.close()
        cnx.close()

    
if __name__ == "__main__":
    main()