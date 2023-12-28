from flask import Blueprint, render_template, jsonify, request, Flask
import pandas as pd
import psycopg2

# Blueprint Initialization with correct template_folder
chart_appbp = Blueprint('chart_appbp', __name__, template_folder='templates')

# Replace these parameters with your PostgreSQL database credentials
DB_HOST = '192.168.29.164'
DB_PORT = '5432'
DB_NAME = 'mydb'
DB_USER = 'test'
DB_PASSWORD = 'test123'

# Function to connect to the database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None

# Routing function for the index page
@chart_appbp.route("/")
def chart_index():
    # Connect to the database
    connection = connect_to_db()

    if connection:
        try:
            # Query instrument identifiers from the database
            query = "SELECT DISTINCT instrumentidentifier FROM table1_data union SELECT DISTINCT instrumentidentifier FROM table1_data1 order by instrumentidentifier ASC "
            with connection, connection.cursor() as cursor:
                cursor.execute(query)
                instrument_identifiers = [row[0] for row in cursor.fetchall()]

            # Render the template with instrument identifiers
            return render_template('chart.html', instrument_identifiers=instrument_identifiers)
        except Exception as e:
            print(f"Error: Unable to execute the query. {e}")
            return jsonify({"error": f"Unable to execute the query. {e}"})
        finally:
            # Connection is closed automatically due to the use of the 'with' statement
            pass
    else:
        return jsonify({"error": "Unable to connect to the database."})

@chart_appbp.route('/')
def test():
    return "test"
@chart_appbp.route('/get_data')
def get_data():
    # Connect to the database
    connection = connect_to_db()

    if connection:
        try:
            # Get the selected symbol from the request parameters
            selected_symbol = request.args.get('symbol')

            # Query data from the database
            #query = "SELECT TO_CHAR(lasttradetime AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.MS') || 'Z' AS lasttradetime,open,high,low,close FROM bigtable where instrumentidentifier='BANKNIFTY01JUN2344600CE'"
            #query = "select lasttradetime as date,open,high,low,close, tradedqty as rd,open as redline from indices_futures_d where instrumentidentifier='FUTIDX_MIDCPNIFTY_30OCT2023_XX_0' and lasttradetime between '2023-10-03 09:15:00+00' and '2023-10-03 15:30:00+00'"
            #query = "SELECT DISTINCT to_timestamp(updated / 1000000000 ) AS date,min_o AS OPEN,min_h AS HIGH,min_l AS LOW,min_c AS CLOSE FROM crypto where ticker = 'X:BTCUSD' AND to_timestamp(updated/1000000000)::date = current_date"
            #query = f"select lasttradetime as date, open, high, low, close, tradedqty as rd from indices_futures_d where instrumentidentifier='{selected_symbol}' union select lasttradetime as date, open, high, low, close, tradedqty as rd from indices_options_d where instrumentidentifier='{selected_symbol}' union select lasttradetime as date, open, high, low, close, tradedqty as rd from currency_futures_d where instrumentidentifier='{selected_symbol}' union select instrumentidentifier,lasttradetime, b1 as redline1,b2 as redline2 from options union select instrumentidentifier,lasttradetime, b1 as redline1,b2 as redline2 from futures union select instrumentidentifier,lasttradetime, b1 as redline1,b2 as redline2 from currency_futures1"
            #query = "select lasttradetime as date, open, high, low, close,tradedqty as  rd from indices_futures_d where instrumentidentifier='FUTIDX_MIDCPNIFTY_30OCT2023_XX_0' and lasttradetimebetween '2023-10-03 09:15:00+00' and '2023-10-03 15:30:00+00'"


            query = f"select lasttradetime as date, open, high, low, close, tradedqty from table1_data where instrumentidentifier='{selected_symbol}' union select lasttradetime as date, open, high, low, close, tradedqty from table1_data1 where instrumentidentifier='{selected_symbol}'"

            #redline_query = f"select lasttradetime as date,level1 ,level2 ,level3,level4,level5,level6,level7,level8,level9,level10  from table1 where instrumentidentifier='{selected_symbol}'"
            redline_query = f" select lasttradetime as date,level1,level2,level3,level4,level5,level6,level7,level8,level9,level10,null as level11,null as level12,null as level13,null as level14,null as level15,null as level16,null as level17,null as level18,null as level19,null as level20,null as level21,null as level22  from table1 where instrumentidentifier='{selected_symbol}'  union select lasttradetime as date,level1,level2,level3,level4,level5,level6,level7,level8,level9,level10,level11,level12,level13,level14,level15,level16,level17,level18,level19,level20,level21,level22 from table2 where instrumentidentifier='{selected_symbol}'"

            #query = f"select date, open, high, low, close, rd from bigtablecopy where instrumentidentifier='{selected_symbol}' and date between '2023-06-01 09:15:00+00' and '2023-06-01 15:30:00+00'"
            with connection, connection.cursor() as cursor:
                cursor.execute(query)
                data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

                cursor.execute(redline_query)
                redline_data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])


            # Combine the main data and redline data
            data['level1'] = redline_data['level1']
            data['level2'] = redline_data['level2'] 
            data['level3'] = redline_data['level3'] 
            data['level4'] = redline_data['level4']
            data['level5'] = redline_data['level5'] 
            data['level6'] = redline_data['level6'] 
            data['level7'] = redline_data['level7']
            data['level8'] = redline_data['level8'] 
            data['level9'] = redline_data['level9'] 
            data['level10'] = redline_data['level10']
            data['level11'] = redline_data['level11']
            data['level12'] = redline_data['level12']
            data['level13'] = redline_data['level13']
            data['level14'] = redline_data['level14']
            data['level15'] = redline_data['level15']
            data['level16'] = redline_data['level16']
            data['level17'] = redline_data['level17']
            data['level18'] = redline_data['level18']
            data['level19'] = redline_data['level19']
            data['level20'] = redline_data['level20']
            data['level21'] = redline_data['level21']
            data['level22'] = redline_data['level22']

        

            # Replace NaN values with None in the DataFrame
            data = data.where(pd.notna(data), None)

            # Convert the combined DataFrame to JSON
            data_json = data.to_dict(orient='records')

            # Return the combined data as JSON
            return jsonify(data_json)

        except Exception as e:
            print(f"Error: Unable to execute the query. {e}")
        finally:
            # Connection is closed automatically due to the use of the 'with' statement
            pass
    else:
        return jsonify({"error": "Unable to connect to the database."})

# Create Flask app and register the blueprint
app = Flask(__name__)
app.register_blueprint(chart_appbp)

if __name__ == '__main__':
    app.run(debug=True)
