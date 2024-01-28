import sys
import requests


def main():
    """
    main function to run the code

    based on the given number of bitcoins given by user in the command-line:
    outputs the current cost of Bitcoins in USD to four decimal places,
    using , as a thousands separator.
    """

    """
    get the number of bitcoins given by the user in the command-line
    """
    number_bitcoins = get_number_bitcoins()

    """
    get the current bitcoin rate value
    """
    bitcoin_rate = get_bitcoin_rate_value()

    """
    calculate and outputs the current cost of Bitcoins in USD 
    to four decimal places, using , as a thousands separator.
    """
    amount = number_bitcoins * bitcoin_rate
    print(f"${amount:,.4f}")


def get_number_bitcoins():
    """
    Returns the number of bitcoins given by the user in the command-line.
    If the number of parameters is not correct or if the number bitcoins cannot be converted to a float
    exit the program with an error message.

    :return: The number of bitcoins given by the user in the command-line.
    """

    """
    exclude the file name from the command-line arguments
    """
    args = sys.argv[1:]

    if len(args) < 1:
        sys.exit("Missing command-line argument")
    elif len(args) > 1:
        sys.exit("Too many command-line arguments")

    try:
        return float(args[0])
    except ValueError:
        sys.exit("Command-line argument is not a number")


def get_bitcoin_rate_value():
    """
    Returns the bitcoin rate value, based on the coindesk API

    :return: The bitcoin rate float value.
    :raises KeyError: If the bpi\\USD\\rate_float json tags dosen't exists in coindesk API reponse.
    :raises ValueError: If the rate_float value returned by the coindesk API isn't a float value.
    :raises RequestException: If the coindesk API request raises an error.
    """
    try:

        """
        get the bitcoin data from the coindesk API
        """
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

        """
        raises an HTTPError for bad responses
        """
        response.raise_for_status()

        """
        get the bitcoin rate float value from json response
        """
        data = response.json()
        rate_float_value = data["bpi"]["USD"]["rate_float"]

        """
        converts the rate_float_value in a float and returns it
        """
        return float(rate_float_value)

    except KeyError:
        sys.exit("No bpi\\USD\\rate_float in the json response of the coindesk API!")
    except ValueError:
        sys.exit("rate_float is not a float value!")
    except requests.RequestException:
        sys.exit(
            "An error occurred when trying to get the bitcoin rate float value, through the coindesk API!"
        )


if __name__ == "__main__":
    main()
