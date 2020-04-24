import shopify
from datetime import datetime
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

	def filter_orders(self, filter_date):
		"""Filter orders created at every Tuesday"""
		result = []
		orders = self.get_orders()
		for order in orders:
			order_created = datetime.strftime(order.attributes['created_at'], "%Y-%m-%d")
			if order_created == filter_date:
				entry = dict()
				result.push(order)

		return orders


if __name__ == "__main__":
	# Setup an instance
	api = ShopifyApi(API_KEY, PASSWORD, SHOP_NAME)

	# filter orders
	api.filter_orders()



