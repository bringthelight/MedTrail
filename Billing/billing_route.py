from flask import Blueprint, render_template, request, jsonify, flash
from flask_mysqldb import MySQL
from datetime import datetime

billing = Blueprint('billing', __name__)
mysql = MySQL()

@billing.route('/generate_bill', methods=['GET'])
def generate_bill():
    """Route to display billing form and fetch medicine data"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            id,
            ratelist_name,
            amount,
            COALESCE(discount, 0) as discount
        FROM pharmacy_ratelist
        ORDER BY ratelist_name ASC
    """)
    med_names = cur.fetchall()
    cur.close()
    return render_template('billing.html', med_names = med_names)


@billing.route('/api/get_medicine_details/<int:medicine_id>', methods=['GET'])
def get_medicine_details(medicine_id):
    """API endpoint to get medicine price, discount and available quantity"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT 
                id,
                ratelist_name,
                amount,
                COALESCE(discount, 0) as discount,
                pharmacy_medicine_id
            FROM pharmacy_ratelist
            WHERE id = %s AND is_active = 1
        """, (medicine_id,))
        
        result = cur.fetchone()
        if result and result['pharmacy_medicine_id']:
            # Get the available stock quantity
            cur.execute("""
                SELECT SUM(COALESCE(quantity, 0)) as available_quantity
                FROM pharmacy_stock
                WHERE pharmacy_medicine_id = %s
            """, (result['pharmacy_medicine_id'],))
            
            stock_result = cur.fetchone()
            available_quantity = int(stock_result['available_quantity']) if stock_result and stock_result['available_quantity'] else 0
            
            response_data = {
                'success': True,
                'data': {
                    'id': result['id'],
                    'name': result['ratelist_name'],
                    'amount': float(result['amount']),
                    'discount': float(result['discount']),
                    'available_quantity': available_quantity,
                    'stock_warning': f'Available stock: {available_quantity} units'
                }
            }
            
            # Add warning if stock is low (less than 10 units)
            if available_quantity < 10:
                response_data['data']['stock_warning'] = f'Warning: Low stock! Only {available_quantity} units available.'
            
            return jsonify(response_data)
        return jsonify({
            'success': False,
            'message': 'Medicine not found or not properly linked to inventory'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching medicine details: {str(e)}'
        }), 500
    finally:
        cur.close()

@billing.route('/api/validate_quantity', methods=['POST'])
def validate_quantity():
    """API endpoint to validate medicine quantity"""
    try:
        data = request.get_json()
        medicine_id = data.get('medicine_id')
        quantity = int(data.get('quantity', 0))

        if not all([medicine_id, quantity]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
            
        # Get the pharmacy_medicine_id from pharmacy_ratelist
        cur = mysql.connection.cursor()
        try:
            # First, check if the medicine exists and get its pharmacy_medicine_id
            cur.execute("""
                SELECT pharmacy_medicine_id
                FROM pharmacy_ratelist
                WHERE id = %s
            """, (medicine_id,))
            
            result = cur.fetchone()
            if not result or not result['pharmacy_medicine_id']:
                return jsonify({
                    'success': False,
                    'message': 'Medicine not found or not properly linked to inventory'
                }), 404
                
            pharmacy_medicine_id = result['pharmacy_medicine_id']
            
            # Check available quantity in stock
            cur.execute("""
                SELECT SUM(COALESCE(quantity, 0)) as available_quantity
                FROM pharmacy_stock
                WHERE pharmacy_medicine_id = %s
            """, (pharmacy_medicine_id,))
            
            stock_result = cur.fetchone()
            available_quantity = int(stock_result['available_quantity']) if stock_result and stock_result['available_quantity'] else 0
            
            if quantity > available_quantity:
                # Return a warning message with available quantity
                return jsonify({
                    'success': False,
                    'valid': False,
                    'message': f'Warning: Cannot select quantity more than available stock. Only {available_quantity} units available.',
                    'available_quantity': available_quantity
                })
                
            return jsonify({
                'success': True,
                'valid': True,
                'available_quantity': available_quantity,
                'message': f'Available stock: {available_quantity} units'
            })
            
        finally:
            cur.close()

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error validating quantity: {str(e)}'
        }), 500

@billing.route('/api/calculate_bill', methods=['POST'])
def calculate_bill():
    """API endpoint to calculate final bill with stock validation"""
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({
                'success': False,
                'message': 'No items in bill'
            }), 400

        # Validate stock for all items before processing
        cur = mysql.connection.cursor()
        try:
            stock_warnings = []
            
            for item in items:
                medicine_id = item.get('medicine_id')
                quantity = int(item.get('quantity', 0))
                
                # Get pharmacy_medicine_id
                cur.execute("""
                    SELECT pharmacy_medicine_id
                    FROM pharmacy_ratelist
                    WHERE id = %s
                """, (medicine_id,))
                
                result = cur.fetchone()
                if not result or not result['pharmacy_medicine_id']:
                    stock_warnings.append(f"Medicine ID {medicine_id}: Not found or not linked to inventory")
                    continue
                    
                pharmacy_medicine_id = result['pharmacy_medicine_id']
                
                # Check available quantity
                cur.execute("""
                    SELECT SUM(COALESCE(quantity, 0)) as available_quantity
                    FROM pharmacy_stock
                    WHERE pharmacy_medicine_id = %s
                """, (pharmacy_medicine_id,))
                
                stock_result = cur.fetchone()
                available_quantity = int(stock_result['available_quantity']) if stock_result and stock_result['available_quantity'] else 0
                
                if quantity > available_quantity:
                    stock_warnings.append(f"Medicine ID {medicine_id}: Requested {quantity} units but only {available_quantity} available")
            
            # If any stock warnings, return them
            if stock_warnings:
                return jsonify({
                    'success': False,
                    'message': 'Stock validation failed',
                    'warnings': stock_warnings
                }), 400
                
        finally:
            cur.close()

        # Calculate totals if stock validation passed
        total_items = sum(int(item['quantity']) for item in items)
        total_amount = sum(float(item['net_amount']) for item in items)

        return jsonify({
            'success': True,
            'data': {
                'total_items': total_items,
                'total_amount': round(total_amount, 2)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error calculating bill: {str(e)}'
        }), 500