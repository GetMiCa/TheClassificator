import datetime


class Cleaner(object):
    def __init__(self):
        self.discard_element_file = "./results/discarded.txt"
        self.replace_condition = [("surface", [("m²", ""),
                                               ("da", "")]),
                                  ("floor", [("t", "0"),
                                             ("s", "-1"),
                                             ("a", "100"),
                                             ("r", "100")]),
                                  ("price", [("€", ""),
                                              ("da", ""),
                                             (".","")])]
        self.discard_condition = [("floor", '""=='),
                                  ("floor", "'m' in"),
                                  ("floor", "'+' in"),
                                  ("surface", "'/' in"),
                                  ("bathrooms", "''=="),
                                  ("bathrooms", "'m²' in"),
                                  ("bathrooms", "'t' in"),
                                  ("bathrooms", "'s4' in"),
                                  ("bathrooms", "'+' in"),
                                  ("bathrooms", "'r' in")]

    def process(self, data):
        (discarded, valid) = self.discard_element(data)
        for appartment in valid:
            appartment = self.format_values(appartment)
        with open(self.discard_element_file, 'w') as f:
            discarded_list = '\n'.join([str(disc) for disc in discarded])
            f.write(discarded_list)
        print(f"Cleaner is complete, discarded: {len(discarded)} over {len(data)}")
        return valid

    def format_values(self, app):
        for (prop, values) in self.replace_condition:
            for (old_val, new_val) in values:
                app[prop] = app[prop].replace(old_val, new_val).strip()
        return app

    def discard_element(self, data):
        valid = []
        discarded = []
        for app in data:
            if self.is_valid(app):
                valid.append(app)
            else:
                discarded.append(app)
        return (discarded, valid)

    def is_valid(self, data):
        if not self.check_price(data):
            return False
        for (prop, match) in self.discard_condition:
            if eval(f'{match}"{data[prop]}"'):
                return False
        return True

    def check_price(self, data):
        new = self.format_values(data)
        return new["price"].isdigit()
