from test_io import echo
from fate_he_performance_test import PaillierAssess


def paillier_test(data_num, test_round, **kwargs):
    """
    paillier
    """
    echo.welcome()

    for method in ["Paillier", "IPCL"]:
        try:
            assess_table = PaillierAssess(method=method, data_num=data_num, test_round=test_round)
        except ValueError as e:
            print(e, "\n")
            continue

        table = assess_table.output_table()
        echo.echo(table)
    echo.farewell()


if __name__ == '__main__':
    paillier_test(16, 10)
