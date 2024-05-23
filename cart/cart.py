
class Cart():
    def __init__(self, request):
        self.session = request.session 
        
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        
        # If the user is new, then create a new one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Make sure cart is available on all pages of the site
        self.cart = cart
