from flask import Flask, request, jsonify
from models import sessionlocal, LeaveType, LeaveCalculationOption

session = sessionlocal()

# Create a calculation option
def create_calculation_option():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'formula']):
            return jsonify({'message': 'Missing required fields'}), 400

        calculation_option = LeaveCalculationOption(
            name=data['name'],
            formula=data['formula']
        )
        session.add(calculation_option)
        session.commit()
        return jsonify(calculation_option.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e)}), 400
    finally:
        session.close()


# Get all calculation options
def get_calculation_options():
    calculation_options = session.query(LeaveCalculationOption).all()
    return jsonify([calculation_option.to_dict() for calculation_option in calculation_options])


# Update a calculation option
def update_calculation_option(id):
    try:
        calculation_option = session.query(LeaveCalculationOption).get(id)
        if not calculation_option:
            return jsonify({'message': 'Calculation option not found'}), 404

        data = request.get_json()
        calculation_option.name = data.get('name', calculation_option.name)
        calculation_option.formula = data.get('formula', calculation_option.formula)
        session.commit()
        return jsonify(calculation_option.to_dict()), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e)}), 400
    finally:
        session.close()


# Delete a calculation option
def delete_calculation_option(id):
    try:
        calculation_option = session.query(LeaveCalculationOption).get(id)
        if not calculation_option:
            return jsonify({'message': 'Calculation option not found'}), 404

        session.delete(calculation_option)
        session.commit()
        return jsonify({'message': 'Calculation option deleted'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e)}), 400
    finally:
        session.close()
