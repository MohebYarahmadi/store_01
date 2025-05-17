#!/usr/bin/env python3
import pandas as pd
from fpdf import FPDF


df = pd.read_csv('data.csv', dtype={'id': str, 'in stock': int})


class Item:
    def __init__(self, item_id):
        self.item_id = item_id
        self.name = df.loc[df['id'] == self.item_id, 'name'].squeeze()
        self.price = df.loc[df['id'] == self.item_id, 'price'].squeeze()

    def find(self):
        id_to_find = df.loc[df['id'] == self.item_id].squeeze()
        if self.item_id in df['id'].values:
            return True
        else:
            return False

    def in_stock(self):
        number = df.loc[df['id'] == self.item_id, 'in stock'].squeeze()
        return number

    def sold(self):
        df.loc[df['id'] == self.item_id, 'in stock'] -= 1
        df.to_csv('data.csv', index=False)


class Invoice:
    def __init__(self, item):
        self.item = item

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.item.item_id}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Item: {self.item.name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: ${self.item.price}", ln=1)

        pdf.output("receipt.pdf")


def main():
    print(df)
    item_id = input("Enter an item id to buy: ")
    item = Item(item_id)
    if item.find():
        if item.in_stock():
            invoice = Invoice(item)
            invoice.generate()
            item.sold()
        else:
            print('Not enough in stock.')
    else:
        print('Item not founded!')


if __name__ == "__main__":
    main()
