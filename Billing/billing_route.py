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
    """API endpoint to get medicine price and discount"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT 
                id,
                ratelist_name,
                amount,
                COALESCE(discount, 0) as discount
            FROM pharmacy_ratelist
            WHERE id = %s AND is_active = 1
        """, (medicine_id,))
        
        result = cur.fetchone()
        if result:
            return jsonify({
                'success': True,
                'data': {
                    'id': result['id'],
                    'name': result['ratelist_name'],
                    'amount': float(result['amount']),
                    'discount': float(result['discount'])
                }
            })
        return jsonify({
            'success': False,
            'message': 'Medicine not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    finally:
        cur.close()

@billing.route('/api/validate_quantity', methods=['POST'])
def validate_quantity():
    """API endpoint to validate medicine quantity"""
    try:
        data = request.get_json()
        medicine_id = data.get('medicine_id')
        quantity = data.get('quantity', 0)

        if not all([medicine_id, quantity]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400

        return jsonify({
            'success': True,
            'valid': True
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@billing.route('/api/calculate_bill', methods=['POST'])
def calculate_bill():
    """API endpoint to calculate final bill"""
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({
                'success': False,
                'message': 'No items in bill'
            }), 400

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
            'message': str(e)
        }), 500