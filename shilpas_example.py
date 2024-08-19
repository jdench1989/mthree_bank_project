# @app.route('/customers')
# def get_customers():
#     conn, cursor = database_connection()  # Establish database connection
#     sql_query = "SELECT * FROM customers"  # Base SQL query
#     filters = []
#     values = []
#     # Check for query parameters
#     customer_id = request.args.get('customer_id')
#     first_name = request.args.get('first_name')
#     last_name = request.args.get('last_name')
#     email = request.args.get('email')
#     # Add filters based on the provided query parameters
#     if customer_id:
#         filters.append("customer_id = %s")
#         values.append(customer_id)
#     if first_name:
#         filters.append("first_name LIKE %s")
#         values.append(f"%{first_name}%")
#     if last_name:
#         filters.append("last_name LIKE %s")
#         values.append(f"%{last_name}%")
#     if email:
#         filters.append("email LIKE %s")
#         values.append(f"%{email}%")
#     # Add filters to SQL query if there are any
#     if filters:
#         sql_query += " WHERE " + " AND ".join(filters)
#     cursor.execute(sql_query, values)  # Execute SQL query
#     res = cursor.fetchall()  # Extract results
#     # Get column names from the cursor
#     column_names = [desc[0] for desc in cursor.description]
#     cursor.close()
#     conn.close()
#     # Format results as a table
#     table = tabulate(res, headers=column_names, tablefmt="html")
#     # print(table)  # Print the table in the console
#     # return jsonify(res), 200
#     html_content = f"""
#     <html>
#     <head>
#     <title>Customer Data</title>
#     <style>
#         table {{
#             width: 100%;
#             border-collapse: collapse;
#         }}
#         table, th, td {{
#             border: 1px solid black;
#         }}
#         th {{
#             background-color: #4CAF50;
#             color: white;
#         }}
#         tr:nth-child(even) {{
#             background-color: #f2f2f2;
#         }}
#         tr:nth-child(odd) {{
#             background-color: #ffffff;
#         }}
#         td {{
#             padding: 8px;
#             text-align: left;
#         }}
#     </style>
#     </head>
#     <body>
#     <h1>Customer Data</h1>
#             {table}
#     </body>
#     </html>
#         """
#     print(table)
#     return render_template_string(html_content)