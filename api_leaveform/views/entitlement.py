from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import sessionlocal, LeaveEntitlement

session = sessionlocal()  # Create a new session for this operation

def create_entitlement():
    try:
        # Parse input data
        data = request.get_json()
        entitlement = LeaveEntitlement(
            employee_id=data['employee_id'],
            leave_type_id=data['leave_type_id'],
            entitlement_days=data['entitlement_days']
        )
        # Add the entitlement to the session and commit
        session.add(entitlement)
        session.commit()
        return jsonify(entitlement.to_dict()), 201
    except SQLAlchemyError as e:
        # Rollback the session on error
        session.rollback()
        return jsonify({"message": str(e)}), 400
    finally:
        # Ensure the session is closed
        session.close()


def get_entitlements(employee_id):

    try:
        entitlements = session.query(LeaveEntitlement).filter(
            LeaveEntitlement.employee_id == employee_id
        ).all()
        return jsonify([e.to_dict() for e in entitlements]), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()


def get_all_entitlement():
    
    try:
        entitlements = session.query(LeaveEntitlement).all()
        return jsonify([e.to_dict() for e in entitlements]), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()


def update_entitlement(id):

    try:
        entitlement = session.query(LeaveEntitlement).filter(
            LeaveEntitlement.id == id
        ).first()
        if not entitlement:
            return jsonify({"message": "Entitlement not found"}), 404

        # Update fields
        data = request.json
        entitlement.used_days += data.get('used_days', 0)
        session.commit()
        return jsonify(entitlement.to_dict()), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()


def delete_entitlement(id):
    
    try:
        entitlement = session.query(LeaveEntitlement).filter(
            LeaveEntitlement.id == id
        ).first()
        if not entitlement:
            return jsonify({"message": "Entitlement not found"}), 404

        # Delete the record
        session.delete(entitlement)
        session.commit()
        return jsonify({"message": "Entitlement deleted"}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()



def apply_leave():
    try:
        # Get data from the request
        data = request.json
        employee_id = data['employee_id']
        leave_type_id = data['leave_type_id']
        requested_days = data['requested_days']

        # Call the apply_leave function
        entitlement = session.query(LeaveEntitlement).filter(
            LeaveEntitlement.employee_id == employee_id,
            LeaveEntitlement.leave_type_id == leave_type_id
        ).first()

        if not entitlement:
            return jsonify({"message": "Entitlement not found"}), 404

        if entitlement.entitlement_days - entitlement.used_days < requested_days:
            return jsonify({"message": "Insufficient leave balance"}), 400

        # Deduct days and approve leave
        entitlement.used_days += requested_days
        session.commit()
        return jsonify({
            "message": "Leave approved",
            "remaining_days": entitlement.entitlement_days - entitlement.used_days
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()
