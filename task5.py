from datetime import datetime


# Base class
class Record:
    def publish(self):
        raise NotImplementedError("Subclasses must implement publish method")


# News class
class News(Record):
    def __init__(self, text, city):
        self.text = text
        self.city = city

    def publish(self):
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        return (
            "News\n"
            "-------------------------\n"
            f"{self.text}\n"
            f"{self.city}, {current_date}\n\n"
        )


# Private Ad class
class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        self.text = text
        self.expiration_date = expiration_date

    def publish(self):
        exp_date = datetime.strptime(self.expiration_date, "%d/%m/%Y")
        today = datetime.now()
        days_left = (exp_date - today).days

        return (
            "Private Ad\n"
            "-------------------------\n"
            f"{self.text}\n"
            f"Actual until: {self.expiration_date}, {days_left} days left\n\n"
        )


# Unique record type
class JokeOfTheDay(Record):
    def __init__(self, text):
        self.text = text

    def publish(self):
        # Simple "funny meter" based on length
        funny_score = min(len(self.text) // 10, 10)

        return (
            "Joke of the Day\n"
            "-------------------------\n"
            f"{self.text}\n"
            f"Funny meter: {funny_score}/10\n\n"
        )


# Function to save to file
def save_to_file(content, filename="news_feed.txt"):
    with open(filename, "a") as file:
        file.write(content)


# Main program
def main():
    while True:
        print("\nSelect what you want to add:")
        print("1 - News")
        print("2 - Private Ad")
        print("3 - Joke of the Day")
        print("0 - Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            text = input("Enter news text: ")
            city = input("Enter city: ")
            record = News(text, city)

        elif choice == "2":
            text = input("Enter ad text: ")
            expiration_date = input("Enter expiration date (dd/mm/yyyy): ")
            record = PrivateAd(text, expiration_date)

        elif choice == "3":
            text = input("Enter your joke: ")
            record = JokeOfTheDay(text)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")
            continue

        content = record.publish()
        save_to_file(content)
        print("Record added successfully!")


if __name__ == "__main__":
    main()
