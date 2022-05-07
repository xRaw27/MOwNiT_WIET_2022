from datasets import load_dataset
from BrowserData import BrowserData


def main():
    dataset = load_dataset("wikipedia", "20220301.simple")["train"]

    browser_data = BrowserData()
    browser_data.create_and_save(dataset[:50000], 50000)
    # browser_data.load_data()

    print(browser_data.matrix)

    # for i in range(10):
    #     print(browser_data.entries[i]["title"])
    #     print(browser_data.entries[i]["short_text"])
    #     print(browser_data.entries[i]["words"])
    # print(len(browser_data.terms))


if __name__ == "__main__":
    main()
