from app import db
import random

class CollectRule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    item_name = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)
    parameter = db.Column(db.String(50), nullable=False)

    def __init__(self, item_name, product_name, rule_type, parameter):
        self.item_name = item_name
        self.product_name = product_name
        self.rule_type = rule_type
        self.parameter = parameter

    def calculte_rule(self):
        match self.rule_type:
            case "equal":
                return {
                    "item_name": self.product_name,
                    "count": int(self.parameter)
                }
            case "poss":
                return {
                    "item_name": self.product_name,
                    "count": 0 if random.random() > float(self.parameter) else 1
                } 
            case "rand":
                # Parse the parameter
                parameter = self.parameter.split(",")
                return {
                    "item_name": self.product_name,
                    "count": round(int(parameter[0]) + int(parameter[1]) * random.random())
                }
            case _:
                raise ValueError("Invalid rule type")