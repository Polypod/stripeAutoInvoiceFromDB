# python >= 3.6, stripe >= 3.7
import stripe
import config
import json
#import getJsonDB
#import clean_json

### - Check stripe is in test mode (api key) and that a test list of customers is used before running! - ###
stripe.api_key = config.api_key

def send_invoice(email, usergroups_str, name, data):
    customer_id = None

    # `data` is a list
    for cust in data:
        if cust.get("Email") == email:
            if "stripe_id" in cust:
                customer_id = cust["stripe_id"]
                break

    # Check if the customer exists in stripe, if not create customer and add it to data
    if customer_id is None:
        existing_customers = stripe.Customer.list(email=email, limit=1).data
        if existing_customers:
            customer_id = existing_customers[0].id
        else:
            customer = stripe.Customer.create(email=email, name=name, description="Customer for invoice")
            customer_id = customer.id
            data.append({"Email": email, "stripe_id": customer_id, "Name": name})  # Make sure this matches your data structure
            
    # Create and send invoice
    invoice = stripe.Invoice.create(customer=customer_id, collection_method='send_invoice', days_until_due=10)
    price_key = "ADULT" if "ADULT" in usergroups_str else "INSTRUCTOR" if "INSTRUCTOR" in usergroups_str else "KIDS" if "KIDS" in usergroups_str else "YOUTH"
    # TODO:1) If customer is in FAMILY usergroup, apply 18% discount or discount cupon. 2) TBD
    stripe.InvoiceItem.create(customer=customer_id, price=PRICES[price_key], invoice=invoice.id, discountable=True)
    
    stripe.Invoice.finalize_invoice(invoice.id)
    stripe.Invoice.send_invoice(invoice.id)

if __name__ == "__main__":
    
    # When testing done:
    # getJsonDB().main() --> DB contents as json file to data/xxx.json
    # clean_json().main() --> Extracts relevant json file contents,cleans them and saves to data/customer_links.json
    
    # TODO:Check if possible to get prices from stripe and populate PRICES
    PRICES = {
        "ADULT": "price_1Oj3LnARO9KHbTHv9KUreuCc",
        "INSTRUCTOR": "price_987654321",
        "KIDS": "price_1Oj5VGARO9KHbTHvCwWXhe4R",
        "YOUTH": "price_1Oj5X1ARO9KHbTHvpre8CRrh"
    }
    
    # Limit to a test case (short list of customers)
    with open('data/customer_links_test.json') as f:
        data = json.load(f)
    
    for user_data in data:
        send_invoice(user_data.get("Email"), user_data.get("Usergroups"), user_data.get("Name"), data)

    # Save updated data back to the JSON file if any new customers were added including their stripe_id
    with open('data/customer_links_updated.json', 'w') as f:
        json.dump(data, f, indent=4)
