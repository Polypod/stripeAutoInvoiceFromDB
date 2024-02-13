# stripeAutoInvoiceFromDB
Pulls customer list from a member DB, adds members as stripe customers if they do not exist and sends out invoices (email) through Stripe with pricing based on customer user group.
The script uses the Stripe API: https://stripe.com/docs/api

To test:

1) Create config.py with api.key and DB auth. Make sure to use stripe in test/develop mode!
2) Run getJson.py and then clean_json to create json with customers from DB (adapt script to your DB)
3) Depending on your DB, manually make a short customer_list (1-2 customers) for testing. Recommend using your own email etc.
4) Run server.py
5) Check logs, generated customers and invoices etc @stripe.

The above is under development and for educational purposes. Use on your own risk, developer takes no resposibility for adverse results.
