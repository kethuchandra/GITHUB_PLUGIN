from flask import Blueprint,request
pull_number = ""
user_name = ""
repo_name = ""

webhook_handler_payload = Blueprint("pull_request_listner", __name__, url_prefix="/webhook")
@webhook_handler_payload.route('/webhook', methods=['GET','POST'])
def webhook_handler():
    if request.method == 'POST':
        data = request.get_data(as_text=True) 
        payload = request.json  #Insert the payload json in static way           
        try:
            data = request.json
            pull_number = payload["pull_request"]["number"]
            user_name = payload["sender"]["login"]
            repo_name = payload["repository"]["name"]
            
        except Exception as e:
            return f"Error extracting values: {str(e)}"
        return "Webhook received successfully!", 200
    
if __name__ == '__main__':
    webhook_handler_payload.run(port=8081, debug=True)
