import pandas as pd
import datetime

now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
receipt_path = './receipt/receipt_' + now + '.txt'

master_csv_path = "./master.csv"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list =[]
        self.item_master=item_master

    # レシートに書き込みする関数
    def write_to_receipt(self,txt):
        with open(receipt_path, 'a')as f:
            f.write(str(txt) + '\n')
    
    def add_item_order(self,item_code,item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
        #return self.item_order_list
        
    # def view_item_list(self):
    #     for item in self.item_order_list:
    #         print("商品コード:{}".format(item))
    
    # オーダー番号から商品情報を取得する（課題１）
    def get_item_data(self,order_code):
        # print(item_new_order_list)
        for m in self.item_master:
            if order_code==m.item_code:
                # print(m.item_name + ":" + str(m.price))
                return m.item_name,m.price

    # オーダーをコンソールから入力
    def input_order(self):
        while True:
            order_code = input("商品コードを入力してください。終了は0 >>>")
            if int(order_code) != 0:
                item_info = self.get_item_data(order_code)
                print(f"{item_info[0]} : 一個 {item_info[1]} 円 がオーダー登録されました")
                order_count = input("個数を入力してください >>>")
                self.add_item_order(order_code, order_count)

            else:
                print("登録を終了します。")
                break
    
    # オーダー登録した商品一覧表示
    def view_order(self):
        self.sum_price=0
        self.order_number=1
        for item_order, item_count in zip(self.item_order_list, self.item_count_list):
            self.write_to_receipt(f"{str(self.order_number)}品目目------------------")
            # item_order_listに格納されたコードからその商品の金額取得
            order_info = self.get_item_data(item_order)
            self.write_to_receipt(f"{order_info[0]} : 一個 {order_info[1]} 円")
            # 商品ごとの合計金額算出
            order_price = order_info[1]*int(item_count)
            self.write_to_receipt(f"         個数: {item_count} 合計金額: {order_price} 円")
            # 全合計金額を加算
            self.sum_price += order_price
            self.order_number += 1
        # txt = "総計：{} 円".format(str(self.sum_price))
        print(f"総計：{str(self.sum_price)} 円")
        # self.write_to_receipt(txt)
    
    def pay_change(self):
        deposit = input("支払い金額を入力してください >>")
        change = int(deposit) - self.sum_price
        # print("お釣り：{} 円".format(change))
        self.write_to_receipt("----------------------------------")
        self.write_to_receipt(f"総計：{str(self.sum_price)} 円")
        self.write_to_receipt(f"お預かり額：{deposit} 円")
        self.write_to_receipt(f"お釣り：{change} 円")


# マスタ登録
def master_from_csv(csv_path):
    item_master = []

    df=pd.read_csv(csv_path,dtype={"item_code":object})
    # df=pd.read_csv(csv_path)
    print(list(df["item_name"])) # (テスト出力)リストを出すには"list"をつける
    for item_code,item_name,price in zip(list(df["item_code"]),list(df["item_name"]),list(df["price"])):
            item_master.append(Item(item_code,item_name,price))
            print(f"{item_name}({item_code})")
    print("------- マスタ登録完了 ---------")
    return item_master


### メイン処理
def main():
    # マスタ登録
    # item_master=[]
    # item_master.append(Item("001","りんご",100))
    # item_master.append(Item("002","なし",120))
    # item_master.append(Item("003","みかん",150))
    item_master=master_from_csv(master_csv_path)
    
    # オーダー登録
    # item_new_order_list = []
    #item_order_list =[]
    #item_count_list =[]
    order=Order(item_master)
    # order.add_item_order("001")
    # order.add_item_order("002")
    # x = order.add_item_order("003")
    order.input_order()
    
    # オーダー表示
    order.view_order()

    # 支払いからお釣り計算
    order.pay_change()
    
if __name__ == "__main__":
    main()