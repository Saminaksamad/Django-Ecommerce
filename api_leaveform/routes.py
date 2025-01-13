from flask import Flask
import views.leavetypes as leavetypes
import views.calculationoptions as calculationoptions
import views.entitlement as entitlement

def register_routes(app):

    #route for leave types
    @app.route('/leavetypes', methods=['POST'])
    def create_leave_type():
        return leavetypes.create_leave_type()

    @app.route('/leavetypes', methods=['GET'])
    def get_leave_types():
        return leavetypes.get_leave_types()

    @app.route('/leavetypes/<int:id>', methods=['GET'])
    def get_leave_type(id):
        return leavetypes.get_leave_type(id)

    @app.route('/leavetypes/<int:id>', methods=['PUT'])
    def update_leave_type(id):
        return leavetypes.update_leave_type(id)

    @app.route('/leavetypes/<int:id>', methods=['DELETE'])
    def delete_leave_type(id):
        return leavetypes.delete_leave_type(id)

    
    
    #route for calculation options
    @app.route('/calculation-options', methods=['POST'])
    def create_calculation_option():
        return calculationoptions.create_calculation_option()
    
    @app.route('/calculation-options', methods=['GET'])
    def get_calculation_options():
        return calculationoptions.get_calculation_options()
          
    @app.route('/calculation-options/<int:id>', methods=['PUT'])
    def update_calculation_option(id):
        return calculationoptions.update_calculation_option(id)
    
    @app.route('/calculation-options/<int:id>', methods=['DELETE'])
    def delete_calculation_option(id):
        return calculationoptions.delete_calculation_option(id)
    
    
    
    
    #route for entitlements
    @app.route('/entitlements', methods=['POST'])
    def create_entitlement():
        return entitlement.create_entitlement()
    
    @app.route('/entitlements', methods=['GET'])
    def get_all_entitlements():
        return entitlement.get_all_entitlements()    
      
    @app.route('/entitlements/<int:employee_id>', methods=['GET'])
    def get_entitlements(employee_id):
        return entitlement.get_entitlements(employee_id)

    @app.route('/entitlements/<int:id>', methods=['PUT'])
    def update_entitlement(id):
        return entitlement.update_entitlement(id)
    
    @app.route('/entitlements/<int:id>', methods=['DELETE'])
    def delete_entitlement(id):
        return entitlement.delete_entitlement(id)
    

    #route for applying leave
    @app.route('/apply-leave', methods=['POST'])
    def apply_leave():
        return entitlement.apply_leave()