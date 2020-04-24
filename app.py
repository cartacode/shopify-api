import shopify
from datetime import datetime
import csv
from env import API_KEY, PASSWORD, SHOP_NAME
import pdb

DOD_HEADERS = ['DATE_CREATED', 'DIVISION', 'DESPATCH_NUMBER', 'DESPATCH_NOTE', 'RUK_ROUTE_CODE', 'SYS_SHIPPING_DATE', 'ORDER_NUMBER', 'ORDER_LINE_NUMBER', 'PART_CODE', 'AFC', 'IPR', 'CATCHWEIGHT', 'SUM_A_SALES_QTY_IN_DESPATCH_', 'CUST_PART_NUM', 'CUST_DESC', 'CUST_STYPE', 'DOM_DATE', 'BBE_DATE', 'LOT', 'REC_TRANS_COND', 'WEIGHT', 'UNIT_OD_MEASURE', 'PACK_QUAN', 'NAV_LINE_NO']
DOH_HEADERS = ['DIVISION', 'DESPATCH_NUMBER', 'DATE_CREATED', 'DESPATCH_NOTE', 'WAREHOUSE', 'CUSTOMER_NUMBER', 'DELIVERY_ADDRESS_CODE', 'RUK_ROUTE_CODE', 'SYS_SHIPPING_DATE', 'ORDER_NUMBER', 'CUSTOMER_NAME', 'SYS_ADDRESS_1', 'SYS_ADDRESS_2', 'SYS_ADDRESS_3', 'SYS_ADDRESS_4', 'SYS_CITY', 'SYS_STATE', 'SYS_POSTAL_CODE', 'SYS_COUNTRY', 'CUST_ORDER_REF', 'DELIVERY_PHONE', 'NOTIFICATION_PHONE', 'NOTIFICATION_EMAIL', 'CARRIER', 'SERVICE', 'NOTES']


class ShopifyApi:
	def __init__(self, api_key, password, shop_name):
		shop_url = "https://%s:%s@%s.myshopify.com/admin" % (api_key, password, shop_name)
		shopify.ShopifyResource.set_site(shop_url)
		self.order = shopify.Order()

	def get_orders(self):
		"""List orders"""
		return self.order.find();

	def get_full_name(customer):
		full_name = ''

		if 'first_name' not in customer:
			return customer['last_name'] if 'last_name' in customer else ''

		full_name = customer['first_name']
		return '{} {}'.format(full_name, customer['last_name']) if 'last_name' in customer else full_name


	def convert_order(self, order, line_num):
		entry = dict()

		# Common data for both CSV
		entry['DATE_CREATED'] = order.attributes['created_at']
		entry['DIVISION'] = 1
		entry['DESPATCH_NUMBER'] = order.attributes['id']
		entry['DESPATCH_NOTE'] = order.attributes['id']
		shipping_address = order.shipping_address.attributes
		entry['RUK_ROUTE_CODE'] = (shipping_address['address1'] + shipping_address['zip']).trip()
		# DOD
		entry['SYS_SHIPPING_DATE'] = ''
		entry['ORDER_NUMBER'] = order.attributes['id']
		entry['ORDER_LINE_NUMBER'] = line_num
		entry['PART_CODE'] = ''
		entry['AFC'] = 1
		entry['IPR'] = ''
		entry['CATCHWEIGHT'] = ''
		entry['SUM_A_SALES_QTY_IN_DESPATCH_'] = 1
		entry['CUST_PART_NUM'] = ''
		entry['CUST_DESC'] = ''
		entry['CUST_STYPE'] = ''
		entry['DOM_DATE'] = ''
		entry['BBE_DATE'] = ''
		entry['LOT'] = ''
		entry['REC_TRANS_COND'] = ''
		entry['WEIGHT'] = ''
		entry['UNIT_OD_MEASURE'] = ''
		entry['PACK_QUAN'] = ''
		entry['NAV_LINE_NO'] = ''
		# DOH
		entry['WAREHOUSE'] = ''

		customer = order.customer.attributes
		entry['CUSTOMER_NUMBER'] = customer['id']
		entry['CUSTOMER_NAME'] = self.get_full_name(customer)
		entry['DELIVERY_ADDRESS_CODE'] = ''
		entry['SYS_SHIPPING_DATE'] = ''
		entry['SYS_ADDRESS_1'] = shipping_address['address1']
		entry['SYS_ADDRESS_2'] = shipping_address['address2']
		entry['SYS_ADDRESS_3'] = ''
		entry['SYS_ADDRESS_4'] = ''
		entry['SYS_CITY'] = shipping_address['city']
		entry['SYS_STATE'] = shipping_address['state']
		entry['SYS_POSTAL_CODE'] = shipping_address['zip']
		entry['SYS_COUNTRY'] = shipping_address['country_code']
		entry['CUST_ORDER_REF'] = ''
		entry['DELIVERY_PHONE'] = shipping_address['phone']
		entry['NOTIFICATION_PHONE'] = order.billing_address.attributes['phone']
		entry['NOTIFICATION_EMAIL'] = order.billing_address.attributes['email']
		entry['CARRIER'] = 'Parcelforce'
		entry['SERVICE'] = '24HR'
		entry['NOTES'] = ''

		return entry


	def filter_orders(self, filter_date):
		"""Filter orders created at every Tuesday"""
		result = []
		orders = self.get_orders()
		pdb.set_trace()
		for order in orders:
			order_created = datetime.strptime(order.attributes['created_at'].split('T')[0], "%Y-%m-%d")
			if order_created.date() == filter_date:
				sum_sales_qty = len(order.line_items)
				line_num = 0

				for line_item in order.line_items:
					entry = dict()
					entry = self.convert_order(order, line_num)
					entry['SUM_A_SALES_QTY_IN_DESPATCH_'] = sum_sales_qty					
					result.append(entry)
					line_num = line_num + 1
		return result

	def total_count(self):
		return self.order.count()


if __name__ == "__main__":
	# Setup an instance
	api = ShopifyApi(API_KEY, PASSWORD, SHOP_NAME)

	# Get total count of orders
	print(api.total_count())

	# filter orders
	current_date = datetime(2020, 4, 24).date()
	orders = api.filter_orders(current_date)
	print(len(orders))

	# # Write DOD
	# with open("DOD_123456.csv", "w") as f:
	# 	writer = csv.DictWriter(
	# 	    f, fieldnames=DOD_HEADERS)
	# 	writer.writeheader()
	# 	writer.writerows(orders)
	# 	f.close()

	# Write DOH
	with open("DOH_123456.csv", "w") as f:
		writer = csv.DictWriter(
		    f, fieldnames=DOH_HEADERS)
		writer.writeheader()
		writer.writerows(orders)
		f.close()



