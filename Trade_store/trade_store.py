from datetime import datetime

class TradeStore():
    csv_header = ['trade_id', 'date', 'product', 'action', 'quantity', 'price']
    products = ['Brent (Swap)', 'WTI', 'LSGO', 'Sing 180', 'Sing 380']
    actions = ['buy', 'sell']

    def __init__(self):
        #Variables for crucial feature of trade history
        self.trade_id_key_pairs = dict() #For lower time complexity
        self.trades_sorted_by_id = []
        self.trades_in_csv = [] #For lower time complexity, same ordering as .trades_sorted_by_id
        
        #Positions memory for lower time complexity
        self.overall_position = Position()
        self.position_by_date = dict() #dictionary od position objects keys = dates
        
        #Max/min lots price memory for lower time complexity
        self.max_lot_price_by_product = ProductsLotPrices()
        self.min_lot_price_by_product = ProductsLotPrices()

    #Complexity of O(1)
    def increment_positions(self,trade):
        self.overall_position.increment(trade.product, trade.amount)
        if not trade.date in self.position_by_date.keys(): self.position_by_date[trade.date] = Position()
        self.position_by_date[trade.date].increment(trade.product, trade.amount)
    
    #Complexity of O(1)
    def update_max_min_lot_prices(self,trade):
        self.max_lot_price_by_product.update(trade.product,trade.lot_price,max)
        self.min_lot_price_by_product.update(trade.product,trade.lot_price,min)
        
    #Complexity of O(n)
    def slow_update_max_min_lot_prices(self):
        for trade in self.trades_sorted_by_id: self.update_max_min_lot_prices(trade)

    #Utility methods for manipulating both TradeStore() lists
    def append_both_lists(self,object_item,csv_item):
        self.trades_sorted_by_id.append(object_item)
        self.trades_in_csv.append(csv_item)

    def assign_both_lists(self,index,object_item,csv_item):
        self.trades_sorted_by_id[index] = object_item
        self.trades_in_csv[index] = csv_item

    #Moves items 1 increment towards end of list (highest id). WARNING: Overrides previous item!
    def move_trade_further_both_lists(self,index):
        self.assign_both_lists(index+1,self.trades_sorted_by_id[index],self.trades_in_csv[index])

    #Esthetic methods for higher clarity in .add()
    def is_lot_price_max(self,trade):
        return trade.lot_price == self.max_lot_price_by_product.of(trade.product)
    
    def is_lot_price_min(self,trade):
        return trade.lot_price == self.min_lot_price_by_product.of(trade.product)

    #Complexity of O(1) if new trade id bigger than previous highest. Otherwise worst case complexity of O(n)
    def insert_trade_to_lists(self,new_trade,trade_string):
        #Keeping the lists sorted with each addition
        initial_length = len(self.trades_sorted_by_id)
        index = initial_length

        #Under assumption that most new trades will have unique highest id's having a conditional append() (complexity O(1)) increases performance
        if initial_length == 0: self.append_both_lists(new_trade,trade_string)
        elif new_trade.id > self.trades_sorted_by_id[-1].id: self.append_both_lists(new_trade,trade_string)

        else:
            index = initial_length-1
            self.append_both_lists(None,None)

            #Using the below while loop should have better performance than regular insertion under assumption that generally newer trades have higher id's.    
            while self.trades_sorted_by_id[index].id > new_trade.id:
                self.move_trade_further_both_lists(index)
                index -= 1
                if index < 0: break
                
            index +=1
            self.assign_both_lists(index,new_trade,trade_string)

        return index

    #Complexity of O(1) in best case and complexity of O(n) in worst
    def add(self, trade_string):

        new_trade = Trade(trade_string)
        id = new_trade.id
        
        if id in self.trade_id_key_pairs:

            key = self.trade_id_key_pairs[id]
            old_trade = self.trades_sorted_by_id[key]
            self.assign_both_lists(key,new_trade,trade_string)
            
            #It's only necessary to call .slow_update_max_min_lot_prices() (complexity O(n)) when replaced trade equals min/max 
            #because slow_update ensures min/max from whole trades history
            if self.is_lot_price_max(old_trade) or self.is_lot_price_min(old_trade): self.slow_update_max_min_lot_prices()
            
            old_trade.amount = -old_trade.amount
            self.increment_positions(old_trade)
            self.increment_positions(new_trade)
        
        else:

            self.increment_positions(new_trade)
            self.update_max_min_lot_prices(new_trade)
            index = self.insert_trade_to_lists(new_trade,trade_string) #Key performance bottleneck in this else block in worst case
            self.trade_id_key_pairs[id] = index

    # Complexity of O(1)
    def trades(self):
        return self.trades_in_csv
    
    # Complexity of O(1) if hashmaps not overloaded
    def position(self, position_date=None):
        if position_date is None: return self.overall_position.the_dictionary
        else: return self.position_by_date[position_date].the_dictionary

    # Complexity of O(1) if hashmaps not overloaded
    def max_price_per_lot(self, product):
        return self.max_lot_price_by_product.of(product)

    # Complexity of O(1) if hashmaps not overloaded
    def min_price_per_lot(self, product):
        return self.min_lot_price_by_product.of(product)

class Trade(TradeStore):
    
    def __init__(self, csv_string):
        #Trade info stored in dict instead of hard typed varibles for slightly more robustness if new unsignificant trade parameters will be added
        self.trade_info = dict(zip(self.csv_header,csv_string.split(","))) 
        self.trade_info['date'] = datetime.strptime(self.trade_info['date'], '%Y-%m-%d').date()
        self.trade_info['trade_id'] = int(self.trade_info['trade_id'])

        #Crucial trade info used throught the class is assigned to own instance variables
        self.product = self.trade_info['product']
        self.amount = int(self.trade_info['quantity'])
        if self.trade_info['action'] == 'sell': self.amount = -self.amount
        self.date = self.trade_info['date']
        self.id = self.trade_info['trade_id']
        self.lot_price = int(self.trade_info['price']) // int(self.trade_info['quantity']) #Used integer division as prices are to be kept integer cents and rounded down

class Position(TradeStore):

    def __init__(self):
        self.the_dictionary = {product: 0 for product in self.products}

    def increment(self,product,how_much):
        self.the_dictionary[product] += how_much

class ProductsLotPrices(TradeStore):

    def __init__(self):
        self.the_dictionary = {product: None for product in self.products}

    #Decorative method for code clarity
    def of(self,product):
        return self.the_dictionary[product]

    def update(self,product,lot_price,function):
        if self.of(product) is None: 
            self.the_dictionary[product] = lot_price
        else: 
            self.the_dictionary[product] = function(self.of(product),lot_price)