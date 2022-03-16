from datetime import date
import unittest
from trade_store import TradeStore


class TestTradeStore(unittest.TestCase):
    header = TradeStore.csv_header

    sample_trade = "1,2017-11-01,Brent (Swap),buy,48,198048"
    sample_position = {'Brent (Swap)': 48, 'WTI': 0, 'LSGO': 0, 'Sing 180': 0, 'Sing 380': 0}

    sample_trade_2 = "2,2017-11-20,WTI,buy,48,164112"
    sample_position_2 = {'Brent (Swap)': 48, 'WTI': 48, 'LSGO': 0, 'Sing 180': 0, 'Sing 380': 0}

    sample_trade_3 = "3,2017-11-20,Brent (Swap),sell,48,128048"
    sample_position_3 = {'Brent (Swap)': -48, 'WTI': 0, 'LSGO': 0, 'Sing 180': 0, 'Sing 380': 0}

    sample_trade_4 = "1,2017-11-01,Brent (Swap),buy,99,198048"

    sample_position_4 = {'Brent (Swap)': 0, 'WTI': 0, 'LSGO': 0, 'Sing 180': 0, 'Sing 380': 0}
    sample_position_5 = {'Brent (Swap)': -48, 'WTI': 48, 'LSGO': 0, 'Sing 180': 0, 'Sing 380': 0}
    sample_position_6 = {'Brent (Swap)': 99, 'WTI': 0, 'LSGO': 0, 'Sing 180': 0, 'Sing 380': 0}

    def test_add_trade(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        self.assertEqual(ts.trades(), [self.sample_trade])

    def test_add_trade_and_check_position(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        self.assertEqual(ts.position(), self.sample_position)

    def test_add_2_trades_and_check_position(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        ts.add(self.sample_trade_2)
        self.assertEqual(ts.position(), self.sample_position_2)

    def test_add_sell_trade_and_check_position(self):
        ts = TradeStore()
        ts.add(self.sample_trade_3)
        self.assertEqual(ts.position(), self.sample_position_3)

    def test_add_balanced_trade_and_check_position(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        ts.add(self.sample_trade_3)
        self.assertEqual(ts.position(), self.sample_position_4)

    def test_add_duplicate_trades_and_check_position(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        ts.add(self.sample_trade_4)
        self.assertEqual(ts.position(), self.sample_position_6)

    def test_add_2_trades_and_check_filtered_position(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        ts.add(self.sample_trade_2)
        ts.add(self.sample_trade_3)
        self.assertEqual(ts.position(date.fromisoformat("2017-11-20")), self.sample_position_5)

    def test_max_price(self):
        ts = TradeStore()
        ts.add(self.sample_trade_3)
        self.assertEqual(ts.max_price_per_lot("Brent (Swap)"), 2667)
        ts.add(self.sample_trade)
        self.assertEqual(ts.max_price_per_lot("Brent (Swap)"), 4126)

    def test_min_price(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        self.assertEqual(ts.min_price_per_lot("Brent (Swap)"), 4126)
        ts.add(self.sample_trade_3)
        self.assertEqual(ts.min_price_per_lot("Brent (Swap)"), 2667)

    def test_min_max_price(self):
        ts = TradeStore()
        ts.add(self.sample_trade)
        self.assertEqual(ts.min_price_per_lot("Brent (Swap)"), 4126)
        self.assertEqual(ts.max_price_per_lot("Brent (Swap)"), 4126)
        ts.add(self.sample_trade_3)
        self.assertEqual(ts.min_price_per_lot("Brent (Swap)"), 2667)
        self.assertEqual(ts.max_price_per_lot("Brent (Swap)"), 4126)


if __name__ == "__main__":
    unittest.main()