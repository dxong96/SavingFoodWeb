<<<<<<< Updated upstream
from app import app, db
from app.models import HawkerCentre, Food, Vendor, Cost, Discount

@app.shell_context_processor
def make_shell_context():
    return {
    	'db': db, 
    	'HawkerCentre': HawkerCentre, 
    	'Food': Food, 
    	'Vendor': Vendor, 
    	'Cost': Cost, 
    	'Discount': Discount
    }
=======
from app import app

 
>>>>>>> Stashed changes
