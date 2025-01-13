from flask import Flask, request, jsonify
from models import sessionlocal, LeaveType, LeaveCalculationOption

session = sessionlocal()

# Fetch all leave types
def get_leave_types():
    try:
        leave_types = session.query(LeaveType).all()
        results = [leave_type.to_dict() for leave_type in leave_types]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()

# Fetch a single leave type
def get_leave_type(id):
    try:
        leave_type = session.query(LeaveType).get(id)
        if leave_type:
            return jsonify(leave_type.to_dict()), 200
        return jsonify({'message': 'Leave type not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()

# Create a leave type
def create_leave_type():
    try:
        data = request.get_json()
        # Validation for required fields
        if not all(key in data for key in ['name', 'description', 'calculation_option_id']):
            return jsonify({'message': 'Missing required fields'}), 400

        leave_type = LeaveType(
            name=data['name'],
            description=data['description'],
            calculation_option_id=data['calculation_option_id']
        )
        session.add(leave_type)
        session.commit()
        return jsonify(leave_type.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e)}), 400
    finally:
        session.close()

# Update a leave type
def update_leave_type(id):
    try:
        leave_type = session.query(LeaveType).get(id)
        if not leave_type:
            return jsonify({'message': 'Leave type not found'}), 404

        data = request.get_json()
        leave_type.name = data.get('name', leave_type.name)
        leave_type.description = data.get('description', leave_type.description)
        leave_type.calculation_option_id = data.get('calculation_option_id', leave_type.calculation_option_id)
        session.commit()
        return jsonify(leave_type.to_dict()), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e)}), 400
    finally:
        session.close()

# Delete a leave type
def delete_leave_type(id):
    try:
        leave_type = session.query(LeaveType).get(id)
        if not leave_type:
            return jsonify({'message': 'Leave type not found'}), 404

        session.delete(leave_type)
        session.commit()
        return jsonify({'message': 'Leave type deleted'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        session.close()

